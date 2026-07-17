Here are the txt files to be included in the database:
MRT-dist.txt
MRT-hscs.txt
MRT-phot.txt
MRT-xmat.txt
MRT-velo.txt

Specifications:
One table with all that from the MRT files
One row per YB
Format YB column: YB1, YB2, YB3, ... YB6176
License: Commons Attributions 4.0 License



Use these to answer questions in the planning process
format: 

question block
answer

cd /Users/wadevining/MIRION_Database
   python3 -c "import astrodbkit" 2>&1 | tail -3
   which uv 2>&1
   uv run pytest -p no:warnings tests -q 2>&1 | tail -60
   Run shell command

 This command requires approval

 Do you want to proceed?
 ❯ 1. Yes



cd /Users/wadevining/MIRION_Database
   python3 --version
   python3 -c "import astrodbkit, astrodb_utils, felis, pytest; print('all imports ok')" 2>&1
   pip3 show astrodbkit 2>&1 | head -5
   Run shell command

 This command requires approval

 Do you want to proceed?
 ❯ 1. Yes



cd /Users/wadevining/MIRION_Database
   python3 -m pytest -p no:warnings tests -q 2>&1 | tail -80
   Run shell command

 This command requires approval

 Do you want to proceed?
 ❯ 1. Yes



cd /Users/wadevining/MIRION_Database
   echo "=== id range check across files (first & last data row IDs) ==="
   for f in MRT-dist.txt MRT-hcsc.txt MRT-phot.txt MRT-velo.txt MRT-xmat.txt; do
     awk 'NF{last=$1} END{print FILENAME": last ID="last}' "$f"
   done
   echo "=== source json count vs unique yb numbers in filenames ==="
   ls data/source | sed -E 's/yb([0-9]+)\.json/\1/' | sort -n | tail -5
   ls data/source | sed -E 's/yb([0-9]+)\.json/\1/' | sort -n | head -5
   echo "=== check id 67 present as its own row (not sequential index) in phot file to confirm ID=catalog number ==="
   grep -E "^  67 " MRT-phot.txt | head -2
   Run shell command

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes



The repo already has a fully normalized MIRION database built from these 5 MRT files — Sources, Photometry (4 rows/source for bands), Distances, RadialVelocities, SEDParameters, and Names, all passing the 24-test suite. Should the new single-row-per-YB table be added alongside that existing structure, or replace it?

	Replace it


