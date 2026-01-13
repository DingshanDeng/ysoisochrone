#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/13/2026

from __future__ import annotations

# Canonical -> aliases accepted from user
TRACK_ALIASES: dict[str, list[str]] = {
    "baraffe2015": ["baraffe2015", "baraffe"],
    "feiden2016": ["feiden2016", "feiden2016_nob", "feiden2016_nonmagnetic", "feiden"],
    "feiden2016_magnetic": ["feiden2016_b", "feiden2016_magnetic", "feiden_magnetic", "feiden_b"],
    "parsec_v2p0": ["parsec", "parsec_v2p0"],
    "parsec_v1p2": ["parsec_v1p2"],
    "mist_v1p2": ["mist", "mist_v1p2"],
    "siess2000": ["siess2000", "siess"],
    "spots0169": ["spots0169"],
    "spots0339": ["spots0339"],
    "spots0508": ["spots0508"],
    "spots0847": ["spots0847"],
    "pisa": ["pisa", "pisa2011"],
    "customize": ["customize", "custom", "user", "usergrid"],
}

# What you want to show in user-facing error messages
TRACK_DISPLAY: list[str] = [
    "Baraffe2015",
    "Feiden2016",
    "Feiden2016_magnetic",
    "PARSEC_v2p0 (same as 'PARSEC')",
    "PARSEC_v1p2",
    "MIST_v1p2 (same as 'MIST')",
    "siess2000",
    "spots0169",
    "spots0339",
    "spots0508",
    "spots0847",
    "pisa",
    "customize",
]

def normalize_track_name(track_type: str) -> str:
    """
    Map a user-provided track_type to a canonical key used internally.
    Raises a single standardized ValueError if unknown.
    """
    if track_type is None:
        raise ValueError(invalid_track_message(track_type))

    t = str(track_type).strip().lower()

    # direct canonical match
    if t in TRACK_ALIASES:
        return t

    # alias match
    for canonical, aliases in TRACK_ALIASES.items():
        if t in aliases:
            return canonical

    raise ValueError(invalid_track_message(track_type))


def invalid_track_message(bad_track) -> str:
    choices = ", ".join([f"'{x}'" for x in TRACK_DISPLAY])
    return (
        f"Invalid model: {bad_track}. Please choose from {choices}. "
        "If you want to use model='customize', provide the absolute path to the "
        "isochrone matrix file via load_file=... (please read the manual/tutorial notebook on how to use this option)."
    )


def list_valid_canonical_tracks() -> list[str]:
    """Canonical keys only (what set_tracks dispatches on)."""
    return list(TRACK_ALIASES.keys())