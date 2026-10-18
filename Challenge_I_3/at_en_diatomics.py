"""Challenge I.3: atomization energies of diatomic molecules, EMT vs MACE-MP.
Extends at_en_mace_EMT_N2.py to a loop over several diatomics.
E_at = E(atom A) + E(atom B) - E(AB, optimized)
EMT is only defined for H, C, N, O (and some metals) -> 'N/A' otherwise.
Experimental values: D0 (eV) and r_e (Angstrom), NIST CCCBDB / CRC Handbook.
"""
from ase import Atoms
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from mace.calculators import mace_mp

MOLECULES = {
    "H2":  ("H",  "H",  0.75, 0.741, 4.478),
    "N2":  ("N",  "N",  1.10, 1.098, 9.759),
    "O2":  ("O",  "O",  1.20, 1.208, 5.117),
    "F2":  ("F",  "F",  1.40, 1.412, 1.602),
    "Cl2": ("Cl", "Cl", 2.00, 1.988, 2.479),
    "CO":  ("C",  "O",  1.13, 1.128, 11.09),
    "HF":  ("H",  "F",  0.92, 0.917, 5.869),
}
EMT_ELEMENTS = {"H", "C", "N", "O", "Al", "Cu", "Ag", "Au", "Ni", "Pd", "Pt"}
mace = mace_mp(model="medium", device="cpu", default_dtype="float64")

def atomization(a, b, d0, calc_factory):
    ea = Atoms(a, calculator=calc_factory()).get_potential_energy()
    eb = Atoms(b, calculator=calc_factory()).get_potential_energy()
    mol = Atoms(a + b, positions=[(0, 0, 0), (0, 0, d0)], calculator=calc_factory())
    BFGS(mol, logfile=None).run(fmax=0.01, steps=200)
    return mol.get_distance(0, 1), ea + eb - mol.get_potential_energy()

rows = []
for name, (a, b, d0, r_exp, e_exp) in MOLECULES.items():
    if a in EMT_ELEMENTS and b in EMT_ELEMENTS:
        r_emt, e_emt = atomization(a, b, d0, EMT)
    else:
        r_emt = e_emt = None
    r_mace, e_mace = atomization(a, b, d0, lambda: mace)
    rows.append((name, r_exp, r_emt, r_mace, e_exp, e_emt, e_mace))
    print(f"done: {name}", flush=True)

f = lambda x, p=3: "N/A" if x is None else f"{x:.{p}f}"
print()
print(f"{'Mol':<5}| {'r_exp':>6} {'r_EMT':>6} {'r_MACE':>7} | {'E_exp':>6} {'E_EMT':>7} {'E_MACE':>7} | {'err_MACE':>8}")
print("-" * 70)
for name, r_exp, r_emt, r_mace, e_exp, e_emt, e_mace in rows:
    err = 100 * (e_mace - e_exp) / e_exp
    print(f"{name:<5}| {r_exp:6.3f} {f(r_emt):>6} {r_mace:7.3f} | {e_exp:6.2f} {f(e_emt, 2):>7} {e_mace:7.2f} | {err:+7.1f}%")
print("\nr in Angstrom, E = atomization energy in eV (exp. = D0).")
