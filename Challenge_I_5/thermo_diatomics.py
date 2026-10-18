"""Challenge I.5: thermodynamic properties of diatomic molecules with MACE-MP + ASE IdealGasThermo.
Extends N2_thermodyn_EMT_MACE_04.py (N2 only) to a loop over diatomics.
T = 298.15 K, p = 1 bar, ideal gas, rigid rotor, harmonic oscillator.
Experimental references: harmonic frequency w_e (cm-1) and standard entropy S0 (J/mol/K),
NIST Chemistry WebBook / CCCBDB.
"""
from ase import Atoms
from ase.optimize import BFGS
from ase.vibrations import Vibrations
from ase.thermochemistry import IdealGasThermo
from mace.calculators import mace_mp

T, P = 298.15, 1.0e5
EV_TO_J_MOL = 96485.33
# name: (A, B, d_init, spin (S), symmetry number, exp. w_e, exp. S0)
MOLECULES = {
    "H2":  ("H",  "H",  0.75, 0, 2, 4401.2, 130.68),
    "N2":  ("N",  "N",  1.10, 0, 2, 2358.6, 191.61),
    "O2":  ("O",  "O",  1.20, 1, 2, 1580.2, 205.15),
    "F2":  ("F",  "F",  1.40, 0, 2, 916.6, 202.79),
    "Cl2": ("Cl", "Cl", 2.00, 0, 2, 559.7, 223.08),
    "CO":  ("C",  "O",  1.13, 0, 1, 2169.8, 197.66),
    "HF":  ("H",  "F",  0.92, 0, 1, 4138.3, 173.78),
}
calc = mace_mp(model="medium", device="cpu", default_dtype="float64")
rows = []
for name, (a, b, d0, spin, sym, w_exp, s_exp) in MOLECULES.items():
    mol = Atoms(a + b, positions=[(0, 0, 0), (0, 0, d0)], calculator=calc)
    BFGS(mol, logfile=None).run(fmax=0.001, steps=300)
    vib = Vibrations(mol, name=f"vib_{name}")
    vib.clean()
    vib.run()
    vib_en = vib.get_energies()
    w = max(vib_en.real) * 8065.544
    thermo = IdealGasThermo(vib_energies=vib_en, potentialenergy=mol.get_potential_energy(),
                            atoms=mol, geometry="linear", symmetrynumber=sym, spin=spin,
                            ignore_imag_modes=True)
    zpe = thermo.get_ZPE_correction()
    H = thermo.get_enthalpy(T, verbose=False) - mol.get_potential_energy()
    S = thermo.get_entropy(T, P, verbose=False) * EV_TO_J_MOL
    G = thermo.get_gibbs_energy(T, P, verbose=False) - mol.get_potential_energy()
    rows.append((name, mol.get_distance(0, 1), w, w_exp, zpe, H, S, s_exp, G))
    print(f"done: {name}", flush=True)

print(f"\nT = {T} K, p = 1 bar; H and G are given relative to the electronic energy E_pot")
print(f"{'Mol':<4}| {'r/A':>6} | {'w_MACE':>7} {'w_exp':>7} {'err':>6} | {'ZPE/eV':>7} {'H-E/eV':>7} | {'S_MACE':>7} {'S_exp':>7} {'err':>6} | {'G-E/eV':>7}")
print("-" * 98)
for name, r, w, w_exp, zpe, H, S, s_exp, G in rows:
    print(f"{name:<4}| {r:6.3f} | {w:7.0f} {w_exp:7.0f} {100*(w-w_exp)/w_exp:+5.1f}% | {zpe:7.3f} {H:7.3f} | {S:7.2f} {s_exp:7.2f} {100*(S-s_exp)/s_exp:+5.1f}% | {G:7.3f}")
print("\nw in cm-1, S in J/(mol K).")
