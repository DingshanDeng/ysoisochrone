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
date: 26 September 2024
bibliography: paper.bib
---

# Background and Methods

There has been a long history of estimating stellar age and masses from the stellar evolutionary models (e.g., @Siess_2000, @Feiden_2016, @Baraffe_2015), and the Bayesian inference has also been implemented in the early works (e.g., @Jorgensen_n_Lindergren_2005, @Gennaro_2012, @Andrews_2013, @Pascucci_2016). Our primary method is a Bayesian inference approach to estimate the stellar masses, ages, and associated uncertainties by comparing their stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties with the stellar evolutionary models. Uniform priors are assumed, and the likelihood functions are defined following [@Andrews_2013]: 
$$
\mathcal{L}(T_{i}, L_{i} | T_{\rm obs}, L_{\rm obs}) = \frac{1}{2\pi \sigma_{T_{\rm obs}} \sigma_{L_{\rm obs}}} \exp\left( -\frac{1}{2} \left[ \frac{(T_{\rm obs} - T_{i})^2}{\sigma_{T_{\rm obs}}^2} + \frac{(L_{\rm obs} - L_{i})^2}{\sigma_{L_{\rm obs}}^2} \right] \right), \tag{1}
$$
where the $T$ and $L$ are the effective temperature and bolometric luminosity, respectively. $T_i, L_i$ are the values from the evolutionary model grids, and $T_{\rm obs}, L_{\rm obs}$ are the observed values for each target with their uncertainties described as $\sigma_{T_{\rm obs}}, \sigma_{L_{\rm obs}}$. 

Our method also uses a combination of the pre-main-sequence evolutionary tracks from  [@Feiden_2016] and [@Baraffe_2015] for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This aligns with the choice made by [@Pascucci_2016], [@Manara_2023_PPVII], and so on. `ysoisochrone` also has an algorithm to find the line of zero-age-main-sequence (ZAMS) stars automatically from the evolutionary tracks and cut the evolutionary models beyond ZAMS, and therefore this method could be extended to the stars entering main-sequence phase (e.g., @Fernandes_2023). This algorithm also enables `ysoisochrone` to handle other stellar evolutionary models that are not only focused on pre-main-sequence stars, such as PARSEC tracks [@Bressan_2012_PARSEC].

We also provide two other ways to estimate the stellar masses and ages from these isochrones. 
- The classical method that compare the position of the pre-main-sequence stars on the Hertzsprung-Russel Diagram with different stellar evolutionary models, and the closest point (based on $T_{\rm eff}$ and $L_{\rm bol}$) from the model grids are assigned as the mass and age for each target. 
- In some cases, when a good measurement of stellar luminosity is unavailable,  we provide an option to set up the assumed age to derive the stellar mass. Some examples when this method is useful includes: targets that are very young and exceptionally bright; and the targets with an edge-on disk so that their $L_{\rm bol}$ cannot be measured.

# Statement of Need and Code Summary

`ysoisochrone` is a `Python3` package that handles the isochrones for young-stellar-objects. One of the primary goals of this code is to derive the stellar mass and ages from the isochrones. There have been a lot of works in the literature on deriving the stellar masses and ages comparing with stellar evolutionary models including varies of method (e.g., @Jorgensen_n_Lindergren_2005, @Gennaro_2012, @Andrews_2013, @Pascucci_2016, @Manara_2023_PPVII) and evolutionary models (e.g., @Feiden_2016, @Baraffe_2015, @Bressan_2012_PARSEC). However, different stellar evolutionary models provide different style of output, and different methods were also adopted in the literature to derive the stellar masses and ages from those models. `ysoisochrone` provides a uniform platform to handle different evolutionary models with the classical and Bayesian inference methods that could be applied to pre-main-sequence and main-sequence stars to derive stellar masses and ages from these models. `ysoisochrone` provides this functionality, along with tutorials and documentation to guide users to easily utilize different methods and models to quickly estimate the stellar masses and age for the targets of interests. 

# Acknowledgements

We acknowledge help from xxx. (Maybe Greg and Sean? As well as the useful discussions we had with AGE-PRO members? Of course help from our group members). Also acknowledge the funding source.

# References
