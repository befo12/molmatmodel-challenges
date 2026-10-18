=============================================================================
Challenge II.8 - Adsorption on graphene: H on C8/C18 and Hg on C18 (ASE + QE)
=============================================================================

Status
------
* ``H_on_C8/`` - course calculations reproduced; all H challenges done except that the last
  relaxation (H on C18) was interrupted after 12 BFGS steps (see below).
* ``Hg_on_C18/`` - inputs for the three adsorption sites are prepared (``run_hg_sites.sh``),
  but **not yet run**: my notebook shut down (overheating) and froze repeatedly under
  sustained DFT load, so these relaxations will be completed later on a more suitable machine.

Part 1 - H on graphene (``H_on_C8/``)
--------------------------------------
Course protocol (``course_relaxation/``, ``course_energy_h/``, ``course_energy_c/``; PBE + DFT-D3,
ecutwfc 80 Ry, Gamma point, nspin = 2) reproduces the reference binding energy exactly::

    E(C8)=-1303.645873  E(H)=-12.559509  E(H@C8)=-1319.069282  ->  E_b = 2.8639 eV (course reference 2.8639 eV)

Challenges: ``h_adsorption_challenges.py`` (driver; all runs in ``runs/<step>/``) and
``h_results_from_outputs.py`` (collects the energies from the QE outputs; output
``h_results_from_outputs.py.log``):

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
    C18, spin (not converged)          2.838     1.109         0.509
    
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
* H on C18: the relaxation stopped at fmax = 0.12 eV/A (target 0.01), so 2.84 eV is not final;
  the energy was still decreasing by ~10 meV per step, i.e. the converged E_b will be slightly
  larger.
* Even with correct spin, E_b depends strongly on the cell (2.13 eV for C8 vs >= 2.84 eV for C18)
  and is much larger than literature values for an isolated H on graphene (~0.7-0.9 eV with PBE in large
  supercells). The main reason is the Gamma-point-only sampling of small periodic cells: as shown in
  Challenge II.6, a 2x2 cell sampled at Gamma does not contain the Dirac point K, while a 3x3 cell
  does (K folds onto Gamma), so the electronic structure of the clean and the H-covered graphene is
  described very differently. Converged values need larger supercells and a k-point grid divisible
  by 3 (e.g. 6x6x1 for the 2x2 cell) - planned as a follow-up.

Part 2 - Hg on C18 (``Hg_on_C18/``) - prepared, not yet run
-----------------------------------------------------------
Course reference (on-top site): E_ads = -0.24 eV. Inputs for the challenge (on-top, bridge, hollow):
initial Hg position 3.4 A above the slab at

* on-top: above a C atom (``c18_hg.vasp``, course),
* bridge: above the middle of a C-C bond (``site_bridge/c18_hg.vasp``),
* hollow: above the centre of a hexagon (``site_hollow/c18_hg.vasp``),

with the course settings unchanged (``relaxation_Hg_C18.py``). ``bash run_hg_sites.sh`` runs the
course single points (C18, Hg), the three relaxations and ``hg_sites_summary.py``, which reports
E_ads = E(Hg@C18) - E(C18) - E(Hg), the Hg height, the shortest Hg-C distance and how far the Hg
atom moved laterally during the relaxation. ``hg_sites_summary.py`` was checked on the course
reference output (on-top: E_ads = -0.238 eV).
