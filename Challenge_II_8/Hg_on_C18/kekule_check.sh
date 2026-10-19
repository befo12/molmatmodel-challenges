#!/bin/bash
# Challenge II.8 (Hg on C18) - test of the graphene distortion: single points (course settings,
# energy_c18.py) of the relaxed bridge / hollow structures with the Hg atom removed, compared with
# the flat C18 (-2947.320598 eV). Run in this directory:  bash kekule_check.sh
export OMP_NUM_THREADS=1
set -e
for s in bridge hollow; do
  d=kekule_$s
  if [ ! -f $d/energy_c18.out ]; then
    mkdir -p $d && cp energy_c18.py C.upf $d/
    python -c "
from ase.io import read, write
a = read('site_$s/relaxation.traj', -1)
del a[[x.index for x in a if x.symbol == 'Hg']]
write('$d/c18.vasp', a, format='vasp')"
    (cd $d && python energy_c18.py > energy_c18.out 2>&1)
  fi
done
python - <<'EOF' | tee kekule_check.log
import re
g = lambda f: float(re.findall(r'Total energy\s*:\s*([-\d.]+)', open(f).read())[-1])
e0 = g('energy_c18.out')
print(f"flat C18 (course)          E = {e0:.6f} eV")
for s in ('bridge', 'hollow'):
    e = g(f'kekule_{s}/energy_c18.out')
    print(f"C18 from {s:<7} (no Hg)   E = {e:.6f} eV   E - E(flat) = {e - e0:+.3f} eV")
EOF
