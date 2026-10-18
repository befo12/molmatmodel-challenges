=======================================================================
Challenge I.8 - UO2I2(OH2)2: geometry optimization with MACE and NWChem
=======================================================================

Task
----
Redo the calculations of Exercise I.8 (uranyl complex UO2I2(OH2)2, structure from
doi:10.1021/ja030260r, Fig. 2) and save the output files. Course abstract: ``readme_course.rst``.

Calculations (outputs in ``*.log``)
-----------------------------------
1. MACE optimization: ``mace/uo2i2_core_mace-geopt.py`` (9 s).
2. NWChem B3LYP single point, Stuttgart RLC ECP (U, I), 3-21G* (O, H):
   ``nwchem/uo2i2water2_b3lyp_stuttgart_rlc_ecp.nw`` (6 MPI, 82 s), E = -377.647069 Hartree.
3. NWChem B3LYP geometry optimization, same basis/ECP:
   ``nwchem/geopt/uo2i2water2_ecp_b3lyp_geopt.nw`` (6 MPI, 133 s, converged).

``bonds_u.py`` extracts the bond lengths from the final NWChem geometry.

Results (average bond lengths, Angstrom; linear O=U=O, I-U-I, Ow-U-Ow)
------------------------------------------------------------------------
::

    Method                              U=O      U-I      U-O(water)
    -----------------------------------------------------------------
    Paper / initial structure          1.773    3.027    2.318
    NWChem B3LYP/ECP (this work)       1.768    3.066    2.427
    NWChem B3LYP/ECP (course ref.)     1.767    3.065    2.432
    MACE-MPA-0 medium (this work)      1.794    2.953      -
    MACE osaka26-small (course ref.)   1.790    2.866      -

Discussion
----------
* The NWChem B3LYP/ECP optimization reproduces the course result within 0.005 A.
* The course MACE model (mace-osaka26-small) was not available, so the script used the
  foundation model MACE-MPA-0 (medium), which covers U and I. It gives U=O close to the
  paper (+0.02 A) and a better U-I distance (-0.07 A) than the osaka26 model (-0.16 A).
* DFT/ECP overestimates and MACE underestimates the paper's U-I distance. As noted in
  the course abstract, spin-orbit coupling and a more rigorous relativistic treatment
  are expected to matter for actinide-halogen bonds.
* MACE takes seconds, DFT minutes: MACE is a useful pre-optimizer before DFT.
