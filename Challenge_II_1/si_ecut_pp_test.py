"""Challenge II.1: Si total energy vs. ecutwfc for three different pseudopotentials.
Same Si structure and settings as Si.in / si_ase.py (Exercise II.1), driven by ASE.
  dojo  : Si.upf (course, PseudoDojo norm-conserving, PBE)
  rrkjus: Si.pbe-nl-rrkjus_psl.1.0.0.UPF (pslibrary ultrasoft, PBE)   } Ubuntu package
  vbc   : Si.pz-vbc.UPF (von Barth-Car norm-conserving, LDA)          } quantum-espresso-data
Absolute total energies of different pseudopotentials are NOT comparable;
only the convergence behaviour with ecutwfc is compared.
"""
import os
from ase import Atoms
from ase.calculators.espresso import Espresso, EspressoProfile

os.environ['OMP_NUM_THREADS'] = '1'
SYS_PP = '/usr/share/espresso/pseudo'
PPS = {
    'dojo-NC-PBE':   (os.path.abspath('.'), 'Si.upf', 4),
    'rrkjus-US-PBE': (SYS_PP, 'Si.pbe-nl-rrkjus_psl.1.0.0.UPF', 8),
    'vbc-NC-LDA':    (SYS_PP, 'Si.pz-vbc.UPF', 4),
}
ECUTS = [15, 20, 25, 30, 40, 50, 60, 80]
atoms = Atoms('Si2', positions=[[1.35745, 4.07235, 4.07235], [0.0, 0.0, 0.0]],
              cell=[[0.0, 2.7149, 2.7149], [2.7149, 0.0, 2.7149], [2.7149, 2.7149, 0.0]], pbc=True)
results = {}
for label, (pdir, pfile, ratio) in PPS.items():
    profile = EspressoProfile(command='mpirun -np 4 pw.x', pseudo_dir=pdir)
    results[label] = []
    for ec in ECUTS:
        atoms.calc = Espresso(profile=profile, directory=f'calc_{label}_{ec}',
            pseudopotentials={'Si': pfile},
            input_data={'control': {'calculation': 'scf', 'outdir': './tmp'},
                        'system': {'ecutwfc': ec, 'ecutrho': ratio * ec, 'occupations': 'smearing',
                                   'smearing': 'gauss', 'degauss': 0.01},
                        'electrons': {'conv_thr': 1e-10}},
            kpts=(2, 2, 2))
        results[label].append(atoms.get_potential_energy())
        print(f"done: {label} {ec} Ry", flush=True)
print("\nTotal energy E (eV) and E - E(80 Ry) (meV/atom); Si, k = 2x2x2")
head = f"{'ecutwfc/Ry':>10}" + "".join(f" | {l:^25}" for l in PPS)
print(head)
print("-" * len(head))
for i, ec in enumerate(ECUTS):
    row = f"{ec:10d}"
    for l in PPS:
        e = results[l][i]
        row += f" | {e:13.5f} {1000*(e-results[l][-1])/2:11.2f}"
    print(row)
for l in PPS:
    conv = next(ec for ec, e in zip(ECUTS, results[l]) if abs(1000*(e-results[l][-1])/2) < 1.0)
    print(f"{l}: converged to < 1 meV/atom at ecutwfc = {conv} Ry")
