"""
One-off generator for the MIRION Yellowball catalog.

Parses the byte-by-byte headers and fixed-width data rows of the five MRT
(Machine Readable Table) files at the repo root, merges them by catalog ID
into one row per YB, converts sentinel/missing values to null, and writes:

  - data/source/mirion_sources.json  (one JSON array, 6176 rows)
  - schema_sources_columns.yaml      (the Felis `columns:` block to paste
                                       into the Sources table in schema.yaml)

Not part of the test/CI pipeline -- run manually when the MRT files change:

    python3 scripts/build_mirion_dataset.py
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MRT_FILES = [
    "MRT-dist.txt",
    "MRT-hcsc.txt",
    "MRT-phot.txt",
    "MRT-velo.txt",
    "MRT-xmat.txt",
]

N_SOURCES = 6176
MISSING_NUMERIC_SENTINEL = "999"

HEADER_LINE_RE = re.compile(
    r"^\s*(?P<start>\d+)(?:-\s*(?P<end>\d+))?\s+"
    r"(?P<fmt>\S+)\s+(?P<units>\S+)\s+(?P<label>\S+)\s+(?P<expl>.*?)\s*$"
)
FORMAT_RE = re.compile(r"^([AIF])(\d+)(?:\.(\d+))?$")

UCD_OVERRIDES = {
    "GLON": "pos.galactic.lon",
    "GLAT": "pos.galactic.lat",
    "DIST": "pos.distance",
    "VLSR": "spect.dopplerVeloc",
    "MASS": "phys.mass",
    "TEMP": "phys.temperature",
    "TBOL": "phys.temperature",
    "BLUM": "phys.luminosity",
}


def parse_format(fmt):
    m = FORMAT_RE.match(fmt)
    if not m:
        raise ValueError(f"Unrecognized format code: {fmt!r}")
    kind, width, _dec = m.groups()
    width = int(width)
    if kind == "A":
        return "string", width
    if kind == "I":
        return "int", width
    if kind == "F":
        return "double", width
    raise ValueError(f"Unhandled format kind: {kind!r}")


def parse_mrt_file(path):
    """Return (columns, data_lines) for one MRT file.

    columns: list of dicts with label/start/end/dtype/width/units/description
    data_lines: raw data lines (fixed-width rows)
    """
    lines = path.read_text().splitlines()
    dash_idxs = [i for i, line in enumerate(lines) if line.startswith("----")]

    col_start = dash_idxs[1] + 1
    col_end = dash_idxs[2]
    data_start = dash_idxs[-1] + 1

    columns = []
    for line in lines[col_start:col_end]:
        if not line.strip():
            continue
        m = HEADER_LINE_RE.match(line)
        if not m:
            raise ValueError(f"Could not parse header line in {path.name}: {line!r}")
        start = int(m.group("start"))
        end = int(m.group("end") or start)
        dtype, width = parse_format(m.group("fmt"))
        units = m.group("units")
        label = m.group("label")
        expl = " ".join(m.group("expl").split())  # collapse tabs/extra spaces
        columns.append(
            {
                "label": label,
                "start": start,
                "end": end,
                "dtype": dtype,
                "width": width,
                "units": None if units == "---" else units,
                "description": expl,
            }
        )

    data_lines = [line for line in lines[data_start:] if line.strip()]
    return columns, data_lines


def parse_value(raw, dtype):
    value = raw.strip()
    if value == "":
        return None
    if dtype == "string":
        return value
    if value == MISSING_NUMERIC_SENTINEL:
        return None
    if dtype == "int":
        return int(value)
    if dtype == "double":
        return float(value)
    raise ValueError(f"Unhandled dtype: {dtype!r}")


def parse_rows(columns, data_lines):
    """Return dict: id -> {label: value}"""
    max_end = max(c["end"] for c in columns)
    rows = {}
    id_col = next(c for c in columns if c["label"] == "ID")
    for line in data_lines:
        padded = line.ljust(max_end)
        # ID is parsed on its own, bypassing the generic sentinel-null logic:
        # a real catalog ID can legitimately equal the "999" missing-value
        # sentinel used for other numeric columns.
        row_id = int(padded[id_col["start"] - 1 : id_col["end"]].strip())
        record = {}
        for c in columns:
            if c is id_col:
                continue
            raw = padded[c["start"] - 1 : c["end"]]
            record[c["label"]] = parse_value(raw, c["dtype"])
        rows[row_id] = record
    return rows


def build_ucd(label, units):
    if label in UCD_OVERRIDES:
        return UCD_OVERRIDES[label]
    if label.startswith("F") and label[1:].isdigit():
        return "phot.flux.density"
    if units == "Jy":
        return "phot.flux.density"
    return None


def main():
    all_columns = {}  # label -> column metadata (excluding ID)
    all_rows = {i: {} for i in range(1, N_SOURCES + 1)}
    label_origin = {}

    for filename in MRT_FILES:
        path = REPO_ROOT / filename
        columns, data_lines = parse_mrt_file(path)
        rows = parse_rows(columns, data_lines)

        for c in columns:
            if c["label"] == "ID":
                continue
            if c["label"] in label_origin:
                raise ValueError(
                    f"Column label {c['label']!r} in {filename} already defined "
                    f"in {label_origin[c['label']]}"
                )
            label_origin[c["label"]] = filename
            all_columns[c["label"]] = c

        for row_id, record in rows.items():
            all_rows[row_id].update(record)

    # Build merged JSON rows: source, yb_number, reference, then MRT columns
    # in a stable order (dist, hcsc, phot, velo, xmat -- i.e. dict insertion
    # order from label_origin above).
    ordered_labels = list(all_columns.keys())

    # astrodbkit's load_json() expects each data/source/*.json file to hold
    # exactly one primary-table ("Sources") row, as {"Sources": [{...}]}, and
    # does one bulk SQL INSERT per file/row. (A single consolidated file with
    # all 6176 rows was tried and hits SQLite's bound-parameter limit: 79
    # columns x 6176 rows = 487,904 params in one INSERT, over the cap.)
    source_dir = REPO_ROOT / "data" / "source"
    n_written = 0
    for yb_number in range(1, N_SOURCES + 1):
        row = {
            "source": f"YB{yb_number}",
            "yb_number": yb_number,
            "reference": "WolfChase25",
        }
        record = all_rows[yb_number]
        for label in ordered_labels:
            row[label.lower()] = record.get(label)

        out_path = source_dir / f"yb{yb_number}.json"
        out_path.write_text(json.dumps({"Sources": [row]}, indent=2) + "\n")
        n_written += 1

    print(f"Wrote {n_written} per-source JSON files to {source_dir}")

    # Build the Felis columns: YAML block for the Sources table
    yaml_lines = []

    def emit_column(name, id_suffix, datatype, description, *, length=None,
                     units=None, ucd=None, nullable=None):
        yaml_lines.append(f"    - name: {name}")
        yaml_lines.append(f'      "@id": "#Sources.{id_suffix}"')
        yaml_lines.append(f"      datatype: {datatype}")
        if length is not None:
            yaml_lines.append(f"      length: {length}")
        if units is not None:
            yaml_lines.append(f"      fits:tunit: {units}")
        if ucd is not None:
            yaml_lines.append(f"      ivoa:ucd: {ucd}")
        desc = description.replace('"', "'")
        yaml_lines.append(f"      description: {desc}")
        if nullable is False:
            yaml_lines.append("      nullable: false")

    emit_column(
        "source", "source", "string", "YB identifier for the source (YB<catalog ID>)",
        length=12, ucd="meta.id;src;meta.main", nullable=False,
    )
    emit_column(
        "yb_number", "yb_number", "int",
        "MIRION catalog identification number (matches the ID column in the source MRT files)",
        ucd="meta.id", nullable=False,
    )
    emit_column(
        "reference", "reference", "string",
        "Publication reference for this catalog entry; links to Publications table",
        length=30, ucd="meta.ref;meta.main", nullable=False,
    )

    for label in ordered_labels:
        c = all_columns[label]
        name = label.lower()
        emit_column(
            name,
            name,
            c["dtype"],
            c["description"],
            length=c["width"] if c["dtype"] == "string" else None,
            units=c["units"],
            ucd=build_ucd(label, c["units"]),
        )

    out_yaml_path = REPO_ROOT / "schema_sources_columns.yaml"
    out_yaml_path.write_text("\n".join(yaml_lines) + "\n")
    print(f"Wrote Sources columns block ({len(ordered_labels) + 3} columns) to {out_yaml_path}")


if __name__ == "__main__":
    main()
