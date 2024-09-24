:py:mod:`ysoisochrone.bayesian`
===============================

.. py:module:: ysoisochrone.bayesian

.. autodoc2-docstring:: ysoisochrone.bayesian
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`bayesian_mass_age <ysoisochrone.bayesian.bayesian_mass_age>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.bayesian_mass_age
          :summary:
   * - :py:obj:`derive_stellar_mass_age <ysoisochrone.bayesian.derive_stellar_mass_age>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age
          :summary:
   * - :py:obj:`derive_stellar_mass_age_legacy <ysoisochrone.bayesian.derive_stellar_mass_age_legacy>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age_legacy
          :summary:
   * - :py:obj:`derive_stellar_mass_age_closest_track <ysoisochrone.bayesian.derive_stellar_mass_age_closest_track>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age_closest_track
          :summary:
   * - :py:obj:`derive_stellar_mass_assuming_age <ysoisochrone.bayesian.derive_stellar_mass_assuming_age>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_assuming_age
          :summary:
   * - :py:obj:`derive_stellar_mass_assuming_age_closest_trk <ysoisochrone.bayesian.derive_stellar_mass_assuming_age_closest_trk>`
     - .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_assuming_age_closest_trk
          :summary:

API
~~~

.. py:function:: bayesian_mass_age(log_age_dummy, log_masses_dummy, L, plot=False, source=None, confidence_interval=0.68, verbose=False, save_fig=False, fig_save_dir='figure', customized_fig_name='')
   :canonical: ysoisochrone.bayesian.bayesian_mass_age

   .. autodoc2-docstring:: ysoisochrone.bayesian.bayesian_mass_age

.. py:function:: derive_stellar_mass_age(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68, single_bayesian_for_nolum_target=False)
   :canonical: ysoisochrone.bayesian.derive_stellar_mass_age

   .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age

.. py:function:: derive_stellar_mass_age_legacy(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68, single_bayesian_for_nolum_target=False)
   :canonical: ysoisochrone.bayesian.derive_stellar_mass_age_legacy

   .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age_legacy

.. py:function:: derive_stellar_mass_age_closest_track(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', verbose=False)
   :canonical: ysoisochrone.bayesian.derive_stellar_mass_age_closest_track

   .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_age_closest_track

.. py:function:: derive_stellar_mass_assuming_age(df_prop, assumed_age, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, confidence_interval=0.68, verbose=False, plot=False)
   :canonical: ysoisochrone.bayesian.derive_stellar_mass_assuming_age

   .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_assuming_age

.. py:function:: derive_stellar_mass_assuming_age_closest_trk(df_prop, assumed_age, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', verbose=False)
   :canonical: ysoisochrone.bayesian.derive_stellar_mass_assuming_age_closest_trk

   .. autodoc2-docstring:: ysoisochrone.bayesian.derive_stellar_mass_assuming_age_closest_trk
