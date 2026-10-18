"""Challenge I.6: C-H bond dissociation energy of methane, CH4 -> CH3. + H.
Modified from ethane_CC_bond_en_EMT_MACE_01.py (Exercise I.6).
D_e = E(CH3) + E(H) - E(CH4)          (electronic, from optimized structures)
D_0 = D_e - [ZPE(CH4) - ZPE(CH3)]     (zero-point corrected, MACE only)
Experiment: D_0(CH3-H) = 432.7 kJ/mol (4.48 eV), D_298 = 439.3 kJ/mol;
r(C-H) in CH4 = 1.087 A.  (Ruscic et al., NIST/ATcT; CRC Handbook)
"""
from ase import Atoms
from ase.build import molecule
from ase.optimize import BFGS
from ase.calculators.emt import EMT
from ase.vibrations import Vibrations
from mace.calculators import mace_mp

EV = 96.485
EXP_D0, EXP_R = 432.7, 1.087

def relax(atoms, calc, name):
    atoms.calc = calc
    BFGS(atoms, trajectory=f"{name}.traj", logfile=None).run(fmax=0.001, steps=500)
    return atoms.get_potential_energy()

def zpe(atoms, name):
    vib = Vibrations(atoms, name=f"vib_{name}")
    vib.clean()
    vib.run()
    return vib.get_zero_point_energy()

results = {}
for label, calc in [("EMT", EMT()),
                    ("MACE", mace_mp(model="medium", device="cpu", default_dtype="float64"))]:
    ch4, ch3 = molecule("CH4"), molecule("CH3")
    h = Atoms("H")
    e_ch4 = relax(ch4, calc, f"ch4_{label}")
    e_ch3 = relax(ch3, calc, f"ch3_{label}")
    h.calc = calc
    e_h = h.get_potential_energy()
    De = e_ch3 + e_h - e_ch4
    r_ch = ch4.get_distance(0, 1)
    D0 = None
    if label == "MACE":
        dzpe = zpe(ch4, f"ch4_{label}") - zpe(ch3, f"ch3_{label}")
        D0 = De - dzpe
        print(f"MACE: ZPE(CH4) - ZPE(CH3) = {dzpe:.3f} eV")
    results[label] = (r_ch, De, D0)
    print(f"{label}: E(CH4) = {e_ch4:.4f}  E(CH3) = {e_ch3:.4f}  E(H) = {e_h:.4f} eV")

print("\n" + "=" * 66)
print("C-H BOND IN METHANE:  CH4 -> CH3. + H.")
print("=" * 66)
print(f"{'Method':<8}{'r(C-H)/A':>10}{'D_e/eV':>10}{'D_e kJ/mol':>12}{'D_0 kJ/mol':>12}{'err D':>9}")
print("-" * 66)
for label, (r, De, D0) in results.items():
    D = D0 if D0 is not None else De
    d0s = f"{D0*EV:12.1f}" if D0 is not None else f"{'-':>12}"
    print(f"{label:<8}{r:10.3f}{De:10.3f}{De*EV:12.1f}{d0s}{100*(D*EV-EXP_D0)/EXP_D0:+8.1f}%")
print(f"{'Exp.':<8}{EXP_R:10.3f}{'':>10}{'':>12}{EXP_D0:12.1f}")
print("-" * 66)
print("err D: D_0 vs experiment for MACE, D_e vs experimental D_0 for EMT.")
