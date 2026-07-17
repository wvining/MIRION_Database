Here are the txt files to be included in the database:
@MRT-dist.txt
@MRT-hscs.txt
@MRT-phot.txt
@MRT-xmat.txt
@MRT-velo.txt

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


 for f in MRT-dist.txt MRT-hcsc.txt MRT-phot.txt MRT-velo.txt MRT-xmat.txt; do echo "=== $f ==="; head -60 "$f"; echo; done
   Show header/byte-by-byte description of each MRT file

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes


 
echo "--- full data/source listing ---"; ls -la /Users/wadevining/MIRION_Database/data/source; echo "--- git log --all ---"; git -C /Users/wadevining/MIRION_Database log --all --oneline; echo "--- grep YB in schema.yaml ---"; grep -in "yb\|mirion" /Users/wadevining/MIRION_Database/schema.yaml | head -20; echo "--- data/reference/Publications.json ---"; cat /Users/wadevining/MIRION_Database/data/reference/Publications.json
   Check full source data listing, git history, and search for MIRION/YB references

 This command requires approval

 Do you want to proceed?
 ❯ 1. Yes


 
 cd /Users/wadevining/MIRION_Database
   for f in MRT-dist.txt MRT-hcsc.txt MRT-phot.txt MRT-velo.txt MRT-xmat.txt; do
     echo "=== $f ==="
     # find start of data (line after the last dashes separator)
     datastart=$(grep -n '^--------' "$f" | tail -1 | cut -d: -f1)
     datastart=$((datastart+1))
     tail -n +$datastart "$f" | awk 'NF{print}' > /tmp/_data_$f.txt
     echo "rows: $(wc -l < /tmp/_data_$f.txt)"
     echo "first id: $(head -1 /tmp/_data_$f.txt | awk '{print $1}')"
     echo "last id: $(tail -1 /tmp/_data_$f.txt | awk '{print $1}')"
   done
   Determine data row counts and ID ranges for each MRT file

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes


 
 cd /Users/wadevining/MIRION_Database
   echo "--- check for footnotes/notes at end of files that might not be data ---"
   for f in MRT-dist.txt MRT-hcsc.txt MRT-phot.txt MRT-velo.txt MRT-xmat.txt; do
     echo "=== $f tail -5 ==="
     tail -5 "$f"
   done
   Check tails of MRT files for trailing notes vs data

 Contains simple_expansion

 Do you want to proceed?
 ❯ 1. Yes


 
cd /Users/wadevining/MIRION_Database
   echo "--- Sources table definition ---"
   awk '/- name: Sources/{flag=1} flag && /- name: [A-Z]/ && !/- name: Sources/{print; exit} flag{print}' schema.yaml | head -80
   Extract Sources table definition from schema.yaml

 This command requires approval

 Do you want to proceed?
 ❯ 1. Yes

 
The template schema currently requires every source to have a `reference` (foreign key to a Publications table with DOI/bibcode). Should the new single-table schema keep a minimal Publications lookup + reference column (so the MIRION paper's citation is recorded properly), or should the table be completely flat with zero foreign keys / lookup tables?

❯ 1. Flat table + Publications FK


The MRT files use sentinel values for missing data (e.g. 999 for missing floats, blank for missing strings), and MRT-hcsc.txt is missing entirely for ~2200 IDs (only 3945 of 6176 have Herschel-matched data). How should missing data be represented in the database?

❯ 1. Convert to NULL



The repo already has a fully normalized MIRION database built from these 5 MRT files — Sources, Photometry (4 rows/source for bands), Distances, RadialVelocities, SEDParameters, and Names, all passing the 24-test suite. Should the new single-row-per-YB table be added alongside that existing structure, or replace it?

	Replace it


