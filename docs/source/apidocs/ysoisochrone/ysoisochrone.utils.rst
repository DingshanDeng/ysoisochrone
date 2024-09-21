:py:mod:`ysoisochrone.utils`
============================

.. py:module:: ysoisochrone.utils

.. autodoc2-docstring:: ysoisochrone.utils
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`unc_log10 <ysoisochrone.utils.unc_log10>`
     - .. autodoc2-docstring:: ysoisochrone.utils.unc_log10
          :summary:
   * - :py:obj:`get_likelihood_andrews2013 <ysoisochrone.utils.get_likelihood_andrews2013>`
     - .. autodoc2-docstring:: ysoisochrone.utils.get_likelihood_andrews2013
          :summary:
   * - :py:obj:`download_file_simple <ysoisochrone.utils.download_file_simple>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_file_simple
          :summary:
   * - :py:obj:`download_file <ysoisochrone.utils.download_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_file
          :summary:
   * - :py:obj:`extract_tarball <ysoisochrone.utils.extract_tarball>`
     - .. autodoc2-docstring:: ysoisochrone.utils.extract_tarball
          :summary:
   * - :py:obj:`download_baraffe_tracks <ysoisochrone.utils.download_baraffe_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_baraffe_tracks
          :summary:
   * - :py:obj:`read_baraffe_file <ysoisochrone.utils.read_baraffe_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_baraffe_file
          :summary:
   * - :py:obj:`download_feiden_trk_tracks <ysoisochrone.utils.download_feiden_trk_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_feiden_trk_tracks
          :summary:
   * - :py:obj:`read_feiden_trk_file <ysoisochrone.utils.read_feiden_trk_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_feiden_trk_file
          :summary:
   * - :py:obj:`download_feiden_iso_tracks <ysoisochrone.utils.download_feiden_iso_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_feiden_iso_tracks
          :summary:
   * - :py:obj:`read_feiden_iso_file <ysoisochrone.utils.read_feiden_iso_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_feiden_iso_file
          :summary:
   * - :py:obj:`download_parsec_v1p2_tracks <ysoisochrone.utils.download_parsec_v1p2_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_parsec_v1p2_tracks
          :summary:
   * - :py:obj:`read_parsec_v1p2_dat_file <ysoisochrone.utils.read_parsec_v1p2_dat_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_parsec_v1p2_dat_file
          :summary:
   * - :py:obj:`download_parsec_v2p0_tracks <ysoisochrone.utils.download_parsec_v2p0_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_parsec_v2p0_tracks
          :summary:
   * - :py:obj:`read_parsec_v2p0_tab_file <ysoisochrone.utils.read_parsec_v2p0_tab_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_parsec_v2p0_tab_file
          :summary:
   * - :py:obj:`download_mist_v1p2_eep_tracks <ysoisochrone.utils.download_mist_v1p2_eep_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_mist_v1p2_eep_tracks
          :summary:
   * - :py:obj:`download_mist_v1p2_iso_tracks <ysoisochrone.utils.download_mist_v1p2_iso_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.utils.download_mist_v1p2_iso_tracks
          :summary:
   * - :py:obj:`read_mist_v1p2_iso_file <ysoisochrone.utils.read_mist_v1p2_iso_file>`
     - .. autodoc2-docstring:: ysoisochrone.utils.read_mist_v1p2_iso_file
          :summary:
   * - :py:obj:`create_meshgrid <ysoisochrone.utils.create_meshgrid>`
     - .. autodoc2-docstring:: ysoisochrone.utils.create_meshgrid
          :summary:
   * - :py:obj:`save_as_mat <ysoisochrone.utils.save_as_mat>`
     - .. autodoc2-docstring:: ysoisochrone.utils.save_as_mat
          :summary:
   * - :py:obj:`compare_grids <ysoisochrone.utils.compare_grids>`
     - .. autodoc2-docstring:: ysoisochrone.utils.compare_grids
          :summary:

API
~~~

.. py:function:: unc_log10(x, err_x)
   :canonical: ysoisochrone.utils.unc_log10

   .. autodoc2-docstring:: ysoisochrone.utils.unc_log10

.. py:function:: get_likelihood_andrews2013(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL)
   :canonical: ysoisochrone.utils.get_likelihood_andrews2013

   .. autodoc2-docstring:: ysoisochrone.utils.get_likelihood_andrews2013

.. py:function:: download_file_simple(url, save_path)
   :canonical: ysoisochrone.utils.download_file_simple

   .. autodoc2-docstring:: ysoisochrone.utils.download_file_simple

.. py:function:: download_file(url, save_path)
   :canonical: ysoisochrone.utils.download_file

   .. autodoc2-docstring:: ysoisochrone.utils.download_file

.. py:function:: extract_tarball(tar_file_path, extract_dir)
   :canonical: ysoisochrone.utils.extract_tarball

   .. autodoc2-docstring:: ysoisochrone.utils.extract_tarball

.. py:function:: download_baraffe_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_baraffe_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_baraffe_tracks

.. py:function:: read_baraffe_file(file_path)
   :canonical: ysoisochrone.utils.read_baraffe_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_baraffe_file

.. py:function:: download_feiden_trk_tracks(save_dir='isochrones_data', download_original_trks=False)
   :canonical: ysoisochrone.utils.download_feiden_trk_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_feiden_trk_tracks

.. py:function:: read_feiden_trk_file(feiden_dir)
   :canonical: ysoisochrone.utils.read_feiden_trk_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_feiden_trk_file

.. py:function:: download_feiden_iso_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_feiden_iso_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_feiden_iso_tracks

.. py:function:: read_feiden_iso_file(feiden_dir)
   :canonical: ysoisochrone.utils.read_feiden_iso_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_feiden_iso_file

.. py:function:: download_parsec_v1p2_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_parsec_v1p2_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_parsec_v1p2_tracks

.. py:function:: read_parsec_v1p2_dat_file(parsec_dir)
   :canonical: ysoisochrone.utils.read_parsec_v1p2_dat_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_parsec_v1p2_dat_file

.. py:function:: download_parsec_v2p0_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_parsec_v2p0_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_parsec_v2p0_tracks

.. py:function:: read_parsec_v2p0_tab_file(parsec_dir)
   :canonical: ysoisochrone.utils.read_parsec_v2p0_tab_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_parsec_v2p0_tab_file

.. py:function:: download_mist_v1p2_eep_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_mist_v1p2_eep_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_mist_v1p2_eep_tracks

.. py:function:: download_mist_v1p2_iso_tracks(save_dir='isochrones_data')
   :canonical: ysoisochrone.utils.download_mist_v1p2_iso_tracks

   .. autodoc2-docstring:: ysoisochrone.utils.download_mist_v1p2_iso_tracks

.. py:function:: read_mist_v1p2_iso_file(mist_iso_file)
   :canonical: ysoisochrone.utils.read_mist_v1p2_iso_file

   .. autodoc2-docstring:: ysoisochrone.utils.read_mist_v1p2_iso_file

.. py:function:: create_meshgrid(data_points, min_age=0.5, max_age=500.0)
   :canonical: ysoisochrone.utils.create_meshgrid

   .. autodoc2-docstring:: ysoisochrone.utils.create_meshgrid

.. py:function:: save_as_mat(masses, log_age, logtlogl, save_path)
   :canonical: ysoisochrone.utils.save_as_mat

   .. autodoc2-docstring:: ysoisochrone.utils.save_as_mat

.. py:function:: compare_grids(loaded_data_py, loaded_data_idl, gridnames=['Python', 'IDL'], plot=True)
   :canonical: ysoisochrone.utils.compare_grids

   .. autodoc2-docstring:: ysoisochrone.utils.compare_grids
