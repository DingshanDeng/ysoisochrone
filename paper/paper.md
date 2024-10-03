---
title: 'ysoisochrone: A Python package to estimate masses and ages for YSOs'
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
	affiliation: 2, 3, 4
affiliations:
 - name: Lunar and Planetary Laboratory, the University of Arizona, Tucson, AZ 85721, USA
   index: 1
 - name: President’s Postdoctoral Fellow
   index: 2
 - name: Department of Astronomy \& Astrophysics, 525 Davey Laboratory, The Pennsylvania State University, University Park, PA 16802, USA
   index: 3
 - name: Center for Exoplanets and Habitable Worlds, 525 Davey Laboratory, The Pennsylvania State University, University Park, PA 16802, USA
   index: 4
date: 03 October 2024
bibliography: paper.bib
---

# Background and Methods
There has been a long history of estimating stellar age and masses from the stellar evolutionary models (e.g., @Siess_2000, @Feiden_2016, @Baraffe_2015). Different methods have been employed, from finding the closest track to an object's luminosity and temperature (e.g., @Manara_2023_PPVII) to employing a Bayesian approach which enables estimating uncertainties on the inferred ages and masses (e.g., @Jorgensen_n_Lindergren_2005, @Gennaro_2012, @Andrews_2013). Our primary method is a Bayesian inference approach, and the `Python` code builds on the `IDL` version developed in @Pascucci_2016. The code estimates the stellar masses, ages, and associated uncertainties by comparing their stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties with different stellar evolutionary models, including those specifically developed for YSOs. As assumed in previous literature, we adopt uniforms priors, and the likelihood functions are defined following:
$$
\mathcal{L}(T_{i}, L_{i} | T_{\rm obs}, L_{\rm obs}) = \frac{1}{2\pi \sigma_{T_{\rm obs}} \sigma_{L_{\rm obs}}} \exp\left( -\frac{1}{2} \left[ \frac{(T_{\rm obs} - T_{i})^2}{\sigma_{T_{\rm obs}}^2} + \frac{(L_{\rm obs} - L_{i})^2}{\sigma_{L_{\rm obs}}^2} \right] \right), \tag{1}
$$
where the $T$ and $L$ are the effective temperature and bolometric luminosity, respectively. $T_i, L_i$ are the values from the evolutionary model grids, and $T_{\rm obs}, L_{\rm obs}$ are the observed values for each target with their uncertainties ($1\,\sigma$ from the assumed Gaussian distribution) described as $\sigma_{T_{\rm obs}}, \sigma_{L_{\rm obs}}$.

Our method also uses a combination of the pre-main-sequence evolutionary tracks from @Feiden_2016 and @Baraffe_2015 for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This aligns with the choice as initially suggested in @Pascucci_2016 to derive the stellar masses of chameleon I young stellar objects (YSOs). `ysoisochrone` also has a new algorithm to find the zero age main sequence (ZAMS) automatically so that post-main sequence tracks are not included when interpolating to a finer grid of evolutionary tracks (e.g., @Fernandes_2023). This algorithm also enables `ysoisochrone` to handle other stellar evolutionary models that are not only focused on pre-main-sequence stars, such as PARSEC tracks [@Bressan_2012_PARSEC]. User-developed evolutionary tracks can be also utilized when provided in the specific format described in the code documentation.

We also provide two other ways to estimate the stellar masses and ages from these isochrones.
- The classical method that finds the closest point from the isochrones for each YSOs based on their $T_{\rm eff}$ and $L_{\rm bol}$ (the uncertainties are ignored in this method).
- In some cases, when a good measurement of the stellar luminosity is unavailable,  we provide an option to set up the assumed age and then derive the stellar mass. Some examples when this method is useful include: targets that are very young and exceptionally bright; and targets with an edge-on disk so that the stellar $L_{\rm bol}$ is significantly underestimated.

# Statement of Need

`ysoisochrone` is a `Python3` package that utilizes stellar evolutionary tracks to estimate stellar masses and ages of pre-main sequence stars with a Bayesian framework. While several papers in the literature utilize this method (e.g.,), an open-source code for YSOs is not available. `ysoisochrone` fills this gap. The code provides a uniform platform to handle different evolutionary models along with tutorials and detailed documentation for first users. 

# Acknowledgements

We thank Greg Herczeg for suggesting the blending of the Feiden and Baraffe evolutionary tracks to handle a large range of stellar masses. D.D. and I.P. acknowledge support from Collaborative NSF Astronomy \& Astrophysics Research grant (ID: 2205870).

# References
