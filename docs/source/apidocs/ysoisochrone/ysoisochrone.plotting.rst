:py:mod:`ysoisochrone.plotting`
===============================

.. py:module:: ysoisochrone.plotting

.. autodoc2-docstring:: ysoisochrone.plotting
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`plot_bayesian_results <ysoisochrone.plotting.plot_bayesian_results>`
     - .. autodoc2-docstring:: ysoisochrone.plotting.plot_bayesian_results
          :summary:
   * - :py:obj:`plot_hr_diagram <ysoisochrone.plotting.plot_hr_diagram>`
     - .. autodoc2-docstring:: ysoisochrone.plotting.plot_hr_diagram
          :summary:
   * - :py:obj:`plot_likelihood_1d <ysoisochrone.plotting.plot_likelihood_1d>`
     - .. autodoc2-docstring:: ysoisochrone.plotting.plot_likelihood_1d
          :summary:
   * - :py:obj:`plot_comparison <ysoisochrone.plotting.plot_comparison>`
     - .. autodoc2-docstring:: ysoisochrone.plotting.plot_comparison
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`style <ysoisochrone.plotting.style>`
     - .. autodoc2-docstring:: ysoisochrone.plotting.style
          :summary:

API
~~~

.. py:data:: style
   :canonical: ysoisochrone.plotting.style
   :value: None

   .. autodoc2-docstring:: ysoisochrone.plotting.style

.. py:function:: plot_bayesian_results(log_age_dummy, log_masses_dummy, L, best_age, best_mass, age_unc, mass_unc, source=None, save_fig=False, fig_save_dir='figure', customized_fig_name='')
   :canonical: ysoisochrone.plotting.plot_bayesian_results

   .. autodoc2-docstring:: ysoisochrone.plotting.plot_bayesian_results

.. py:function:: plot_hr_diagram(isochrone, df_prop=None, ax_set=None, ages_to_plot=None, masses_to_plot=None, age_positions=None, mass_rotation=None, age_rotation=None, mass_positions=None, age_xycoords='data', mass_xycoords='data', xlim_set=None, ylim_set=None, no_uncertainties=False, zams_curve=True, bare=False)
   :canonical: ysoisochrone.plotting.plot_hr_diagram

   .. autodoc2-docstring:: ysoisochrone.plotting.plot_hr_diagram

.. py:function:: plot_likelihood_1d(log_masses_dummy, likelihood, best_log_mass, lower_mass, upper_mass, source=None)
   :canonical: ysoisochrone.plotting.plot_likelihood_1d

   .. autodoc2-docstring:: ysoisochrone.plotting.plot_likelihood_1d

.. py:function:: plot_comparison(log_age_idl, masses_idl, logtlogl_interp_py, logtlogl_idl, logtlogl_diff, logtlogl_diff_norm, gridnames=['Python', 'IDL'])
   :canonical: ysoisochrone.plotting.plot_comparison

   .. autodoc2-docstring:: ysoisochrone.plotting.plot_comparison
