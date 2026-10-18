==========================================================
Challenge I.6 - C-H bond dissociation energy of methane
==========================================================

Task
----
Modify the ethane C-C bond energy script (Exercise I.6) to compute the C-H bond energy
in methane from the reaction CH4 -> CH3. + H.

Files
-----
* ``ethane_CC_bond_en_EMT_MACE_01.py`` - original course script (ethane C-C), output ``*.log``
* ``methane_CH_bond_en.py`` - modified script for methane C-H, output ``methane_CH_bond_en.py.log``
* ``*.traj`` - optimization trajectories, ``vib_*`` - finite-difference displacements

Method
------
* CH4, CH3 and H relaxed with BFGS (fmax = 0.001 eV/A) using EMT and MACE-MP medium (float64).
* D_e = E(CH3) + E(H) - E(CH4).
* For MACE also the zero-point corrected value D_0 = D_e - [ZPE(CH4) - ZPE(CH3)],
  with harmonic frequencies from ``ase.vibrations.Vibrations``.
* Experiment: D_0(CH3-H) = 432.7 kJ/mol, r(C-H) = 1.087 A.

Results
-------
::

    MACE: ZPE(CH4) - ZPE(CH3) = 0.411 eV
    ==================================================================
    C-H BOND IN METHANE:  CH4 -> CH3. + H.
    ==================================================================
    Method    r(C-H)/A    D_e/eV  D_e kJ/mol  D_0 kJ/mol    err D
    ------------------------------------------------------------------
    EMT          1.152     3.254       313.9           -   -27.4%
    MACE         1.093     4.316       416.4       376.7   -12.9%
    Exp.         1.087                             432.7
    ------------------------------------------------------------------
    err D: D_0 vs experiment for MACE, D_e vs experimental D_0 for EMT.

For comparison, the original ethane script gives C-C: MACE 1.522 A / 360.3 kJ/mol,
EMT 1.010 A / 208.3 kJ/mol (exp. 1.536 A, ~368 kJ/mol).

Discussion
----------
* EMT fails completely for this covalent organic molecule (C-H bond 6 % too long,
  bond energy 27 % too low); it is designed for close-packed metals.
* MACE-MP gives a good C-H bond length (1.093 vs 1.087 A).
* The MACE bond energy without ZPE (416 kJ/mol) looks close to experiment, but this is
  partly fortuitous: the experimental value is a D_0, which already contains the zero-point
  energy. The ZPE of CH4 is larger than that of CH3 by 0.41 eV (40 kJ/mol, MACE), so the
  consistent comparison D_0(MACE) = 377 kJ/mol vs 433 kJ/mol shows MACE underbinding the
  C-H bond by ~13 %.
* The same applies to the ethane C-C comparison in the course script (D_e compared directly
  with an experimental D_0/D_298). Consistent comparison with experiment requires ZPE (and,
  at 298 K, thermal) corrections - the same thermochemical corrections that the START
  project applies to adsorption energies.
* As in Challenge I.3, the underbinding of molecules and radicals is consistent with
  MACE-MP being trained on bulk crystalline materials rather than on gas-phase molecules.
