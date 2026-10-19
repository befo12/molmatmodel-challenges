=========================================================
Challenge II.3 - Cell relaxation of Si (QE and ASE-QE)
=========================================================

Task
----
Geometry relaxation (QE and ASE-driven QE) of the Si unit cell.
Challenge (course ``readme.rst``): "For the cell relaxation (both QE and ASE-QE), use custom, tighter
values of etot_conv_thr and forc_conv_thr, shift the atoms manually and run the convergence again."

Runs
----
* ``default/`` - course inputs unchanged (only ``pw_command = 'mpirun -np 6 pw.x'``):

  - Step 3.1, direct QE: ``pw.x < cell_relaxation_si.in`` (vc-relax, BFGS for ions and cell,
    ecutwfc = 45 Ry, k = 12x12x12, QE default thresholds etot_conv_thr = 1e-4 Ry,
    forc_conv_thr = 1e-3 Ry/bohr, press_conv_thr = 0.5 kbar); output ``cell_relaxation_si_direct.out``
  - Step 3.2, ASE-driven QE: ``cell_relaxation_si.py`` (UnitCellFilter + ASE BFGS, fmax = 0.01 eV/A,
    ecutwfc = 65 Ry, k = 15x15x15); output ``cell_relaxation_si.out``, ``relaxation.traj``,
    ``relaxation.log``, ``final_relaxed_structure.vasp``

* ``tight_shifted/`` - Challenge: first Si atom shifted by +0.05 A along x, and tighter criteria:

  - QE: etot_conv_thr = 1e-6 Ry, forc_conv_thr = 1e-5 Ry/bohr, press_conv_thr = 0.1 kbar
  - ASE: fmax = 0.005 eV/A

``summarize_relax.py`` reads all outputs and writes ``summary.txt``.

Results
-------
::

    Run                                     E/eV   P/kbar  Fmax/eV/A    V/A^3      a/A  Si-Si/A  #SCF
    -------------------------------------------------------------------------------------------------
    QE vc-relax (default)             -230.27972     0.00    0.00000  40.8927   5.4689   2.3681     5
    ASE-QE BFGS (default)             -230.28007     0.49    0.00000  40.8705   5.4679   2.3677     3
    QE vc-relax (tight_shifted)       -230.27972     0.00    0.00024  40.8927   5.4689   2.3681    10
    ASE-QE BFGS (tight_shifted)       -230.28008     0.01    0.00115  40.8928   5.4689   2.3680    10
    
    Experimental lattice constant a = 5.431 A, Si-Si = 2.3517 A

Fmax = largest force on the atoms; the cell part of the relaxation is measured by P.

The default runs reproduce the course reference outputs: ASE E = -230.28007 eV,
P = 0.49 kbar (reference -230.280074 eV, 0.488 kbar); direct QE -16.92527471 Ry
(reference -16.92527497 Ry).

Discussion
----------
* All four relaxations end at the same structure: the PBE lattice constant of Si is
  ~5.47 A, about 0.7 % larger than experiment (5.431 A) - the typical GGA overestimation.
  This is why the experimental cell showed a pressure of ~20 kbar in Challenge II.2.
* Stress and forces are negligible at the end of all runs (abs(P) < 0.5 kbar, far within the
  +-50 kbar suggested in the task).
* The manually shifted atom moves back to the ideal diamond position (equal Si-Si bonds),
  i.e. the relaxation is robust against a perturbed starting geometry; the lower symmetry
  and tighter thresholds require more SCF steps.
* Direct QE (vc-relax) and ASE-driven QE use different convergence measures (QE: energy
  change, max force component and pressure; ASE: max force norm including the cell degrees of
  freedom through UnitCellFilter) and in this course example also different ecutwfc and
  k-points, so the total energies differ slightly, but the structures agree.
