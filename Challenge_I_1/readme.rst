=====================================================
Challenge I.1 - Basic software functionality checks
=====================================================

Task
----
Run the provided scripts that check the basic functionality of the software
installed in the ``molmatmodel`` conda environment (Ubuntu under WSL2).

Environment
-----------
* Windows 11 + WSL2, Ubuntu
* Miniforge (conda-forge), environment ``molmatmodel`` (Python 3.11)
* conda-forge packages: nwchem, qe (7.6), mopac, ase, xtb, xtb-python, crest, pyscf, gromacs
* pip: mace-torch

Scripts run
-----------
* ``ase-test2.py``
* ``ase_tests-pyscf_mopac.py``
* ``ase_tests-pyscf-mopac-xtb-crest-nwchem-qe.py``
* ``qe/test_qe_ase.py``
* ``qe/test_qe_ase_02.py``

Each script was run as ``python script.py > script.py.log 2>&1``; the ``.log`` files are included.

Results
-------
* PySCF, MOPAC, xTB, CREST, NWChem and Quantum ESPRESSO checks: all passed.
* ``qe/test_qe_ase.py``: Passed 3/3.
* ``qe/test_qe_ase_02.py``: Passed 3/3 (serial ``pw.x``, set in ``qe/qe_command.txt``).

Problem found and solution
--------------------------
The conda-forge ``qe 7.6`` package was installed without its ELPA dependency, so
``pw.x`` failed with::

    pw.x: error while loading shared libraries: libelpa.so.19: cannot open shared object file

Diagnosed with ``ldd $(which pw.x) | grep "not found"`` and fixed by installing the
OpenMPI build of ELPA matching the MPI library in the environment::

    conda install -c conda-forge "elpa=2025.06.001=mpi_openmpi*"

``H.upf`` (required by ``qe/test_qe_ase.py``) was copied from ``materials-modeling/H.upf``
of the course repository.
