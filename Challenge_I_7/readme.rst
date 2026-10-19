==============================================================
Challenge I.7 - Quantum ESPRESSO geometry relaxation of CH4
==============================================================

Task
----
Adapt the ASE-driven Quantum ESPRESSO water optimization (``qe_h2o_optimize.py``,
Exercise I.7) to relax the CH4 molecule and compare with experiment.

Files
-----
* ``qe_h2o_optimize.py`` - original course script (water, for reference)
* ``qe_ch4_optimize.py`` - adapted script for CH4; output ``qe_ch4_optimize.py.log``,
  ``ch4_opt.log``, ``ch4_opt.traj``, ``espresso.pwi`` / ``espresso.pwo``
* ``ecut_convergence_ch4.py`` - ecutwfc convergence test; output ``ecut_convergence_ch4.py.log``,
  run directories ``cut_*``
* ``C.upf``, ``H.upf`` - pseudopotentials

Method
------
* Quantum ESPRESSO 7.6 (conda-forge) driven by ASE, 4 MPI processes.
* PBE, PseudoDojo norm-conserving pseudopotentials (``C.upf``, ``H.upf`` from
  ``materials-modeling/`` of the course repository). The PAW files used in the water example
  (``/usr/share/espresso/pseudo``) are not part of the conda installation.
* CH4 in a 12 x 12 x 12 A box, Gamma point, ecutwfc = 80 Ry, conv_thr = 1e-8,
  BFGS until fmax < 0.01 eV/A.

Results
-------
Geometry (2 BFGS steps, 3 SCF calculations of ~13 s each)::

                    QE (PBE)      Exp.     Diff.
    r(C-H) / A        1.0941    1.0870   +0.0071
    H-C-H / deg       109.47    109.47     +0.00

    Final energy: -228.6940 eV

All four C-H bonds are equal and all angles are 109.47 deg (Td symmetry preserved).

ecutwfc convergence (single points at the optimized geometry)::

    ecutwfc/Ry           E/eV   E-E(100)/meV
            40    -227.987522         707.60
            50    -228.464286         230.83
            60    -228.636518          58.60
            70    -228.684718          10.40
            80    -228.693974           1.15
            90    -228.694974           0.14
           100    -228.695119           0.00

Discussion
----------
* The PBE C-H bond length is 0.007 A (0.65 %) longer than experiment, the typical slight
  overestimation of bond lengths by GGA functionals; the tetrahedral angle is exact by symmetry.
* With the norm-conserving pseudopotentials the total energy is converged to ~1 meV at
  80 Ry, so the cutoff used for the relaxation is sufficient. Norm-conserving PPs need a
  higher cutoff than the PAW potentials of the water example (46 Ry).
* For comparison, MACE-MP gave r(C-H) = 1.093 A for CH4 in Challenge I.6 - very close to
  this DFT result, at a tiny fraction of the cost.
