#
# Challenge I.7: ASE-driven Quantum ESPRESSO geometry optimization of CH4
# adapted from qe_h2o_optimize.py (Exercise I.7)
#
import os
from ase.build import molecule
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import BFGS

os.environ['OMP_NUM_THREADS'] = '1'

# PseudoDojo norm-conserving PBE pseudopotentials from the course repository
# (materials-modeling/H.upf, C.upf), copied into the working directory
PSEUDO_DIR = './'
pseudopotentials = {'C': 'C.upf', 'H': 'H.upf'}

EXP_RCH, EXP_ANGLE = 1.087, 109.47  # experiment (CCCBDB), Td symmetry

ch4 = molecule('CH4')
ch4.set_cell([12, 12, 12])
ch4.center()

input_data = {
    'control': {'calculation': 'scf', 'prefix': 'ch4', 'outdir': './outdir', 'tprnfor': True},
    'system': {
        'ecutwfc': 80.0,     # norm-conserving PPs need a higher cutoff than PAW
        'ibrav': 0, 'nosym': True, 'noinv': True,
        'occupations': 'smearing', 'smearing': 'gaussian', 'degauss': 0.02,
    },
    'electrons': {'conv_thr': 1e-8, 'mixing_beta': 0.7},
}

profile = EspressoProfile(command='mpirun -np 4 pw.x', pseudo_dir=PSEUDO_DIR)
ch4.calc = Espresso(profile=profile, pseudopotentials=pseudopotentials,
                    input_data=input_data, kpts=(1, 1, 1))

dyn = BFGS(ch4, trajectory='ch4_opt.traj', logfile='ch4_opt.log')
dyn.run(fmax=0.01)

r = [ch4.get_distance(0, i) for i in range(1, 5)]
ang = [ch4.get_angle(i, 0, j) for i in range(1, 5) for j in range(i + 1, 5)]
r_mean, a_mean = sum(r) / 4, sum(ang) / 6
print("Optimized C-H bond lengths (A): " + ", ".join(f"{x:.4f}" for x in r))
print("H-C-H angles (deg):             " + ", ".join(f"{x:.2f}" for x in ang))
print(f"Final energy (eV): {ch4.get_potential_energy():.4f}   BFGS steps: {dyn.nsteps}")
print()
print(f"{'':<14}{'QE (PBE)':>10}{'Exp.':>10}{'Diff.':>10}")
print(f"{'r(C-H) / A':<14}{r_mean:10.4f}{EXP_RCH:10.4f}{r_mean-EXP_RCH:+10.4f}")
print(f"{'H-C-H / deg':<14}{a_mean:10.2f}{EXP_ANGLE:10.2f}{a_mean-EXP_ANGLE:+10.2f}")
