# Challenge I.7 (extra): ecutwfc convergence for CH4 at the optimized geometry
import os
from ase.io import read
from ase.calculators.espresso import Espresso, EspressoProfile
os.environ['OMP_NUM_THREADS'] = '1'
ch4 = read('ch4_opt.traj')          # last (optimized) structure
profile = EspressoProfile(command='mpirun -np 4 pw.x', pseudo_dir=os.path.abspath('.'))
res = []
for ec in [40, 50, 60, 70, 80, 90, 100]:
    ch4.calc = Espresso(profile=profile, directory=f'cut_{ec}',
                        pseudopotentials={'C': 'C.upf', 'H': 'H.upf'},
                        input_data={'control': {'calculation': 'scf', 'outdir': './outdir'},
                                    'system': {'ecutwfc': ec, 'ibrav': 0, 'nosym': True,
                                               'occupations': 'smearing', 'smearing': 'gaussian',
                                               'degauss': 0.02},
                                    'electrons': {'conv_thr': 1e-8}},
                        kpts=(1, 1, 1))
    res.append((ec, ch4.get_potential_energy()))
    print(f"done: {ec} Ry", flush=True)
print(f"\n{'ecutwfc/Ry':>10} {'E/eV':>14} {'E-E(100)/meV':>14}")
for ec, e in res:
    print(f"{ec:10d} {e:14.6f} {1000*(e-res[-1][1]):14.2f}")
