#!/bin/bash
# Challenge II.8 (Hg on C18): course runs (on-top site) + bridge and hollow sites, then summary.
# Run in this directory:  bash run_hg_sites.sh      (each relaxation ~10-20 min with 4 MPI processes)
export OMP_NUM_THREADS=1
set -e
[ -f energy_c18.out ] || (mkdir -p sp_c18 && cd sp_c18 && cp ../energy_c18.py ../c18.vasp ../C.upf . && python energy_c18.py > ../energy_c18.out 2>&1)
[ -f energy_Hg.out ]  || (mkdir -p sp_hg && cd sp_hg && cp ../energy_Hg.py ../hg.vasp ../Hg.upf . && python energy_Hg.py > ../energy_Hg.out 2>&1)
[ -f relaxation_Hg_C18.out ] || python relaxation_Hg_C18.py > relaxation_Hg_C18.out 2>&1          # on-top site (course)
for s in bridge hollow; do
  [ -f site_$s/relaxation_Hg_C18.out ] || (cd site_$s && python relaxation_Hg_C18.py > relaxation_Hg_C18.out 2>&1)
done
python hg_sites_summary.py | tee hg_sites_summary.log
