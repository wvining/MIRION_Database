MIRION Catalog of Yellowballs Database
---------------------------

[![build](https://github.com/astrodbtoolkit/astrotemplate-db/actions/workflows/run_tests.yml/badge.svg)](https://github.com/astrodbtoolkit/astrotemplate-db/actions/workflows/run_tests.yml)  ![GitHub License](https://img.shields.io/github/license/astrodbtoolkit/astrodb-template-db)

An [AstroDB Toolkit](https://github.com/astrodbtoolkit) database for the **MIRION Catalog of Yellowballs**
(Wolf-Chase, Kerton, Devine, et al., "Bridging Intermediate- and High-Mass Star Formation with the MIRION
Catalog of Yellowballs"). The database has a single `Sources` table with one row per YB (`YB1`..`YB6176`),
merging the catalog's Distances, Herschel-Matched, Photometry, Velocities, and Cross-match tables. See
`schema.yaml` and [docs/schema/Sources.md](docs/schema/Sources.md) for the full column list, and
`scripts/build_mirion_dataset.py` for the generator that produces `data/source/*.json` from the source MRT
files at the repo root.

Usage instructions for the underlying framework are included in the companion `astrodb-utils` package:
[Getting started with a new database](https://astrodb-utils.readthedocs.io/en/latest/pages/make_new_db/getting_started_new_database.html)

Entity relationship diagram of the schema

![Entity Relationship Diagram](docs/figures/schema_erd.png)

Data license
------------

The catalog data (`data/source/*.json`) is released under CC BY 4.0 — see
[data/LICENSE-DATA.md](data/LICENSE-DATA.md) for the citation. The repository code/tooling is licensed
separately under BSD 3-Clause — see the top-level `LICENSE` file.

---
<!-- Do not delete this line. It is used to identify repositories based on this template. -->
This repository is based on the [astrodb-template](https://github.com/astrodbtoolkit/astrodb-template-db) template repository, which is part of the [AstroDB Toolkit](https://github.com/astrodbtoolkit).
