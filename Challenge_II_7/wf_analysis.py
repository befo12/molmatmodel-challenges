"""Challenge II.7: work function of graphene, with and without assume_isolated = '2D'.
Vacuum level = mean planar-averaged electrostatic potential 3.5-5.0 A away from the graphene
layer (z = 7.5 A), where the potential is flat; W = V_vac - E_F.
Literature: graphene W(exp) ~ 4.5-4.6 eV (Kelvin probe / photoemission), PBE ~ 4.2-4.3 eV."""
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BOHR, RY, Z0 = 0.529177, 13.605693, 7.5
RUNS = {'with assume_isolated = 2D': 'with_2D', 'without assume_isolated': 'no_2D'}
COLORS = {'with_2D': '#d62728', 'no_2D': '#1f77b4'}

def style(ax):
    for s in ax.spines.values():
        s.set_visible(True); s.set_color('black')
    ax.tick_params(colors='black', direction='in', top=True, right=True)

fig, ax = plt.subplots(figsize=(7, 4.4))
print(f"{'Run':<28}{'E_F/eV':>9}{'V_vac/eV':>10}{'W/eV':>8}{'V(z=0)/eV':>11}")
print('-' * 66)
for name, d in RUNS.items():
    ef = float(re.search(r'Fermi level:\s*([-\d.]+)', open(f'{d}/work_function.out').read()).group(1))
    a = np.loadtxt(f'{d}/potential_results/avg.dat')
    z, vp, vm = a[:, 0] * BOHR, a[:, 1] * RY, a[:, 2] * RY
    win = (np.abs(z - Z0) >= 3.5) & (np.abs(z - Z0) <= 5.0)
    vvac = vp[win].mean()
    print(f"{name:<28}{ef:9.4f}{vvac:10.4f}{vvac-ef:8.3f}{vp[0]:11.3f}")
    c = COLORS[d]
    ax.plot(z, vp, color=c, lw=1.3, label=f'planar average, {name}')
    ax.plot(z, vm, color=c, lw=1.0, ls='--', label=f'macroscopic average, {name}')
    ax.axhline(ef, color=c, lw=0.9, ls=':')
    ax.text(0.3, ef + 0.6, f'$E_F$ = {ef:.2f} eV' + (' (2D)' if d == 'with_2D' else ''), color=c, fontsize=8)
ax.set_xlim(0, 15); ax.set_ylim(-20, 16)
ax.set_xlabel('z (A)', color='black'); ax.set_ylabel('electrostatic potential (eV)', color='black')
style(ax)
ax.legend(loc='lower right', frameon=True, framealpha=1, edgecolor='black', fancybox=False, fontsize=7)
fig.tight_layout(); fig.savefig('work_function_comparison.png', dpi=200)
print("\nLiterature: graphene W ~ 4.5-4.6 eV (experiment), ~4.2-4.3 eV (PBE)")
print("Figure: work_function_comparison.png")
