================================================================================
Challenge II.4 - Electronic properties of Si (charge density, Lowdin, DOS, PDOS)
================================================================================

Task
----
Electronic properties of Si (charge density, Lowdin charges, DOS, PDOS).
Challenge (course ``readme.rst``): "Modify the input parameters in the Si ASE script and test the
effects of different values of Gaussian broadening (degauss)."

Exercise
--------
``electronic_properties_si.py`` (course script; only the QE executables changed to the conda
installation, 6 MPI processes): SCF (65 Ry, k = 15x15x15) -> ``pp.x`` charge density
(``charge_density.cube``, view in VESTA), ``projwfc.x`` Lowdin charges (``lowdin.out``);
NSCF (k = 30x30x30) -> ``dos.x`` total DOS (``total_dos.dat``) and ``projwfc.x`` PDOS
(``pdos_results/``). Output: ``electronic_properties_si.out``.

The result reproduces the course reference: E_F = 6.3215 eV, integrated TDOS 7.9999 states,
integrated sum of PDOS 7.9292 states (0.88 % difference, i.e. low spilling).

Figure ``dos_pdos_si.png``: TDOS, sum of PDOS and s/p PDOS of Si atom 1 vs E - E_F.

Lowdin charges (``lowdin.out``)::

    Löwdin Charges from SCF calculation (projwfc.out):
    ================================================
    Lowdin Charges: 
         Atom #   1: total charge =   3.9644, s =  1.1604, 
         Atom #   1: total charge =   3.9644, p =  2.8040, pz=  0.9347, px=  0.9347, py=  0.9347, 
         Atom #   2: total charge =   3.9644, s =  1.1604, 
         Atom #   2: total charge =   3.9644, p =  2.8040, pz=  0.9347, px=  0.9347, py=  0.9347, 
    Spilling Parameter: 0.008900

Challenge - Gaussian broadening (degauss)
-----------------------------------------
``degauss_dos_test.py`` re-uses the NSCF wavefunctions and runs ``dos.x`` with
degauss = 0.002, 0.005, 0.01, 0.02 and 0.05 Ry (inputs/outputs in ``degauss_test/``,
figure ``degauss_test/dos_vs_degauss.png``). It also reads the Kohn-Sham eigenvalues of all
NSCF k-points from ``tmp/Si_Electronic.save/data-file-schema.xml`` to get the band gap::

    degauss/Ry  sigma/eV  gap in DOS/eV  VBM-EF/eV  CBM-EF/eV
         0.002     0.027           0.56      -0.28       0.28
         0.005     0.068           0.51      -0.25       0.26
         0.010     0.136           0.38      -0.19       0.19
         0.020     0.272         closed          -          -
         0.050     0.680         closed          -          -
    (gap in DOS = width of the region with DOS < 0.01 states/eV around E_F)
    Kohn-Sham (PBE) band gap from NSCF eigenvalues: 0.611 eV  (VBM 6.016 eV, CBM 6.627 eV)
    Experimental band gap of Si: 1.12 eV (indirect)
    Figures: dos_pdos_si.png, degauss_test/dos_vs_degauss.png

Discussion
----------
* Broadening: degauss replaces every eigenvalue by a Gaussian of width sigma = degauss.
  Small values (0.002 Ry) give a noisy but sharp DOS with the gap clearly open; larger values
  smooth the DOS but smear the band edges into the gap. The apparent gap in the DOS shrinks
  (0.56 -> 0.51 -> 0.38 eV) and closes completely for degauss >= 0.02 Ry (sigma = 0.27 eV),
  so Si would wrongly look metallic. The broadening must be small compared with the features
  of interest, and the k-mesh dense enough that a small broadening still gives a smooth DOS.
* Band gap: the Kohn-Sham (PBE) gap from the eigenvalues is 0.61 eV, independent of degauss,
  in agreement with the literature PBE value (~0.6 eV) but only about half of the experimental
  gap of 1.12 eV. This is the well-known band-gap problem of LDA/GGA: Kohn-Sham eigenvalues
  are not quasiparticle energies (missing derivative discontinuity, self-interaction error).
  Hybrid functionals (HSE06 ~1.1-1.2 eV) or GW give gaps close to experiment.
* The valence band is s-like at the bottom (-12 to -8 eV) and p-like near the top, as
  expected for sp3-bonded Si. Above E_F the sum of PDOS is lower than the TDOS because the
  atomic s/p projectors do not fully describe the conduction states.
