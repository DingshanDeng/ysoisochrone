:py:mod:`ysoisochrone.registry`
===============================

.. py:module:: ysoisochrone.registry

.. autodoc2-docstring:: ysoisochrone.registry
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`normalize_track_name <ysoisochrone.registry.normalize_track_name>`
     - .. autodoc2-docstring:: ysoisochrone.registry.normalize_track_name
          :summary:
   * - :py:obj:`invalid_track_message <ysoisochrone.registry.invalid_track_message>`
     - .. autodoc2-docstring:: ysoisochrone.registry.invalid_track_message
          :summary:
   * - :py:obj:`list_valid_canonical_tracks <ysoisochrone.registry.list_valid_canonical_tracks>`
     - .. autodoc2-docstring:: ysoisochrone.registry.list_valid_canonical_tracks
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`TRACK_ALIASES <ysoisochrone.registry.TRACK_ALIASES>`
     - .. autodoc2-docstring:: ysoisochrone.registry.TRACK_ALIASES
          :summary:
   * - :py:obj:`TRACK_DISPLAY <ysoisochrone.registry.TRACK_DISPLAY>`
     - .. autodoc2-docstring:: ysoisochrone.registry.TRACK_DISPLAY
          :summary:

API
~~~

.. py:data:: TRACK_ALIASES
   :canonical: ysoisochrone.registry.TRACK_ALIASES
   :type: dict[str, list[str]]
   :value: None

   .. autodoc2-docstring:: ysoisochrone.registry.TRACK_ALIASES

.. py:data:: TRACK_DISPLAY
   :canonical: ysoisochrone.registry.TRACK_DISPLAY
   :type: list[str]
   :value: ['Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', "PARSEC_v2p0 (same as 'PARSEC')", 'PARSEC_v1p2'...

   .. autodoc2-docstring:: ysoisochrone.registry.TRACK_DISPLAY

.. py:function:: normalize_track_name(track_type: str) -> str
   :canonical: ysoisochrone.registry.normalize_track_name

   .. autodoc2-docstring:: ysoisochrone.registry.normalize_track_name

.. py:function:: invalid_track_message(bad_track) -> str
   :canonical: ysoisochrone.registry.invalid_track_message

   .. autodoc2-docstring:: ysoisochrone.registry.invalid_track_message

.. py:function:: list_valid_canonical_tracks() -> list[str]
   :canonical: ysoisochrone.registry.list_valid_canonical_tracks

   .. autodoc2-docstring:: ysoisochrone.registry.list_valid_canonical_tracks
