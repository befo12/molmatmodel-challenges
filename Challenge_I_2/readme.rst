=============================================
Challenge I.2 - Software performance checks
=============================================

Task
----
Measure the performance of NWChem, Quantum ESPRESSO and MOPAC on my personal
computer for different numbers of MPI processes / threads (inputs from the course
repository, ``molecular-modeling/software_performance``).

Machine
-------
* CPU: 12th Gen Intel(R) Core(TM) i7-12650H
* Physical cores: 8, logical CPUs: 16
* OS: Windows + WSL2, Ubuntu 26.04.1 LTS
* Software from conda-forge (env ``molmatmodel``): mopac 23.2.5, nwchem 7.3.1, openmpi 5.0.11, qe 7.6
* ``OMP_NUM_THREADS=1`` for MPI runs (NWChem, QE); ``OMP_NUM_THREADS=N`` together with ``THREADS=N`` for MOPAC

Test systems
------------
* NWChem: CH3 radical, ZORA B3LYP/6-311G, EPR/NMR properties (``ch3_zora_b3lyp_prop.nw``)
* Quantum ESPRESSO: Tl2 bulk SCF with spin-orbit, 8x8x8 k-points (``Tl2.so_scf.in``)
* MOPAC: "mini DNA" C40H50N14O26P4, PM7 single point (``dna_pm7.mop``, THREADS=N)

Results (wall time, seconds)
----------------------------

+--------------------+--------+--------+--------+
| Software           |   N    | Wall/s | Status |
+====================+========+========+========+
| NWChem             |      1 |   17.3 | OK     |
+--------------------+--------+--------+--------+
| NWChem             |      2 |   14.9 | OK     |
+--------------------+--------+--------+--------+
| NWChem             |      4 |   11.8 | OK     |
+--------------------+--------+--------+--------+
| NWChem             |      6 |   11.5 | OK     |
+--------------------+--------+--------+--------+
| NWChem             |      8 |   11.9 | OK     |
+--------------------+--------+--------+--------+
| QE                 |      1 |   40.5 | OK     |
+--------------------+--------+--------+--------+
| QE                 |      2 |   30.4 | OK     |
+--------------------+--------+--------+--------+
| QE                 |      4 |   20.7 | OK     |
+--------------------+--------+--------+--------+
| QE                 |      6 |   20.0 | OK     |
+--------------------+--------+--------+--------+
| QE                 |      8 |   25.6 | OK     |
+--------------------+--------+--------+--------+
| MOPAC              |      1 |   31.2 | OK     |
+--------------------+--------+--------+--------+
| MOPAC              |      2 |   24.2 | OK     |
+--------------------+--------+--------+--------+
| MOPAC              |      4 |   23.5 | OK     |
+--------------------+--------+--------+--------+
| MOPAC              |      6 |   24.5 | OK     |
+--------------------+--------+--------+--------+
| MOPAC              |      8 |   31.3 | OK     |
+--------------------+--------+--------+--------+

N = number of MPI processes (NWChem, QE) or OpenMP threads (MOPAC).
All input and output files are in the ``nwchem/``, ``qe/`` and ``mopac/`` subdirectories.

Discussion
----------
* Best wall times: NWChem 11.5 s with 6 MPI processes (1.5x speed-up vs. 1 process),
  Quantum ESPRESSO 20.0 s with 6 MPI processes (2.0x), MOPAC 23.5 s with 4 threads (1.3x).
* All three codes become slower again with 8 processes/threads. The i7-12650H is a hybrid
  CPU with 6 performance (P) cores and 4 efficiency (E) cores; WSL2 reports 8 cores /
  16 logical CPUs. With more than 6 workers some of them run on slower E-cores or share
  a P-core via hyper-threading, and the whole parallel job waits for the slowest worker.
  On this notebook, 4-6 workers is the best choice.
* Scaling is limited because the test systems are small: the fixed costs (start-up,
  MPI communication, serial parts of the code) are a large fraction of the run time.
* Note on MOPAC: in a first run ``OMP_NUM_THREADS=1`` was exported for the whole script,
  which overrode the MOPAC ``THREADS=N`` keyword, and MOPAC showed no speed-up (29-31 s for
  all N). Setting ``OMP_NUM_THREADS=N`` for each MOPAC run fixed this.
* Wall times on a notebook vary by roughly 15-20 % between repeated runs (turbo boost,
  temperature); e.g. QE with 6 MPI processes took 16.7 s in the first run and 20.0 s here.
