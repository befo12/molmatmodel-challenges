"""Challenge II.4: effect of the Gaussian broadening (degauss) on the DOS of Si.
Re-uses the NSCF wavefunctions (k = 30x30x30) written by electronic_properties_si.py
(prefix 'Si_Electronic', outdir './tmp') and runs dos.x for several degauss values.
Also plots TDOS/PDOS of the main run and computes the Kohn-Sham band gap."""
import os, re, subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
DEGAUSS = [0.002, 0.005, 0.01, 0.02, 0.05]   # Ry
RY = 13.605693
EXP_GAP = 1.12                               # eV, Si at 300 K (indirect)

def read_dos(fname):
    with open(fname) as f:
        ef = float(re.search(r'EFermi\s*=\s*([-\d.]+)', f.readline()).group(1))
    d = np.loadtxt(fname)
    return d[:, 0] - ef, d[:, 1], ef

def ks_gap_from_xml(xml='tmp/Si_Electronic.save/data-file-schema.xml'):
    import xml.etree.ElementTree as ET
    root = ET.parse(xml).getroot()
    nocc = int(round(float(next(el.text for el in root.iter() if el.tag.endswith('nelec'))) / 2))
    vbm, cbm = -1e9, 1e9
    for ks in root.iter():
        if ks.tag.endswith('ks_energies'):
            ev = next(c for c in ks if c.tag.endswith('eigenvalues'))
            eig = np.array(ev.text.split(), float) * 27.211386
            vbm, cbm = max(vbm, eig[nocc - 1]), min(cbm, eig[nocc])
    return vbm, cbm, cbm - vbm

def gap_from_dos(e, dos, thr=1e-2):
    m = (e > -2) & (e < 3)
    e, low = e[m], dos[m] < thr
    best, start = (0.0, None, None), None
    for i, flag in enumerate(low):
        if flag and start is None:
            start = i
        if (not flag or i == len(low) - 1) and start is not None:
            end = i if flag else i - 1
            if e[end] - e[start] > best[0]:
                best = (e[end] - e[start], e[start], e[end])
            start = None
    return best

def style(ax):
    for s in ax.spines.values():
        s.set_visible(True); s.set_color('black')
    ax.tick_params(colors='black', direction='in', top=True, right=True)

os.makedirs('degauss_test', exist_ok=True)
for dg in DEGAUSS:
    out = f'degauss_test/dos_dg{dg}.dat'
    with open('dos_tmp.in', 'w') as f:
        f.write(f"&DOS\n  prefix='Si_Electronic', outdir='./tmp', DeltaE=0.01, Emin=-20.0, Emax=20.0,\n"
                f"  ngauss=0, degauss={dg}, fildos='{out}'\n/\n")
    with open('dos_tmp.in') as fin, open(f'degauss_test/dos_dg{dg}.out', 'w') as fout:
        subprocess.run(['dos.x'], stdin=fin, stdout=fout, stderr=subprocess.STDOUT, check=True)
    os.replace('dos_tmp.in', f'degauss_test/dos_dg{dg}.in')

print(f"{'degauss/Ry':>10} {'sigma/eV':>9} {'gap in DOS/eV':>14} {'VBM-EF/eV':>10} {'CBM-EF/eV':>10}")
fig, ax = plt.subplots(figsize=(6.5, 4.2))
for dg, c in zip(DEGAUSS, ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']):
    e, dos, ef = read_dos(f'degauss_test/dos_dg{dg}.dat')
    g, lo, hi = gap_from_dos(e, dos)
    if lo is None:
        print(f"{dg:10.3f} {dg*RY:9.3f} {'closed':>14} {'-':>10} {'-':>10}")
    else:
        print(f"{dg:10.3f} {dg*RY:9.3f} {g:14.2f} {lo:10.2f} {hi:10.2f}")
    ax.plot(e, dos, color=c, lw=1.2, label=f'degauss = {dg} Ry')
print("(gap in DOS = width of the region with DOS < 0.01 states/eV around E_F)")
try:
    vbm, cbm, g = ks_gap_from_xml()
    print(f"Kohn-Sham (PBE) band gap from NSCF eigenvalues: {g:.3f} eV  (VBM {vbm:.3f} eV, CBM {cbm:.3f} eV)")
except Exception as err:
    print(f"Could not read eigenvalues from the XML file: {err}")
print(f"Experimental band gap of Si: {EXP_GAP} eV (indirect)")
ax.set_xlim(-13, 5); ax.set_ylim(bottom=0)
ax.set_xlabel(r'$E - E_\mathrm{F}$ (eV)', color='black'); ax.set_ylabel('DOS (states/eV)', color='black')
ax.axvline(0, color='black', lw=0.8, ls='--'); style(ax)
ax.legend(loc='upper left', frameon=True, framealpha=1, edgecolor='black', fancybox=False, fontsize=8)
fig.tight_layout(); fig.savefig('degauss_test/dos_vs_degauss.png', dpi=200)

e, dos, ef = read_dos('total_dos.dat')
pt = np.loadtxt('pdos_results/pdos.pdos_tot')
ps = np.loadtxt('pdos_results/pdos.pdos_atm#1(Si)_wfc#1(s)')
pp = np.loadtxt('pdos_results/pdos.pdos_atm#1(Si)_wfc#2(p)')
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(e, dos, color='black', lw=1.4, label='total DOS (dos.x)')
ax.plot(pt[:, 0] - ef, pt[:, 2], color='#1f77b4', lw=1.0, ls='--', label='sum of PDOS')
ax.plot(ps[:, 0] - ef, ps[:, 1], color='#d62728', lw=1.2, label='Si(1) s')
ax.plot(pp[:, 0] - ef, pp[:, 1], color='#2ca02c', lw=1.2, label='Si(1) p')
ax.axvline(0, color='black', lw=0.8, ls=':')
ax.set_xlim(-13, 5); ax.set_ylim(bottom=0)
ax.set_xlabel(r'$E - E_\mathrm{F}$ (eV)', color='black'); ax.set_ylabel('DOS (states/eV)', color='black')
style(ax)
ax.legend(loc='upper left', frameon=True, framealpha=1, edgecolor='black', fancybox=False, fontsize=8)
fig.tight_layout(); fig.savefig('dos_pdos_si.png', dpi=200)
print("Figures: dos_pdos_si.png, degauss_test/dos_vs_degauss.png")
