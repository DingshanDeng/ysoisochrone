:py:mod:`ysoisochrone.isochrone`
================================

.. py:module:: ysoisochrone.isochrone

.. autodoc2-docstring:: ysoisochrone.isochrone
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`Isochrone <ysoisochrone.isochrone.Isochrone>`
     - .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone
          :summary:

API
~~~

.. py:class:: Isochrone(data_dir=None)
   :canonical: ysoisochrone.isochrone.Isochrone

   .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone

   .. rubric:: Initialization

   .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.__init__

   .. py:method:: prepare_baraffe_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.prepare_baraffe_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.prepare_baraffe_tracks

   .. py:method:: prepare_feiden_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.prepare_feiden_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.prepare_feiden_tracks

   .. py:method:: prepare_parsecv1p2_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.prepare_parsecv1p2_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.prepare_parsecv1p2_tracks

   .. py:method:: prepare_parsecv2p0_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.prepare_parsecv2p0_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.prepare_parsecv2p0_tracks

   .. py:method:: prepare_mistv1p2_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.prepare_mistv1p2_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.prepare_mistv1p2_tracks

   .. py:method:: load_baraffe2015_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_baraffe2015_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_baraffe2015_tracks

   .. py:method:: load_feiden2016_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_feiden2016_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_feiden2016_tracks

   .. py:method:: load_feiden2016_magnetic_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_feiden2016_magnetic_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_feiden2016_magnetic_tracks

   .. py:method:: load_parsecv1p2_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_parsecv1p2_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_parsecv1p2_tracks

   .. py:method:: load_parsecv2p0_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_parsecv2p0_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_parsecv2p0_tracks

   .. py:method:: load_mistv1p2_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_mistv1p2_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_mistv1p2_tracks

   .. py:method:: load_siess2000_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_siess2000_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_siess2000_tracks

   .. py:method:: load_spots0000_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_spots0000_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_spots0000_tracks

   .. py:method:: load_spots0169_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_spots0169_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_spots0169_tracks

   .. py:method:: load_spots0339_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_spots0339_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_spots0339_tracks

   .. py:method:: load_spots0508_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_spots0508_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_spots0508_tracks

   .. py:method:: load_spots0847_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_spots0847_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_spots0847_tracks

   .. py:method:: load_pisa_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.load_pisa_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_pisa_tracks

   .. py:method:: load_tracks_from_customize_matrix(load_file)
      :canonical: ysoisochrone.isochrone.Isochrone.load_tracks_from_customize_matrix

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.load_tracks_from_customize_matrix

   .. py:method:: set_tracks_legacy(track_type, load_file='')
      :canonical: ysoisochrone.isochrone.Isochrone.set_tracks_legacy

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.set_tracks_legacy

   .. py:method:: set_tracks(track_type, load_file='', verbose=False)
      :canonical: ysoisochrone.isochrone.Isochrone.set_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.set_tracks

   .. py:method:: get_tracks()
      :canonical: ysoisochrone.isochrone.Isochrone.get_tracks

      .. autodoc2-docstring:: ysoisochrone.isochrone.Isochrone.get_tracks
