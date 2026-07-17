# Sources
The Sources table contains the full MIRION Yellowball (YB) catalog: one row per YB, combining the Distances, Herschel-Matched, Photometry, Velocities, and Cross-match tables from the source publication. The *source* identifier (YB1..YB6176) is unique.


Columns marked with an exclamation mark (❗️) may not be empty.
| Column Name | Description | Datatype | Length | Units  | UCD |
| --- | --- | --- | --- | --- | --- |
| ❗️ <ins>source</ins> | YB identifier for the source (YB<catalog ID>) | string | 12 |  | meta.id;src;meta.main  |
| ❗️ yb_number | MIRION catalog identification number (matches the ID column in the source MRT files) | int |  |  | meta.id  |
| ❗️ reference | Publication reference for this catalog entry; links to Publications table | string | 30 |  | meta.ref;meta.main  |
| dist | Adopted distance | double |  | kpc | pos.distance  |
| e_dist | Uncertainty in distance | double |  | kpc |   |
| dist_c | Distance from Elia et al. (2021) | double |  | kpc |   |
| dist_m | Distance from Mege et al. (2021) | double |  | kpc |   |
| e_dist_m | Uncertainty in distance from Mege et al. (2021) | double |  | kpc |   |
| stat_m | Status flag from Mege et al. (2021) | string | 11 |  |   |
| pfar | P_far parameter for Reid et al. (2019) distance finder (RDF) | double |  |  |   |
| dist_r1 | Most probable RDF distance | double |  | kpc |   |
| e_dist_r1 | Uncertainty in most probable RDF distance | double |  | kpc |   |
| pint_r1 | Integrated probability for most probable RDF distance | double |  |  |   |
| arm_r1 | Name of associated spiral arm for most probable RDF distance (1) | string | 5 |  |   |
| dist_r2 | Second-most probable RDF distance | double |  | kpc |   |
| e_dist_r2 | Uncertainty in second-most probable RDF distance | double |  | kpc |   |
| pint_r2 | Integrated probability for second-most probable RDF distance | double |  |  |   |
| arm_r2 | Name of associated spiral arm for second-most probable RDF distance (1) | string | 5 |  |   |
| diam | Diameter | double |  | pc |   |
| e_diam | Uncertainty in diameter | double |  | pc |   |
| mass | Mass | double |  | Msun | phys.mass  |
| e_mass | Uncertainty in mass | double |  | Msun |   |
| blum | Bolometric luminosity | double |  | Lsun | phys.luminosity  |
| e_blum | Uncertainty in bolometric luminosity | double |  | Lsun |   |
| lmrat | Bolometric luminosity/mass ratio | double |  | Lsun/Msun |   |
| e_lmrat | Uncertainty in bolometric luminosity/mass ratio | double |  | Lsun/Msun |   |
| temp | Temperature from graybody fit | double |  | K | phys.temperature  |
| e_temp | Uncertainty in temperature | double |  | K |   |
| lrat | Luminosity ratio | double |  |  |   |
| e_lrat | Uncertainty in luminosity ratio | double |  |  |   |
| tbol | Bolometric temperature | double |  | K | phys.temperature  |
| e_tbol | Uncertainty in bolometric temperature | double |  | K |   |
| sigma | Surface density | double |  | g/cm^2 |   |
| e_sigma | Uncertainty in surface density | double |  | g/cm^2 |   |
| glon | Galactic longitude | double |  | deg | pos.galactic.lon  |
| glat | Galactic latitude | double |  | deg | pos.galactic.lat  |
| mwpr | MWP radius | double |  | deg |   |
| e_glon | Uncertainty in Galactic longitude | double |  | deg |   |
| e_glat | Uncertainty in Galactic latitude | double |  | deg |   |
| e_mwpr | Uncertainty in MWP radius | double |  | deg |   |
| hrate | MWP hit rate | double |  |  |   |
| f8 | Flux density at 8 microns | double |  | Jy | phot.flux.density  |
| e_f8 | Uncertainty in flux density at 8 microns | double |  | Jy | phot.flux.density  |
| f12 | Flux density at 12 microns | double |  | Jy | phot.flux.density  |
| e_f12 | Uncertainty in flux density at 12 microns | double |  | Jy | phot.flux.density  |
| f24 | Flux density at 24 microns | double |  | Jy | phot.flux.density  |
| e_f24 | Uncertainty in flux density at 24 microns | double |  | Jy | phot.flux.density  |
| f70 | Flux density at 70 microns | double |  | Jy | phot.flux.density  |
| e_f70 | Uncertainty in flux density at 70 microns | double |  | Jy | phot.flux.density  |
| n8 | Number of photometric measurements at 8 microns | int |  |  |   |
| n12 | Number of photometric measurements at 12 microns | int |  |  |   |
| n24 | Number of photometric measurements at 24 microns | int |  |  |   |
| n70 | Number of photometric measurements at 70 microns | int |  |  |   |
| f_sat | Saturation flag (1) | string | 4 |  |   |
| f_multi | Multiple source flag (2) | int |  |  |   |
| f_nosrc | No clear source flag (1) | string | 4 |  |   |
| f_pconf | Poor confidence in photometry (1) | string | 4 |  |   |
| f_cext | Highly circular extended source (2) | int |  |  |   |
| vlsr | Adopted velocity (1) | double |  | km/s | spect.dopplerVeloc  |
| e_vlsr | Uncertainty in VLSR | double |  | km/s |   |
| stype | Type of spectrum (2) | string | 4 |  |   |
| vlsr_g | Velocity from GRS (3) | double |  | km/s |   |
| vlsr_s | Velocity from SEDIGISM (3) | double |  | km/s |   |
| vlsr_f | Velocity from FCRAO OGS (3) | double |  | km/s |   |
| vlsr_t | Velocity from ThrUMMS (3) | double |  | km/s |   |
| vlsr_dht | Velocity from DHT survey (3) | double |  | km/s |   |
| vlsr_dgt | Velocity from dense gas tracer (DGT) survey (3) | double |  | km/s |   |
| dgt | DGT survey (3) | string | 11 |  |   |
| vlsr_c | Velocity reported in Elia et al. (2021) | double |  | km/s |   |
| vlsr_m | Velocity reported in Mege et al. (2021) | double |  | km/s |   |
| e_vlsr_m | Uncertainty in VLSR_M | double |  | km/s |   |
| higal | Hi-GAL 360 source identifier | string | 22 |  |   |
| agal | ATLASGAL source identifier | string | 17 |  |   |
| corn | CORNISH source identifier | string | 17 |  |   |
| corn_t | CORNISH source type | string | 18 |  |   |
| rms | RMS source identifier | string | 18 |  |   |
| rms_t | RMS source type | string | 14 |  |   |
| wise | WISE source identifier | string | 15 |  |   |
| wise_t | WISE source type | string | 1 |  |   |

## Indexes
| Name | Columns | Description |
| --- | --- | --- |
| PK_Sources_source | ['#Sources.source'] | Primary key for Sources table |
| IDX_Sources_yb_number | ['#Sources.yb_number'] | Index for numeric lookups/sorting by catalog ID |

## Foreign Keys
| Description | Columns | Referenced Columns |
| --- | --- | --- |
| Link Sources reference to Publications table | ['#Sources.reference'] | ['#Publications.reference'] |
## Checks
| Description | Expression |
| --- | --- |
| Validate Galactic latitude range | glat >= -90 AND glat <= 90 |
