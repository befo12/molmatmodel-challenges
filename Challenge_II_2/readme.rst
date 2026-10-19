====================================================================
Challenge II.2 - Automated cutoff and k-point convergence (ASE + QE)
====================================================================

Task 2.1 - automated convergence test
-------------------------------------
Course script ``convergence_test_si.py`` (ecutwfc 20-115 Ry in 5 Ry steps at k = 13x13x13,
then k = 2..24 at the converged cutoff; tolerance 0.01 meV/atom between successive steps).
Only the pw.x command (``mpirun -np 6 pw.x``) and the pseudopotential settings were changed.

Challenge - different pseudopotentials
--------------------------------------
``make_pp_variants.py`` writes one copy of the course script per pseudopotential into
``pp_*/`` (output ``pp_*/convergence_test_si_*.out``). For the ultrasoft potential
ecutrho = 8 ecutwfc was added; all other settings are identical.

::

    Pseudopotential                              type, XC   converged ecutwfc   converged k-grid
    ---------------------------------------------------------------------------------------------
    Si.upf (PseudoDojo, course)                  NC, PBE        65 Ry            15x15x15
    Si.pbe-nl-rrkjus_psl.1.0.0.UPF (pslibrary)   US, PBE        90 Ry            15x15x15
    Si.pz-vbc.UPF (von Barth-Car)                NC, LDA        75 Ry            15x15x15

The PseudoDojo result (65 Ry, 15x15x15) is identical to the course reference output.

Number of SCF runs performed by ASE for the course pseudopotential: 10 for ecutwfc + 14 for k-points = 24
(ASE overwrites espresso.pwi/espresso.pwo at every step, so only the last run is kept on disk).

Task 2.2 - forces and stress at the converged settings
------------------------------------------------------
``Si_force_stress.in`` (ecutwfc = 65 Ry, k = 15x15x15, tstress/tprnfor = .true.), and a
modified copy ``Si_shifted_force_stress.in`` in which the first Si atom is displaced by
+0.1 A along x (idea of task 2.3: shift the atoms manually)::

    Si_force_stress (course reference: -16.92488384 Ry, P = 19.93 kbar):
    !    total energy              =     -16.92488372 Ry
         atom    1 type  1   force =     0.00000000   -0.00000000    0.00000000
         atom    2 type  1   force =     0.00000000    0.00000000    0.00000000
              total   stress  (Ry/bohr**3)                   (kbar)     P=       19.93

    Si_shifted_force_stress:
    !    total energy              =     -16.91990527 Ry
         atom    1 type  1   force =    -0.05223499    0.00000000    0.00000000
         atom    2 type  1   force =     0.05223499    0.00000000    0.00000000
              total   stress  (Ry/bohr**3)                   (kbar)     P=       23.36

Discussion
----------
* The cutoff needed for convergence depends strongly on the pseudopotential (65-90 Ry
  for 0.01 meV/atom); the k-point convergence (15x15x15) does not, because it is set by the
  Brillouin-zone sampling of the crystal, not by the pseudopotential.
* The 0.01 meV/atom criterion between successive steps is very strict; for most purposes
  ~1 meV/atom (Challenge II.1: 40-50 Ry) is sufficient.
* In the ideal diamond structure all forces are zero by symmetry, but the pressure is
  ~20 kbar: the experimental lattice constant used here (5.43 A) is not the PBE equilibrium
  lattice constant, so the cell would expand in a variable-cell relaxation (Challenge II.3).
* Displacing one atom by 0.1 A breaks the symmetry: equal and opposite forces appear on the
  two atoms (Newton's third law) and the total energy increases.
