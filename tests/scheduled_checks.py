"""
These tests are not called on every push or pull request. They're time-intensive, so on GitHub they're only called
monthly. To run them locally, use the following command:

    pytest -s -rpP tests/scheduled_checks.py

Because the filename doesn't begin with test_, it's not automatically run with pytest. The -s flag is used to print
the results of the tests, and the -rpP flags are used to suppress the output of the tests that pass.

Note: the generic template's SIMBAD-name-resolution and SVO-filter-resolution checks were removed here.
YB<n> catalog identifiers are internal MIRION designations, not SIMBAD-registered object names, so
name resolution doesn't apply; and this schema has no PhotometryFilters/Spectra tables to check.
"""
