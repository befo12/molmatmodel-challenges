==========================================================================
Molecular and Materials Modeling School (JINR, August 2026) - Challenges
==========================================================================

Solutions of the challenges of the school "Molecular and Materials Modeling"
(BLTP JINR, August 26-27, 2026; course repository
https://github.com/miroi/Molecular-and-Materials-Modeling-2026-August).

Author: Berfin (GitHub: befo12)

Each challenge is in its own directory ``Challenge_X_N`` with a ``readme.rst`` (task, method,
results, discussion), all input files and scripts, and the output files of the runs.
In every challenge the course example was first re-run and compared with the course reference
output; the challenge itself was then solved on top of it.

Computational environment
-------------------------
* ASUS notebook, Intel Core i7-12650H (6 performance + 4 efficiency cores), Windows 11 + WSL2 Ubuntu
* Miniforge, conda environment ``molmatmodel`` (conda-forge): Quantum ESPRESSO 7.6, NWChem 7.3.1,
  MOPAC 23.2.5, xtb, CREST, PySCF, GROMACS, ASE 3.29, OpenMPI 5.0; ``mace-torch`` 0.3.16 (pip)
* Pseudopotentials: course files (PseudoDojo norm-conserving, PBE) and, for comparisons, the
  Ubuntu package ``quantum-espresso-data``

Overview
--------

Part I - Molecular modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~

==================  ===========================================================================
Challenge           Main result
==================  ===========================================================================
``Challenge_I_1``   All software checks pass. Found and fixed a missing dependency of conda-forge
                    QE 7.6 (``libelpa.so.19``) by installing the matching OpenMPI build of ELPA.
``Challenge_I_2``   NWChem, QE and MOPAC timings for 1-8 processes/threads; best performance with
                    4-6 workers on this hybrid (P/E-core) CPU.
``Challenge_I_3``   MACE-MP atomization energies of 7 diatomics: good bond lengths, 5-8 % error for
                    H2, N2, O2, CO, but failure for F2, Cl2, HF (F2 unbound).
``Challenge_I_4``   All MACE test scripts run; energies identical to the course reference.
``Challenge_I_5``   Ideal-gas thermochemistry of 7 diatomics with MACE: S0 within 0.6 % of
                    experiment; vibrational frequencies are the more sensitive test.
``Challenge_I_6``   C-H bond energy of CH4: MACE D0 = 377 kJ/mol vs. 433 kJ/mol (exp.); shows the
                    importance of the zero-point correction.
``Challenge_I_7``   QE (PBE) relaxation of CH4: r(C-H) = 1.094 A (exp. 1.087 A); ecutwfc
                    convergence test (80 Ry within 1 meV).
``Challenge_I_8``   UO2I2(OH2)2: NWChem B3LYP/ECP reproduces the course result; MACE-MPA-0 gives
                    a better U-I distance than the course MACE model.
==================  ===========================================================================

Part II - Materials modeling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

==================  ===========================================================================
Challenge           Main result
==================  ===========================================================================
``Challenge_II_1``  Si total energy (QE and ASE-QE) reproduced; ecutwfc convergence for three
                    pseudopotentials (norm-conserving PBE/LDA, ultrasoft PBE).
``Challenge_II_2``  Automated convergence: 65 / 90 / 75 Ry for the three pseudopotentials, k-grid
                    15x15x15 for all; forces and stress, displaced-atom test.
``Challenge_II_3``  Cell relaxation (QE vc-relax and ASE): a(PBE) = 5.469 A; a manually displaced
                    atom returns to the ideal position with tighter thresholds.
``Challenge_II_4``  Si DOS/PDOS; Kohn-Sham (PBE) gap 0.61 eV vs. 1.12 eV (exp.); a Gaussian
                    broadening >= 0.02 Ry closes the gap in the DOS.
``Challenge_II_5``  Al from the experimental structure: convergence, EOS relaxation
                    (a0 = 4.037 A, B = 78 GPa) and DOS with the relaxed cell; k-point oscillations
                    of a metal discussed.
``Challenge_II_6``  Graphene (convergence, 2D relaxation, DOS/PDOS) reproduced; pz character at
                    E_F; the even 20x20x1 grid misses the Dirac point and gives an artificial
                    0.88 eV gap.
``Challenge_II_7``  Work function of graphene W = 4.24 eV, identical with and without the 2D
                    Coulomb cutoff although E_F differs by 2.5 eV.
``Challenge_II_8``  H on graphene: course result reproduced; correct spin polarization lowers
                    E_b from 2.86 to 2.13 eV; cutoff converged; cell-size / k-point dependence.
                    Hg on C18: on-top site reproduces the course E_ads = -0.24 eV; bridge and
                    hollow (-0.51, -0.67 eV) are dominated by a Kekule-type distortion of the
                    graphene, most likely an artefact of the Gamma-only 3x3 cell.
==================  ===========================================================================

Large scratch files of the codes (wavefunctions, QE ``tmp/`` directories, NWChem ``*.db`` and
``*.movecs``) are not included (``.gitignore``); they are not needed to check the results.
