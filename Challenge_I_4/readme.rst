=================================================
Challenge I.4 - Testing the MACE installation
=================================================

Task
----
Run all MACE testing scripts from the course repository
(``molecular-modeling/ase_mace/mace``) on my computer.

Preparation
-----------
``tests/quick_test.py`` expects the MACE-MPA-0 medium model in ``~/.cache/mace/macempa0mediummodel``.
It was downloaded with::

    python -c "from mace.calculators import mace_mp; mace_mp(model='medium-mpa-0')"

Scripts run (all finished with exit code 0, outputs in ``*.log``)
------------------------------------------------------------------
* ``tests/quick_test.py`` - single-point energies of small molecules
* ``tests/model_analyzer.py`` - analysis of installed models
* ``tests/model_element_detector.py`` - elements covered by each model (89 elements for MACE-MP)
* ``tests/check_mace_ml_installation.py`` - installation check
* ``simple/water_mace.py`` - H2O geometry optimization with MACE
* ``simple/water_mace_emt_01.py`` - H2O, MACE vs EMT

Results
-------
``quick_test.py`` (MACE-MPA-0 medium, CPU)::

         H2O: -13.785927 eV
         CH4: -23.166403 eV
         NH3: -18.995643 eV
         CO2: -22.545622 eV
        C6H6: -75.069722 eV
          N2: -16.410813 eV

These energies are identical (to 6 decimals) with the reference output of the course.

``water_mace.py``: optimized O-H bond length 0.9728 A (experiment 0.958 A).

``water_mace_emt_01.py``: MACE is ~9x more accurate than EMT for the O-H bond length and
~17x more accurate for the H-O-H angle.

Environment: Windows + WSL2 Ubuntu, conda env ``molmatmodel``, mace-torch 0.3.16, CPU only.
