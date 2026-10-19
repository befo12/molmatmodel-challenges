=====================================================
Challenge II.7 - Work function of graphene (ASE + QE)
=====================================================

Task
----
Work function of graphene: planar-averaged electrostatic potential and work function with ASE + QE.
Challenge (course overview): "Simply redo the calculations and save the output files." In addition,
the run was repeated without the 2D Coulomb cutoff (see below).

Runs
----
Course script ``work_function.py`` (SCF 100 Ry, k = 27x27x1 -> ``pp.x`` electrostatic potential
(plot_num = 11) -> ``average.x`` planar and macroscopic average along z), run twice:

* ``with_2D/`` - with ``assume_isolated = '2D'`` (as in the course reference output)
* ``no_2D/``   - without it (the line is commented out in the course script)

``wf_analysis.py`` takes the vacuum level as the mean planar-averaged potential 3.5-5.0 A away from
the graphene layer (z = 7.5 A), where the potential is flat, and computes W = V_vac - E_F.
Figure: ``work_function_comparison.png``.

Results
-------
::

    Run                            E_F/eV  V_vac/eV    W/eV  V(z=0)/eV
    ------------------------------------------------------------------
    with assume_isolated = 2D     -4.2405    0.0020   4.243     14.585
    without assume_isolated       -1.7174    2.5230   4.240      2.523
    
    Literature: graphene W ~ 4.5-4.6 eV (experiment), ~4.2-4.3 eV (PBE)

Discussion
----------
* The with_2D run reproduces the course reference (E_F = -4.2405 eV, ``reference_outputs/``); the
  Fermi level written in the ``plot_potential.gp`` of the course directory (-1.7174 eV) corresponds
  to the run without the 2D cutoff.
* With the 2D cutoff the potential in the vacuum is zero by construction (V_vac = 0.002 eV), so
  W = -E_F directly.
* The two runs give Fermi levels differing by 2.5 eV, but the same work function (4.243 vs
  4.240 eV). In a periodic calculation the zero of the electrostatic potential is arbitrary,
  so absolute eigenvalues / E_F have no physical meaning; only the difference to the vacuum
  level does. W is therefore the physically meaningful, reference-independent quantity.
* With the 2D cutoff the potential shows large unphysical peaks at the cell boundaries
  (V(z=0) = 14.6 eV) caused by the truncated Coulomb interaction; without it the potential is
  flat throughout the vacuum region (V(z=0) = V_vac = 2.52 eV). For a symmetric single layer the
  2D cutoff is not needed for the work function.
* The computed W = 4.24 eV agrees with literature PBE values for free-standing graphene
  (~4.2-4.3 eV) and is slightly below experimental values (~4.5-4.6 eV), which depend on
  substrate, doping and adsorbates; GGA functionals typically underestimate work functions slightly.
