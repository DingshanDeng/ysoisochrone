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
    affiliation: "2, 3, 4"
affiliations:
 - name: Lunar and Planetary Laboratory, the University of Arizona, Tucson, AZ 85721, USA
   index: 1
 - name: President’s Postdoctoral Fellow
   index: 2
 - name: Department of Astronomy \& Astrophysics, 525 Davey Laboratory, The Pennsylvania State University, University Park, PA 16802, USA
   index: 3
 - name: Center for Exoplanets and Habitable Worlds, 525 Davey Laboratory, The Pennsylvania State University, University Park, PA 16802, USA
   index: 4
date: 22 Janurary 2025
bibliography: paper.bib
---

# Background and Methods
There has been a long history of estimating **stellar ages and masses** from the stellar evolutionary models [e.g., @Baraffe_2015; @Feiden_2016; @Siess_2000]. Different methods have been employed, from finding the closest track to an object's luminosity and temperature [e.g., @Manara_2023_PPVII] to employing a Bayesian approach which enables estimating uncertainties on the inferred ages and masses [e.g., @Andrews_2013; @Gennaro_2012;  @Jorgensen_n_Lindergren_2005]. Our primary method is a Bayesian inference approach, and the `Python` code builds on the `IDL` version developed by @Pascucci_2016. **The code estimates the stellar mass, age, and associated uncertainties by comparing a star's effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$)**, and their uncertainties with different stellar evolutionary models, including those specifically developed for young stellar objects **(YSOs)**. **The conditional likelihood function assumes log-uniform priors and can be written as:**
$$
\begin{aligned}
&\mathcal{L}(\log T_{i}, \log L_{i} \mid \log T_{\rm obs}, \log L_{\rm obs}) = 
\frac{1}{2\pi \sigma_{\log T_{\rm obs}} \sigma_{\log L_{\rm obs}}} \\
&\quad \times \exp\left( -\frac{1}{2} \left[ 
\frac{(\log T_{\rm obs} - \log T_{i})^2}{\sigma_{\log T_{\rm obs}}^2} 
+ \frac{(\log L_{\rm obs} - \log L_{i})^2}{\sigma_{\log L_{\rm obs}}^2} 
\right] \right),
\end{aligned} \tag{1}
$$
where the $T$ and $L$ are the effective temperature and bolometric luminosity, respectively. $T_i, L_i$ are the values from the evolutionary model grids, and $T_{\rm obs}, L_{\rm obs}$ are the observed values for each target with their uncertainties ($1\,\sigma$ from the assumed Gaussian distribution **log-scale**) described as $\sigma_{\log T_{\rm obs}}, \sigma_{\log L_{\rm obs}}$.
**In this first released version, we assume log-uniform priors for $T$ and $L$ in this likelihood function following the `IDL` code used in @Pascucci_2016. This is because both initial mass function of stars and their evolutionary timescales imply that the occurrence of stars decreases as a function of $T_{\rm eff}$ and $L_{\rm bol}$, which is represented by the log-uniform priors. Different likelihood function can be added in the future versions.**

**We choose $T_{\rm eff}$ and $L_{\rm bol}$ to estimate the stellar age and mass because extinction is significant for young stars especially when embedded in the natal cloud. Although the $T_{\rm eff}$ and $L_{\rm bol}$ are not directly observed quantities, they are the two main quantities that evolutionary models can be compared with. When median or high-resolution spectroscopy is employed on individual targets, $T_{\rm eff}$ and $L_{\rm bol}$ can be well determined, and the best estimates for YSOs are from works where a stellar spectrum is fitted simutaneously with extinction and accretional heating [e.g., @alcala_x-shooter_2017]. To ensure the best results, we recommend using $T_{\rm eff}$ and $L_{\rm bol}$ (with their uncertainties) that are derived simutaneously through spectroscopy.**

Our method uses a combination of the pre-main-sequence **non-magnetic** evolutionary tracks from @Feiden_2016 and @Baraffe_2015 for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This aligns with the choice **as initially suggested in @herczeg_empirical_2015 and @Pascucci_2016, who used the combination of these tracks to derive the stellar masses of Chamaeleon I YSOs, and has also been tested and adopted in some recent works [e.g., @Fernandes_2023; @Manara_2023_PPVII; @simon_2019]**. `ysoisochrone` also has a new algorithm to find the zero age main sequence (ZAMS) automatically so that post-main sequence tracks are not included when interpolating to a finer grid of evolutionary tracks [e.g., @Fernandes_2023]. This algorithm also enables `ysoisochrone` to handle other stellar evolutionary models that are not only focused on pre-main-sequence stars, such as PARSEC tracks [@Bressan_2012_PARSEC]. **We note that there have been recent development on the stellar evolutionary models, but some of those updated models have not yet been released to the public. Therefore,** user-developed evolutionary tracks can be also utilized **in `ysoisochrone`** when provided in the specific format described in the code documentation. **We also aim to include those updated models once they are publicly available.**

We also provide two other ways to estimate the stellar masses and ages from these isochrones.

1. In some cases, when a good measurement of the stellar luminosity is unavailable,  we provide an option to set up the assumed age and then derive the stellar mass. Some examples when this method is useful include: targets that are very young and exceptionally bright; and targets with an edge-on disk so that the stellar $L_{\rm bol}$ is significantly underestimated. 
   
2. The classical method that finds the closest point from the isochrones for each YSOs based on their $T_{\rm eff}$ and $L_{\rm bol}$. **We note that this stand alone function is primarily used for verification purposes against literature [e.g., @Manara_2023_PPVII; @Pascucci_2016] as it does not provide uncertainties**. 

# Statement of Need

**At this moment, there are a few existing tools and packages that can be used to handle stellar evolutionary tracks and to estimate stellar mass and age for pre-main sequence stars. For example, [`isochrones`](https://github.com/timothydmorton/isochrones) provides a `Python` interface to access the [MIST](https://waps.cfa.harvard.edu/MIST/) grids, and the `PARSEC` team provides a [web interface](http://stev.oapd.inaf.it/PARSEC/tools.html) to access different versions of their tracks together with some useful web-based tools. More recently, @squicciarini_madys_2022 developed and published another `Python` package [`MADYS`](https://madys.readthedocs.io/en/latest/), which can be used to derive ages and masses for pre-main sequence stars from multi-wavelengths photometric data with the extinction corrected according to extinction maps and laws. This code could also utilize different stellar evolutionary models. `MADYS` provides easy access to obtaining photometric age and mass estimates for large groups of young stellar or substellar objects.**

**Here we introduce** `ysoisochrone`, a `Python3` package that utilizes stellar evolutionary tracks to estimate stellar masses and ages of pre-main sequence stars with a Bayesian framework. While several papers in the literature utilize this method **[e.g., @Fernandes_2023; @Jorgensen_n_Lindergren_2005; @Pascucci_2016]**, an open-source **tool implementing this method** is not available. `ysoisochrone` fills this gap and provides a uniform platform to handle different evolutionary models **with easy access to Bayesian framework** along with tutorials and detailed documentation for first users. 

# Acknowledgements

We thank Greg Herczeg for suggesting the blending of the Feiden and Baraffe evolutionary tracks to handle a large range of stellar masses. **We also thank the editor and two referees, who provided helpful comments and suggestions to the package, documentation and this paper**. D.D. and I.P. acknowledge support from Collaborative NSF Astronomy \& Astrophysics Research grant (ID: 2205870).

# References
