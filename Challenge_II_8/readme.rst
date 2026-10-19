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
* ``Hg_on_C18/`` - all three adsorption sites done (on-top, bridge, hollow).
* Extra (follow-up): the Gamma-point-only sampling of the course scripts was found to distort both
  results. Both were recomputed with k-point sampling: H on graphene now agrees with the literature
  (E_b = 0.83-0.84 eV), and the large Hg site differences turned out to be an artefact (all three
  sites -0.19 to -0.20 eV). MACE foundation models were compared with the DFT results for Hg.

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
  described very differently. This is tested in the follow-up below.

Follow-up: H on graphene with k-point sampling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``h_kpoint_followup.py`` (output ``h_kpoint_followup.py.log``, runs in ``kfollow/``): same settings
(PBE + DFT-D3, 80 Ry, Gaussian 0.01 Ry, spin-polarized, starting moment 1 muB on H), H and all C atoms
relaxed with pw.x (``calculation = 'relax'``, force threshold 0.01 eV/A) starting from the Gamma
geometries. k-grids: 6x6x1 for the 2x2 cell (C8), as in Casolo et al., J. Chem. Phys. 130, 054704
(2009) (course folder ``casolo2009.pdf``), and 4x4x1 for the 3x3 cell (C18, same k-point density).
E(H atom, spin) = -13.597248 eV::

    cell         k-grid   E_b/eV   C-H/A  pucker/A   m/muB   Casolo 2009 (PBE, 6x6x1)
    C8 (2x2)     6x6x1     0.828   1.128     0.333    1.00   0.75 eV, 0.36 A
    C18 (3x3)    4x4x1     0.844   1.126     0.403    1.02   0.77 eV, 0.42 A
    C8 (2x2)     Gamma     2.126   1.098     0.424    1.00
    C18 (3x3)    Gamma     2.545   1.111     0.509    0.00

* With k-points the binding energy drops from 2.1-2.8 eV to 0.83-0.84 eV and agrees with the
  literature PBE values (0.75 / 0.77 eV); the remaining ~0.07 eV is consistent with the DFT-D3
  dispersion included here but not in the PBE literature values. The geometry (C-H 1.13 A, pucker
  0.33 / 0.40 A) also agrees, and the cell-size dependence nearly disappears (16 meV between the
  2x2 and 3x3 cells, as in the literature), instead of 0.4-0.7 eV with Gamma only.
* The Gamma-only description is not even unique: for H@C18 the pw.x relaxation (Gamma, started from
  the earlier Gamma geometry) converged to a non-magnetic solution (m = 0.00, E_b = 2.545 eV), while
  the earlier ASE relaxation had found a magnetic one (E_b = 2.841 eV). With the Dirac states folded
  onto Gamma, several self-consistent solutions exist; with k-points the expected moment of 1 muB is
  obtained in both cells.
* Conclusion: the course values of E_b (2.86 eV, and 2.13 / 2.84 eV with correct spin) are
  artefacts of the Gamma-point sampling of small graphene cells; the converged value for this setup
  is E_b = 0.83-0.84 eV.

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
* This is an artefact of the course settings, not physics (confirmed below): in a 3x3 graphene cell the
  Dirac points K and K' fold onto Gamma (Challenge II.6), so a Gamma-only calculation with a small
  smearing has degenerate states exactly at E_F. A Kekule distortion couples K and K' and opens a
  gap, which lowers the energy of this artificial model; real graphene (dense k-sampling) is stable
  against it. An adsorbate that breaks the symmetry (bridge, hollow) lets BFGS find this path.
  Consistent with this, the bridge relaxation needed 113 steps on a very flat energy surface.
* The same Gamma-only caveat applies to H on C18 in Part 1 (see the follow-up there).

Follow-up 1: the distorted graphene without Hg (``kekule_check.sh``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Single points (course settings, Gamma) of the relaxed bridge / hollow structures with the Hg atom
removed (``kekule_bridge/``, ``kekule_hollow/``; output ``kekule_check.log``)::

    flat C18 (course)          E = -2947.320598 eV
    C18 from bridge  (no Hg)   E = -2947.592411 eV   E - E(flat) = -0.272 eV
    C18 from hollow  (no Hg)   E = -2947.740349 eV   E - E(flat) = -0.420 eV

The bare distorted sheets are lower in energy by 0.272 / 0.420 eV, i.e. by the same amount as the
energy gained in the Hg relaxations (0.273 / 0.426 eV). The extra "binding" at the bridge and hollow
sites is therefore a property of the graphene sheet in this Gamma-only model, not of Hg.

Follow-up 2: k-point sampling (``hg_kpoint_followup.py``, helper ``qe_k.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Same course settings with k-grids 1x1x1 (Gamma), 3x3x1 and 6x6x1 (output
``hg_kpoint_followup.py.log``, runs in ``kfollow/``): flat graphene with Hg 3.4 A above each site
(the start structures), the Gamma-relaxed (distorted) structures with and without Hg, and flat C18
and the Hg atom as references (E_ads in eV)::

    k-grid   E_ads flat graphene:        E_dist (distorted - flat):  E_ads Gamma-relaxed:
             top     bridge  hollow      bridge   hollow             bridge   hollow
    1x1x1    -0.237  -0.237  -0.240      -0.272   -0.420             -0.510   -0.665
    3x3x1    -0.194  -0.195  -0.202      +0.423   +0.473             +0.226   +0.271
    6x6x1    -0.194  -0.195  -0.202      +0.487   +0.538             +0.290   +0.337

* With k-points the Kekule distortion costs +0.49 / +0.54 eV instead of gaining energy: real
  graphene is stable against it, as expected. The Gamma-relaxed bridge / hollow structures are not
  even bound with k-points (E_ads > 0).
* On flat graphene the three sites differ by only 8 meV (hollow slightly preferred) and the result
  is converged with k (3x3x1 and 6x6x1 agree within 0.2 meV): Hg is physisorbed with
  E_ads = -0.19 to -0.20 eV, essentially site-independent. The course on-top value (-0.24 eV) is
  close; the Gamma values for bridge and hollow (-0.51, -0.67 eV) are artefacts.
* A full relaxation with k-points was not done; since Hg hardly perturbs flat graphene (Gamma, on-top:
  0.001 eV relaxation energy), the flat-graphene values are a good estimate.

Follow-up 3: MACE foundation models vs DFT (``hg_mace_sites.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Same structures with MACE-MP medium and MACE-MPA-0 medium (mace-torch 0.3.16). These models are
trained on PBE data without dispersion, so each is also run with the same D3(BJ) correction as in
the DFT runs (``mace_mp(dispersion=True)``). Single points with Hg at 3.4 A over flat graphene and
full BFGS relaxations (output ``hg_mace_sites.py.log``; E_ads in eV, h(Hg) in A)::

    model                  E_ads at 3.4 A          E_ads relaxed            h(Hg)    C-C (A)
                           top    bridge hollow    top    bridge hollow     relaxed  relaxed
    MP medium              +0.257 +0.256 +0.244    -0.013 -0.013 -0.013     4.72-4.78  1.424-1.425
    MPA-0 medium           +0.361 +0.365 +0.345    -0.178 -0.172 -0.161     4.56-4.63  1.424-1.426
    MP medium + D3(BJ)     +0.038 +0.037 +0.025    -0.111 -0.110 -0.107     4.36-4.41  1.424-1.426
    MPA-0 medium + D3(BJ)  +0.142 +0.146 +0.125    -0.273 -0.269 -0.260     4.50-4.56  1.424-1.426
    DFT (PBE+D3, 6x6x1)    -0.194 -0.195 -0.202    (Hg at 3.4 A, flat graphene)

* MACE keeps the graphene ideal (C-C 1.424-1.426 A) and gives nearly equal energies for the three
  sites, like the converged DFT: it has no electronic degeneracy at Gamma and is not affected by
  the Kekule artefact.
* MACE is repulsive at the DFT adsorption height (E_ads > 0 at 3.4 A) and places Hg 1.0-1.4 A too
  far from the sheet (4.4-4.8 A vs 3.4 A).
* Dispersion matters: without D3 the MP model barely binds Hg (-0.01 eV); MPA-0 + D3 gives the
  closest energy to DFT (-0.27 vs -0.19 to -0.20 eV), but at the wrong height, i.e. for the wrong
  reason. Foundation MLIPs are thus useful for geometries of strongly bound systems, but weak
  metal-atom physisorption on graphene would need fine-tuning on DFT(+D3) data of this system -
  directly relevant for MLIP-based adsorption studies.
