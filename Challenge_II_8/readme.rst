=============================================================================
Challenge II.8 - Adsorption on graphene: H on C8/C18 and Hg on C18 (ASE + QE)
=============================================================================

Task
----
Adsorption on graphene. Challenges (course ``readme.rst`` files):

* H on C8: "Modify the Python script to perform the relaxation of the C8 slab and calculate the new
  adsorption energy. Likewise, increase the ecutwfc parameter to see if this improves the binding
  energy of H on C8. Enlarge the slab to C18 as for the Hg atom adsorption, and compute the
  adsorption energy."
* Hg on C18: "Calculate the adsorption energy of Hg on 3 different adsorption sites of the C18 slab:
  on-top, on-bridge, on-hollow."

Status
------
* ``H_on_C8/`` - course calculations reproduced; all H challenges done (the H on C18 relaxation
  was interrupted once and later resumed from its trajectory to fmax < 0.01 eV/A).
* ``Hg_on_C18/`` - all three adsorption sites done (on-top, bridge, hollow). A follow-up test of the
  graphene distortion found at the bridge and hollow sites is prepared (``kekule_check.sh``), not yet run.

Part 1 - H on graphene (``H_on_C8/``)
--------------------------------------
Course protocol (``course_relaxation/``, ``course_energy_h/``, ``course_energy_c/``; PBE + DFT-D3,
ecutwfc 80 Ry, Gamma point, nspin = 2) reproduces the reference binding energy exactly::

    E(C8)=-1303.645873  E(H)=-12.559509  E(H@C8)=-1319.069282  ->  E_b = 2.8639 eV (course reference 2.8639 eV)

Challenges: ``h_adsorption_challenges.py`` (driver; all runs in ``runs/<step>/``; it re-uses
finished steps and resumes an interrupted relaxation from its trajectory; final output
``resume.log``). ``h_results_from_outputs.py`` collects the energies directly from the QE outputs
(written while the C18 run was still unfinished; output ``h_results_from_outputs.py.log``):

1. relaxation of the clean C8 slab,
2. (extra) correct spin polarization of the H atom and of H@C8,
3. ecutwfc = 100 and 120 Ry,
4. a larger slab, C18 (3x3 graphene cell), as used for Hg.

E_b = E(slab) + E(H) - E(H@slab)::

    Model                           E_b (eV)   C-H (A)  C pucker (A)
    ----------------------------------------------------------------
    C8, course protocol                2.864     1.102         0.421
    C8 relaxed slab                    2.864     1.102         0.421
    C8 relaxed, spin-polarized         2.126     1.098         0.424
    C8, spin, ecutwfc 100 Ry           2.126     1.098         0.424
    C8, spin, ecutwfc 120 Ry           2.126     1.098         0.424
    C18, spin-polarized                2.841     1.111         0.509
    
    'C pucker' = height of the C atom bonded to H above the mean plane of the other C atoms
    Spin-polarization energy of the isolated H atom: 1.038 eV
    Energy change on relaxing the clean C8 slab: 0.00 meV
    Magnetic moment: H atom 1.00 muB, H@C8 1.00 muB (spin-polarized runs), see runs/*/espresso.pwo

Discussion
----------
* Relaxing the clean C8 slab changes nothing (0.00 meV): it is already ideal graphene with the
  relaxed lattice constant of Challenge II.6.
* Spin polarization: in the course scripts ``nspin = 2`` is set but no starting magnetization,
  so QE converges to a *non-magnetic* H atom (total magnetization 0.00). An isolated H atom has one
  unpaired electron; with a starting moment the H atom becomes fully polarized (1.00 muB) and its
  energy drops by 1.04 eV (E = -13.597 eV, close to the exact -13.606 eV). H@C8 also carries
  1 muB (the sp3 defect leaves an unpaired pi electron). The consistent spin-polarized binding
  energy is 2.13 eV instead of 2.86 eV: the course value overestimates E_b by 0.74 eV.
* ecutwfc: 80 Ry is converged - E_b is unchanged (< 1 meV) at 100 and 120 Ry.
* Geometry: H binds on top of a C atom (C-H = 1.10 A), which is pulled out of the plane by
  ~0.42 A (C8) / ~0.51 A (C18): rehybridization from sp2 to sp3 (chemisorption).
* H on C18: the first run stopped at fmax = 0.12 eV/A (E_b = 2.838 eV); resumed to
  fmax < 0.01 eV/A it gives E_b = 2.841 eV (E(H@C18) = -2963.759057 eV), i.e. the last part of
  the relaxation changed E_b by only 3 meV.
* Even with correct spin, E_b depends strongly on the cell (2.13 eV for C8 vs 2.84 eV for C18)
  and is much larger than literature values for an isolated H on graphene (~0.7-0.9 eV with PBE in large
  supercells). The main reason is the Gamma-point-only sampling of small periodic cells: as shown in
  Challenge II.6, a 2x2 cell sampled at Gamma does not contain the Dirac point K, while a 3x3 cell
  does (K folds onto Gamma), so the electronic structure of the clean and the H-covered graphene is
  described very differently. Converged values need larger supercells and a k-point grid divisible
  by 3 (e.g. 6x6x1 for the 2x2 cell) - planned as a follow-up.

Part 2 - Hg on C18 (``Hg_on_C18/``)
-----------------------------------
Course reference (on-top site): E_ads = -0.24 eV. Challenge: on-top, bridge and hollow sites,
initial Hg position 3.4 A above the slab at

* on-top: above a C atom (``c18_hg.vasp``, course),
* bridge: above the middle of a C-C bond (``site_bridge/c18_hg.vasp``),
* hollow: above the centre of a hexagon (``site_hollow/c18_hg.vasp``),

with the course settings unchanged (``relaxation_Hg_C18.py``: PBE + DFT-D3, 80 Ry, Gamma point,
Gaussian smearing 0.01 Ry, no atoms fixed, BFGS to fmax < 0.01 eV/A). ``bash run_hg_sites.sh`` runs
the course single points (C18, Hg), the three relaxations and ``hg_sites_summary.py``
(output ``hg_sites_summary.log``)::

    E(C18) = -2947.320598 eV, E(Hg) = -4533.787985 eV

    start      E(Hg@C18)/eV  E_ads/eV  kJ/mol  h(Hg)/A  d(Hg-C)/A   final  C-C min/max (A)  dE relax/eV  steps
    ----------------------------------------------------------------------------------------------------------
    top        -7481.346431    -0.238   -22.9    3.410      3.428     top    1.425/1.425       -0.001      7
    bridge     -7481.618851    -0.510   -49.2    3.421      3.510  bridge    1.402/1.472       -0.273    113
    hollow     -7481.774037    -0.665   -64.2    3.400      3.676  hollow    1.395/1.484       -0.426      8

    h(Hg) = height of Hg above the mean C plane; d(Hg-C) = shortest Hg-C distance;
    final = site from the nearest-C pattern; dE relax = E(last) - E(first BFGS step)

The on-top result is identical to the course reference (E = -7481.346431 eV, E_ads = -0.238 eV).

Discussion
~~~~~~~~~~
* All three sites stay where they started (nearest-C pattern 1 / 2 / 6 atoms) and Hg stays
  ~3.4 A above the sheet: physisorption, as expected for the closed-shell Hg atom.
* At the start of the relaxations (flat graphene, Hg at 3.4 A) the three sites have almost the
  same energy: -7481.3455 (top), -7481.3458 (bridge) and -7481.3485 eV (hollow), i.e. the
  site preference of Hg itself is only ~3 meV, typical of a flat dispersion-dominated potential.
* The large differences of the final E_ads (-0.24, -0.51, -0.67 eV) come entirely from the
  relaxation of the graphene sheet, not from Hg: at the bridge and hollow sites the C-C bonds split
  into short (1.40 A) and long (1.47-1.48 A) bonds (ideal graphene: 1.425 A), a Kekule-type bond
  alternation, lowering the energy by 0.27 and 0.43 eV. At the on-top site the sheet stays ideal
  (the optimizer stops after 7 steps with small forces); this symmetric structure may be a saddle
  point that a small perturbation would also lead to a distorted sheet.
* This is most likely an artefact of the course settings, not physics: in a 3x3 graphene cell the
  Dirac points K and K' fold onto Gamma (Challenge II.6), so a Gamma-only calculation with a small
  smearing has degenerate states exactly at E_F. A Kekule distortion couples K and K' and opens a
  gap, which lowers the energy of this artificial model; real graphene (dense k-sampling) is stable
  against it. An adsorbate that breaks the symmetry (bridge, hollow) lets BFGS find this path.
  Consistent with this, the bridge relaxation needed 113 steps on a very flat energy surface.
* Test prepared in ``kekule_check.sh``: single points of the relaxed bridge / hollow graphene
  without Hg. If these are ~0.3-0.4 eV below the flat C18, the energy gain is a property of the
  distorted sheet. A physically meaningful site comparison needs a denser k-grid (e.g. 6x6x1 or
  9x9x1 for the 3x3 cell) or a larger supercell; with flat graphene the site differences of Hg are
  only a few meV.
* The same Gamma-only caveat applies to H on C18 in Part 1. There the final sheet shows the
  expected sp3 elongation of the three C-C bonds at the H-bonded C (1.50 A) and no clear Kekule
  pattern (other bonds 1.41-1.43 A), but the binding energy is still affected by the k-sampling.
