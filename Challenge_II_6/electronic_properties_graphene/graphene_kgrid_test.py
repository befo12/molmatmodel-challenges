"""Challenge II.6: graphene DOS with k-grids lower than the converged one (12, 18 and the 'even'
20x20x1) compared with the converged run (SCF 42x42x1 / NSCF 66x66x1, this directory).
For every grid the course script is re-run with scf_kpts = nscf_kpts = (k, k, 1) in kgrid_k/.
From the NSCF data of each run: E_F, DOS at E_F, Kohn-Sham eigenvalues at Gamma (bands 3-6)
relative to E_F, and the smallest direct pi-pi* gap over all k-points (0 only if the grid
contains the Dirac point K = (1/3, 1/3, 0)). Figures: dos_vs_kgrid.png, pdos_p_orbitals_graphene_vs_si.png"""
import os, re, subprocess
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
GRIDS = [12, 18, 20]
HA = 27.211386
SI_PDOS = os.path.expanduser('~/challenges/Challenge_II_4/pdos_results/pdos.pdos_atm#1(Si)_wfc#2(p)')
SI_DOS = os.path.expanduser('~/challenges/Challenge_II_4/total_dos.dat')

def style(ax):
    for s in ax.spines.values():
        s.set_visible(True); s.set_color('black')
    ax.tick_params(colors='black', direction='in', top=True, right=True)

def fermi(dos_file):
    with open(dos_file) as f:
        return float(re.search(r'EFermi\s*=\s*([-\d.]+)', f.readline()).group(1))

def analyse(d):
    ef = fermi(f'{d}/total_dos.dat')
    dos = np.loadtxt(f'{d}/total_dos.dat')
    res = {'ef': ef, 'dos_ef': np.interp(ef, dos[:, 0], dos[:, 1]), 'gamma': None, 'gap': None, 'nk': None}
    xml = f'{d}/tmp/graphene.save/data-file-schema.xml'
    if os.path.exists(xml):
        root = ET.parse(xml).getroot()
        nocc = int(round(float(next(el.text for el in root.iter() if el.tag.endswith('nelec'))) / 2))
        gaps, nk = [], 0
        for ks in root.iter():
            if not ks.tag.endswith('ks_energies'):
                continue
            nk += 1
            kpt = np.array(next(c for c in ks if c.tag.endswith('k_point')).text.split(), float)
            eig = np.array(next(c for c in ks if c.tag.endswith('eigenvalues')).text.split(), float) * HA
            gaps.append(eig[nocc] - eig[nocc - 1])
            if np.linalg.norm(kpt) < 1e-6:
                res['gamma'] = eig[nocc - 2:nocc + 2] - ef
        res['gap'], res['nk'] = min(gaps), nk
    return res

src = open('electronic_properties_graphene.py').read()
for k in GRIDS:
    d = f'kgrid_{k}'
    if os.path.exists(f'{d}/total_dos.dat'):
        continue
    os.makedirs(d, exist_ok=True)
    s = src.replace('scf_kpts = (42,42,1)', f'scf_kpts = ({k},{k},1)').replace('nscf_kpts = (66, 66, 1)', f'nscf_kpts = ({k}, {k}, 1)')
    open(f'{d}/electronic_properties_graphene_k{k}.py', 'w').write(s)
    print(f'running k = {k}x{k}x1 ...', flush=True)
    subprocess.run(f'cp C.upf {d}/ && cd {d} && python electronic_properties_graphene_k{k}.py > electronic_properties_graphene_k{k}.out 2>&1', shell=True, check=True)

runs = [(f'{k}x{k}x1', f'kgrid_{k}') for k in GRIDS] + [('42x42x1 / 66x66x1 (conv.)', '.')]
print(f"\n{'k-grid (SCF / NSCF)':<26}{'E_F/eV':>9}{'DOS(E_F)':>10}{'min pi-pi* gap/eV':>19}{'#k':>6}   Gamma: bands 3-6 relative to E_F (eV)")
print('-' * 110)
results = {}
for name, d in runs:
    r = analyse(d)
    results[name] = (d, r)
    gam = ('  '.join(f'{x:7.3f}' for x in r['gamma'])) if r['gamma'] is not None else 'n/a'
    gap = f"{r['gap']:19.3f}" if r['gap'] is not None else f"{'n/a':>19}"
    nk = f"{r['nk']:6d}" if r['nk'] else f"{'-':>6}"
    print(f"{name:<26}{r['ef']:9.3f}{r['dos_ef']:10.4f}{gap}{nk}   {gam}")

fig, ax = plt.subplots(figsize=(6.5, 4.2))
for (name, (d, r)), c in zip(results.items(), ['#d62728', '#ff7f0e', '#9467bd', 'black']):
    dos = np.loadtxt(f'{d}/total_dos.dat')
    ax.plot(dos[:, 0] - r['ef'], dos[:, 1], color=c, lw=1.4 if d == '.' else 1.0, label=name)
ax.axvline(0, color='black', lw=0.8, ls=':')
ax.set_xlim(-3, 3); ax.set_ylim(0, 0.6)
ax.set_xlabel(r'$E - E_\mathrm{F}$ (eV)', color='black'); ax.set_ylabel('DOS (states/eV)', color='black')
style(ax)
ax.legend(loc='upper center', frameon=True, framealpha=1, edgecolor='black', fancybox=False, fontsize=8)
fig.tight_layout(); fig.savefig('dos_vs_kgrid.png', dpi=200)

ef_g = fermi('total_dos.dat')
g = np.loadtxt('pdos_results/pdos.pdos_atm#1(C)_wfc#2(p)')
fig, axes = plt.subplots(1, 2, figsize=(10, 4.0))
axes[0].plot(g[:, 0] - ef_g, g[:, 2], color='#d62728', lw=1.3, label=r'C $p_z$')
axes[0].plot(g[:, 0] - ef_g, g[:, 3], color='#1f77b4', lw=1.1, label=r'C $p_x$')
axes[0].plot(g[:, 0] - ef_g, g[:, 4], color='#2ca02c', lw=1.1, ls='--', label=r'C $p_y$')
axes[0].set_title('graphene', color='black', fontsize=10)
if os.path.exists(SI_PDOS):
    ef_s = fermi(SI_DOS)
    s = np.loadtxt(SI_PDOS)
    axes[1].plot(s[:, 0] - ef_s, s[:, 2], color='#d62728', lw=1.3, label=r'Si $p_z$')
    axes[1].plot(s[:, 0] - ef_s, s[:, 3], color='#1f77b4', lw=1.1, label=r'Si $p_x$')
    axes[1].plot(s[:, 0] - ef_s, s[:, 4], color='#2ca02c', lw=1.1, ls='--', label=r'Si $p_y$')
axes[1].set_title('Si (Challenge II.4)', color='black', fontsize=10)
for ax in axes:
    ax.axvline(0, color='black', lw=0.8, ls=':')
    ax.set_xlim(-10, 5); ax.set_ylim(bottom=0)
    ax.set_xlabel(r'$E - E_\mathrm{F}$ (eV)', color='black'); ax.set_ylabel('PDOS (states/eV)', color='black')
    style(ax)
    ax.legend(loc='upper left', frameon=True, framealpha=1, edgecolor='black', fancybox=False, fontsize=8)
fig.tight_layout(); fig.savefig('pdos_p_orbitals_graphene_vs_si.png', dpi=200)
print('\nFigures: dos_vs_kgrid.png, pdos_p_orbitals_graphene_vs_si.png')
