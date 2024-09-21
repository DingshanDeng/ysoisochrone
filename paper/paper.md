---
title: 'ysoisochrone: A Python package to handle the isochrones for young stellar objects'
tags:
  - Python
  - astronomy
authors:
  - name: Dingshan Deng
    orcid: 0000-0003-0777-7392
    affiliation: 1
  - name: Ilaria Pascucci
    orcid: 0000-0001-7962-1683
    affiliation: 1
  - name: Rachel B. Fernandes
    orcid: 0000-0002-3853-7327
    affiliation: 2
affiliations:
 - name: Lunar and Planetary Laboratory, the University of Arizona, Tucson, AZ 85721, USA
   index: 1
 - name: Department of Astronomy & Astrophysics, Center for Exoplanets and Habitable Worlds, The Pennsylvania State University, University Park, PA 16802
   index: 2
date: 21 September 2024
bibliography: paper.bib
---

# Background

*Here we need to describe the background and the statement of need for this software*

# Code Summary

`ysoisochrone` is a Python package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.
Our primary method is a Bayesian inference approach that introduced in [@Pascucci_2016] to estimate the stellar masses, ages, and associated uncertainties from the stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties. Uniform priors are assumed, and the likelihood functions are defined following [@Andrews_2013]. The pre-main-sequence evolutionary tracks from both [@Feiden_2016] and [@Baraffe_2015] are adopted for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This method was also adopted in other works (e.g., [@Fernandes_2023] and ALMA large program AGE-PRO). 

We also provide two other ways to estimate the stellar masses and ages from these isochrones: (b) In some cases, when a good measurement of stellar luminosity is unavailable,  we also provide an option to set up the assumed age to derive the stellar mass from the Bayesian inference. (c) A simple approach to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target.

# Methods

*Here we describe the methods that are included in this software: including but not limited to the Bayesian inference approach that was devloped in [@Pascucci_2016], how we define and format the evolutionatry tracks downloaded from online sources*.

# Acknowledgements

# References
