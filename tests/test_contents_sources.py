"""
This module tests the contents of the Sources table (the MIRION Yellowball catalog).
As users add their own data, these tests should be modified to reflect the new data.

"""

import re

from sqlalchemy import or_

N_YB = 6176
YB_RE = re.compile(r"^YB(\d+)$")


def test_sources_count(db):
    # Test that Sources has one row per YB, YB1..YB6176
    n_sources = db.query(db.Sources).count()
    assert n_sources == N_YB, f"found {n_sources} sources, expected {N_YB}"


def test_sources_reference(db):
    # Every row should cite the MIRION catalog publication
    n_sources = (
        db.query(db.Sources).filter(db.Sources.c.reference == "WolfChase25").count()
    )
    assert n_sources == N_YB, f"found {n_sources} sources referencing WolfChase25"


def test_source_naming(db):
    # source must be "YB<n>" and match yb_number, covering 1..N_YB with no gaps/duplicates
    t = db.query(db.Sources.c.source, db.Sources.c.yb_number).astropy()

    yb_numbers = set()
    for source, yb_number in t.iterrows():
        m = YB_RE.match(source)
        assert m, f"source {source!r} does not match YB<n> format"
        assert int(m.group(1)) == yb_number, (
            f"source {source!r} does not match yb_number {yb_number}"
        )
        yb_numbers.add(yb_number)

    assert yb_numbers == set(range(1, N_YB + 1)), "yb_number does not cover 1..N_YB exactly once"


def test_galactic_coordinates(db):
    # Verify that populated Galactic latitude values are physically valid
    # (glon uses the catalog's own wraparound convention, so it isn't bounds-checked here)
    t = (
        db.query(db.Sources.c.source, db.Sources.c.glat)
        .filter(
            or_(
                db.Sources.c.glat < -90,
                db.Sources.c.glat > 90,
            )
        )
        .astropy()
    )

    assert len(t) == 0, f"{len(t)} Sources failed Galactic latitude checks: {t}"


def test_distances_nonnegative(db):
    # Populated distance values should be physically non-negative
    t = (
        db.query(db.Sources.c.source, db.Sources.c.dist)
        .filter(db.Sources.c.dist < 0)
        .astropy()
    )

    assert len(t) == 0, f"{len(t)} Sources have a negative adopted distance: {t}"
