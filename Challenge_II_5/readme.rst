==================================================================
Challenge II.5 - Electronic properties of Al (fcc metal)
==================================================================

Exercise
--------
Course script ``electronic_properties_al.py`` (Materials Project cell, a = 4.0389 A, ecutwfc = 65 Ry,
k = 15 (SCF) / 30 (NSCF), Gaussian smearing 0.01 Ry; only the QE executables changed).
Output ``electronic_properties_al.out``; reproduces the reference: E_F = 7.9691 eV
(ref. 7.9692 eV), integrated TDOS 2.9966 states (3 valence electrons), sum of PDOS 2.9528 states (1.46 %).

Challenge
---------
``al_challenge.py`` (output ``al_challenge.py.log``, all runs in ``runs/``):

1. Experimental structure: fcc Al, Fm-3m, a = 4.0495 A (room temperature; Wyckoff 1963, COD 9008460).
2. Convergence tests with the course pseudopotential (``Al.upf``) and smearing, tolerance 1 meV/atom
   between successive steps: ecutwfc at k = 12, then k at the converged cutoff.
3. Relaxation of the cubic cell with a Birch-Murnaghan equation of state (7 points, a_exp +-3 %),
   figure ``al_eos.png``.
4. The course script re-run with the relaxed cell and the converged parameters
   (``relaxed_electronic/``; k(NSCF) = 2 k(SCF)).

Results
-------
::

    1. ecutwfc convergence at k = 12x12x12, a = 4.0495 A (tolerance 1.0 meV/atom)
       ecutwfc =  20 Ry  E = -63.024195 eV
       ecutwfc =  25 Ry  E = -63.053553 eV  dE =  -29.358 meV
       ecutwfc =  30 Ry  E = -63.066903 eV  dE =  -13.350 meV
       ecutwfc =  35 Ry  E = -63.073261 eV  dE =   -6.358 meV
       ecutwfc =  40 Ry  E = -63.073970 eV  dE =   -0.710 meV
    >>> ecutwfc converged at 40 Ry
    2. k-point convergence at ecutwfc = 40 Ry
       k =  4x 4x 4  E = -62.785235 eV
       k =  6x 6x 6  E = -63.132660 eV  dE = -347.426 meV
       k =  8x 8x 8  E = -63.061466 eV  dE =   71.194 meV
       k = 10x10x10  E = -63.048593 eV  dE =   12.873 meV
       k = 12x12x12  E = -63.073970 eV  dE =  -25.377 meV
       k = 14x14x14  E = -63.059043 eV  dE =   14.927 meV
       k = 16x16x16  E = -63.071392 eV  dE =  -12.349 meV
       k = 18x18x18  E = -63.064384 eV  dE =    7.008 meV
       k = 20x20x20  E = -63.065934 eV  dE =   -1.549 meV
       k = 22x22x22  E = -63.067919 eV  dE =   -1.985 meV
       k = 24x24x24  E = -63.065082 eV  dE =    2.837 meV
       k = 26x26x26  E = -63.067645 eV  dE =   -2.563 meV
       k = 28x28x28  E = -63.065947 eV  dE =    1.697 meV
       k = 30x30x30  E = -63.066869 eV  dE =   -0.922 meV
    >>> k-points converged at 30x30x30
    3. Equation of state around a_exp (ecutwfc = 40 Ry, k = 30)
       a = 3.9280 A  V = 15.1516 A^3  E = -63.038411 eV
       a = 3.9685 A  V = 15.6251 A^3  E = -63.056330 eV
       a = 4.0090 A  V = 16.1083 A^3  E = -63.065523 eV
       a = 4.0495 A  V = 16.6014 A^3  E = -63.066869 eV
       a = 4.0900 A  V = 17.1044 A^3  E = -63.061185 eV
       a = 4.1305 A  V = 17.6175 A^3  E = -63.049226 eV
       a = 4.1710 A  V = 18.1408 A^3  E = -63.031683 eV
    >>> relaxed a0 = 4.0365 A (exp. 4.0495 A, -0.32 %), V0 = 16.4416 A^3, B = 78.2 GPa (exp. ~76 GPa)
    4. Electronic properties with a0 = 4.0365 A, ecutwfc = 40 Ry, k(SCF) = 30, k(NSCF) = 60:
      7. Verifying TDOS vs summed PDOS (ONLY below Fermi level)...
      Fermi level from NSCF calculation: 7.9751 eV
      Integrated TDOS: 2.9979 states
      Integrated sum of PDOS: 2.9539 states
      Relative difference in integrated DOS: 1.47%

Summary::

                         course cell     this work (relaxed)     experiment
    a (A)                  4.0389            4.0365               4.0495 (300 K)
    B (GPa)                  -                78.2                ~76
    ecutwfc (Ry)            65                40                    -
    k-grid SCF / NSCF      15 / 30           30 / 60                -
    E_F (eV)               7.9691            7.9751                 -

Discussion
----------
* Lattice constant and bulk modulus: PBE gives a0 = 4.0365 A (-0.3 % vs. the room-temperature
  experiment) and B = 78.2 GPa, both in good agreement with experiment and with literature PBE
  values. The remaining difference in a0 is partly thermal expansion and zero-point motion,
  which are not included in the static DFT calculation.
* Cutoff: 40 Ry is enough for 1 meV/atom with this norm-conserving Al pseudopotential.
* k-points (metal): the energy oscillates with the k-grid (+-1.5 to 3 meV up to 28x28x28)
  because the Fermi surface is sampled with only a small Gaussian broadening (0.01 Ry).
  The criterion "successive difference < 1 meV" is fulfilled at 30x30x30, but with the
  oscillations still at the ~1-2 meV level this is only marginal convergence. For metals a
  larger, better-behaved smearing (e.g. Marzari-Vanderbilt, 0.02 Ry) converges much faster;
  semiconductors such as Si (Challenge II.2) do not have this problem.
* The EOS energy differences (~35 meV over +-3 % in a) are much larger than the k-point
  noise, so a0 and B are robust.
* The DOS of Al is free-electron-like (sqrt(E) shape from the band bottom up to E_F) with
  no gap at E_F, as expected for a simple metal; the integrated TDOS gives the 3 valence
  electrons of Al.
