==================================================================
Challenge I.3 - Atomization energies of diatomic molecules (MACE)
==================================================================

Task
----
Modify the N2 script ``at_en_mace_EMT_N2.py`` (Exercise I.3) so that it computes
atomization energies of other diatomic molecules in a loop, with EMT and MACE-MP.

Files
-----
* ``at_en_mace_EMT_N2.py`` - original course script (N2), output ``at_en_mace_EMT_N2.py.log``
* ``at_en_diatomics.py`` - modified script, loop over H2, N2, O2, F2, Cl2, CO, HF
* ``at_en_diatomics.py.log`` - output

Method
------
* E_at = E(atom A) + E(atom B) - E(AB), AB geometry optimized with BFGS (fmax = 0.01 eV/A).
* Calculators: ASE ``EMT`` (only H, C, N, O and some metals) and ``mace_mp(model="medium")``, float64, CPU.
* Experimental references: D0 and r_e from NIST CCCBDB / CRC Handbook.

Results
-------
r in Angstrom, atomization energies in eV::

    Mol  |  r_exp  r_EMT  r_MACE |  E_exp   E_EMT  E_MACE | err_MACE
    ----------------------------------------------------------------------
    H2   |  0.741  0.779   0.747 |   4.48    5.35    4.21 |    -6.1%
    N2   |  1.098  0.998   1.112 |   9.76    9.94   10.31 |    +5.7%
    O2   |  1.208  1.100   1.237 |   5.12    8.58    5.53 |    +8.0%
    F2   |  1.412    N/A   1.456 |   1.60     N/A   -0.58 |  -136.4%
    Cl2  |  1.988    N/A   1.981 |   2.48     N/A    1.00 |   -59.8%
    CO   |  1.128  1.056   1.143 |  11.09    7.43   10.56 |    -4.8%
    HF   |  0.917    N/A   0.942 |   5.87     N/A    4.48 |   -23.7%

The N2 result (1.112 A, 10.31 eV) reproduces the reference output of the course script.

Discussion
----------
* MACE-MP bond lengths are good for all molecules (within ~0.04 A of experiment),
  much better than EMT, which shortens all bonds by ~0.04-0.1 A.
* MACE-MP atomization energies are reasonable for H2, N2, O2 and CO (errors 5-8 %),
  but fail for the halogen-containing molecules: Cl2 and HF are strongly underbound and
  F2 even comes out unbound (negative atomization energy).
* Reason: MACE-MP is a foundation model trained on Materials Project data (periodic
  bulk crystals). Isolated atoms and small gas-phase molecules are poorly represented in
  this training set; in particular the spin-polarized free-atom energies, which enter
  E_at directly, are not described consistently.
* Part of the remaining difference is also physical: the calculations give D_e
  (no zero-point energy), whereas the experimental values are D_0 = D_e - ZPE
  (ZPE ~ 0.1-0.3 eV for these molecules), so computed values should lie slightly
  above experiment.
* Conclusion: MACE-MP is suitable for geometries, but for gas-phase reaction energies of
  molecules a molecule-trained model or DFT/ab-initio reference calculations are needed.
