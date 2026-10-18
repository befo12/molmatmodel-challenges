========================================================================
Challenge II.1 - Total energy of the Si unit cell (QE and ASE-driven QE)
========================================================================

Exercise
--------
* Step 1: SCF calculation directly with Quantum ESPRESSO 7.6: ``mpirun -np 4 pw.x < Si.in > Si.out``
  (``pseudo_dir`` changed to ``./``).
* Step 2: the same calculation driven by ASE: ``python si_ase.py > si_ase.out``
  (``pw_command`` changed to ``mpirun -np 4 pw.x``); ASE writes ``espresso.pwi`` / ``espresso.pwo``.

Both reproduce the reference outputs of the course::

    Step 1:  ! total energy = -16.73649696 Ry   (reference -16.73649709 Ry), 7 SCF iterations, JOB DONE
    Step 2:  Total energy  = -227.711622 eV    (reference -227.711623 eV)
             Fermi level   =    6.823300 eV    (reference 6.823300 eV)

Challenge
---------
Change ``ecutwfc`` and check how the total energy changes; try different pseudopotentials
for Si. Script: ``si_ecut_pp_test.py``, output ``si_ecut_pp_test.py.log``, runs in ``calc_*``.

Pseudopotentials compared (same structure, k = 2x2x2, Gaussian smearing 0.01 Ry):

* ``Si.upf`` - PseudoDojo norm-conserving, PBE (course file); ecutrho = 4 ecutwfc
* ``Si.pbe-nl-rrkjus_psl.1.0.0.UPF`` - pslibrary ultrasoft, PBE; ecutrho = 8 ecutwfc
* ``Si.pz-vbc.UPF`` - von Barth-Car norm-conserving, LDA; ecutrho = 4 ecutwfc

The last two come from the Ubuntu package ``quantum-espresso-data``
(``/usr/share/espresso/pseudo``); see also https://pseudopotentials.quantum-espresso.org/legacy_tables.

Results
-------
::

    Total energy E (eV) and E - E(80 Ry) (meV/atom); Si, k = 2x2x2
    ecutwfc/Ry |        dojo-NC-PBE        |       rrkjus-US-PBE       |        vbc-NC-LDA        
    ----------------------------------------------------------------------------------------------
            15 |    -227.57548       70.04 |    -275.43333       49.88 |    -212.85430      129.44
            20 |    -227.68719       14.19 |    -275.47602       28.53 |    -213.03276       40.21
            25 |    -227.70691        4.33 |    -275.50675       13.17 |    -213.08351       14.84
            30 |    -227.71162        1.97 |    -275.52066        6.21 |    -213.09901        7.09
            40 |    -227.71503        0.27 |    -275.53062        1.23 |    -213.10911        2.04
            50 |    -227.71520        0.18 |    -275.53258        0.26 |    -213.11244        0.37
            60 |    -227.71534        0.11 |    -275.53280        0.14 |    -213.11310        0.04
            80 |    -227.71557        0.00 |    -275.53309        0.00 |    -213.11318        0.00
    dojo-NC-PBE: converged to < 1 meV/atom at ecutwfc = 40 Ry
    rrkjus-US-PBE: converged to < 1 meV/atom at ecutwfc = 50 Ry
    vbc-NC-LDA: converged to < 1 meV/atom at ecutwfc = 50 Ry

Discussion
----------
* The total energy decreases monotonically (variationally) with ecutwfc for all three
  pseudopotentials, as expected for a plane-wave basis.
* With the course pseudopotential the default ecutwfc = 30 Ry is ~2 meV/atom from the
  converged value; < 1 meV/atom requires 40 Ry.
* The ultrasoft (PBE) and the old LDA norm-conserving potential need ~50 Ry for the same
  accuracy.
* Absolute total energies of different pseudopotentials (-227.7, -275.5 and -213.1 eV)
  must NOT be compared: each pseudopotential has its own reference for the frozen core,
  and the LDA potential also uses a different exchange-correlation functional. Only
  energy differences computed with the same pseudopotential and settings are meaningful.
* The convergence test should always be done for the quantity of interest (e.g. energy
  differences, forces, lattice constant), which usually converge faster than the total energy.
