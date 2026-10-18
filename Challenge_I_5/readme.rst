==============================================================
Challenge I.5 - Thermodynamic properties of diatomic molecules
==============================================================

Task
----
Modify the N2 script ``N2_thermodyn_EMT_MACE_04.py`` (Exercise I.5) to compute
thermodynamic properties of other diatomic molecules.

Files
-----
* ``N2_thermodyn_EMT_MACE_04.py`` - original course script, output ``N2_thermodyn_EMT_MACE_04.py.log``
* ``thermo_diatomics.py`` - modified script: loop over H2, N2, O2, F2, Cl2, CO, HF
* ``thermo_diatomics.py.log`` - output

Method
------
* MACE-MP medium (float64, CPU); geometry optimized with BFGS (fmax = 0.001 eV/A).
* Harmonic frequencies from finite differences (``ase.vibrations.Vibrations``).
* ``ase.thermochemistry.IdealGasThermo``: linear geometry, symmetry number 2 for homonuclear
  and 1 for heteronuclear molecules, spin S = 1 for triplet O2, S = 0 otherwise.
* T = 298.15 K, p = 1 bar. Experimental w_e and S0 from NIST WebBook / CCCBDB.

Results
-------
::

    T = 298.15 K, p = 1 bar; H and G are given relative to the electronic energy E_pot
    Mol |    r/A |  w_MACE   w_exp    err |  ZPE/eV  H-E/eV |  S_MACE   S_exp    err |  G-E/eV
    --------------------------------------------------------------------------------------------------
    H2  |  0.747 |    4436    4401  +0.8% |   0.275   0.365 |  130.47  130.68  -0.2% |  -0.038
    N2  |  1.112 |    2347    2359  -0.5% |   0.146   0.235 |  191.79  191.61  +0.1% |  -0.357
    O2  |  1.237 |    1419    1580 -10.2% |   0.088   0.178 |  205.51  205.15  +0.2% |  -0.457
    F2  |  1.456 |     676     917 -26.3% |   0.042   0.135 |  204.00  202.79  +0.6% |  -0.495
    Cl2 |  1.981 |     586     560  +4.7% |   0.036   0.131 |  222.67  223.08  -0.2% |  -0.557
    CO  |  1.143 |    2018    2170  -7.0% |   0.125   0.215 |  197.83  197.66  +0.1% |  -0.396
    HF  |  0.942 |    3767    4138  -9.0% |   0.234   0.323 |  174.04  173.78  +0.1% |  -0.214
    
    w in cm-1, S in J/(mol K).

Discussion
----------
* Standard entropies agree with experiment within 0.6 % for all molecules, including those
  for which MACE-MP gives poor frequencies or bond energies. At 298 K the entropy is
  dominated by translation and rotation, which depend only on mass, bond length and symmetry;
  the vibrational contribution is small for these stiff bonds.
* The correct symmetry numbers and the triplet ground state of O2 are essential: with
  spin = 0 the O2 entropy would be R ln 3 = 9.1 J/(mol K) too low.
* Vibrational frequencies are a more sensitive test of the potential energy surface
  (second derivatives): very good for H2, N2 and Cl2 (< 5 %), but 7-10 % too low for O2, CO
  and HF and 26 % too low for F2 - the same molecules for which the atomization energies
  in Challenge I.3 were poor.
* ZPE and thermal enthalpy corrections are 0.04-0.28 eV and 0.13-0.37 eV, i.e. not
  negligible compared to reaction energies; this is why the START project adds such
  thermochemical corrections to computed adsorption energies.
