====================================================================
Challenge II.6 - Graphene: convergence, 2D cell relaxation, DOS/PDOS
====================================================================

Exercise (course scripts, only the QE executables changed; each step in its own directory)
------------------------------------------------------------------------------------------
* ``convergence_test_graphene/`` - Step 6.1: graphene (c = 15 A vacuum, ``assume_isolated = '2D'``),
  ecutwfc and (3k, 3k, 1) k-grid convergence: **100 Ry** and **(42, 42, 1)**, as in the reference.
* ``cell_relaxation_graphene/`` - Step 6.2: in-plane cell relaxation (UnitCellFilter mask, only xx, yy):
  E = -327.840666 eV, P = 0.064 kbar (reference -327.840655 eV, 0.062 kbar).
* ``electronic_properties_graphene/`` - Step 6.3: charge density, Lowdin charges, TDOS and PDOS
  (SCF 42x42x1, NSCF 66x66x1): E_F = -4.2408 eV, TDOS/PDOS integral difference 0.97 % (reference 0.97 %).

Figure ``electronic_properties_graphene/pdos_p_orbitals_graphene_vs_si.png``: p-orbital PDOS of C in
graphene (pz, px, py) compared with Si (Challenge II.4).

Challenge - lower k-grids (``electronic_properties_graphene/graphene_kgrid_test.py``)
-------------------------------------------------------------------------------------
The course script was re-run with SCF = NSCF grids of 12x12x1, 18x18x1 and the 'even' 20x20x1
(``kgrid_*``). From the NSCF data: E_F, DOS at E_F, Kohn-Sham eigenvalues at Gamma, and the smallest
direct gap between band 4 (pi) and band 5 (pi*) over all k-points (read from
``tmp/graphene.save/data-file-schema.xml``). Figure ``dos_vs_kgrid.png``.

::

    k-grid (SCF / NSCF)          E_F/eV  DOS(E_F)  min pi-pi* gap/eV    #k   Gamma: bands 3-6 relative to E_F (eV)
    --------------------------------------------------------------------------------------------------------------
    12x12x1                      -4.240    0.2304              0.000    19    -3.061   -3.061    3.291    4.195
    18x18x1                      -4.240    0.1024              0.000    37    -3.062   -3.062    3.291    4.195
    20x20x1                      -4.245    0.0000              0.876    44    -3.057   -3.057    3.296    4.200
    42x42x1 / 66x66x1 (conv.)    -4.241    0.0095              0.000   397    -3.061   -3.061    3.292    4.196

Discussion
----------
* PDOS: near E_F the states of graphene are purely C pz (pi / pi* bands forming the Dirac cones),
  while px and py (sp2 sigma bonds) lie below about -3 eV and above the gap of the sigma bands.
  In Si the three p orbitals are identical by cubic symmetry and all take part in the sp3 bonds;
  there is no orbital separation and a real band gap at E_F.
* Grids divisible by 3 (12, 18, 42) contain the Dirac point K = (1/3, 1/3, 0): the pi-pi* gap is 0
  and graphene is correctly a zero-gap semimetal.
* The even 20x20x1 grid does not contain K: the closest k-points give an artificial gap of 0.88 eV,
  DOS(E_F) = 0 and a slightly shifted E_F - graphene would wrongly appear as a semiconductor.
* Coarse grids that do contain K (12, 18) give a much too large DOS at E_F (0.23 and 0.10 vs 0.0095
  states/eV), because the few k-points near K carry large weights; the linear DOS of the Dirac cone
  needs the dense NSCF grid.
* The eigenvalues at Gamma agree within ~5 meV for all grids: the SCF charge density is already well
  described with coarse grids; the errors are confined to the region around K, which dominates the
  physics near E_F.
