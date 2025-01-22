# ysoisochrone

`ysoisochrone` is a `Python3` package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

## Background
There has been a long history of estimating stellar age and masses from the stellar evolutionary models (e.g., [Siess et al. 2000](https://ui.adsabs.harvard.edu/abs/2000A&A...358..593S), [Feiden 2016](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract), [Baraffe 2015](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract)). Different methods have been employed, from finding the closest track to an object's luminosity and temperature (e.g., [Manara et al. 2022](https://ui.adsabs.harvard.edu/abs/2023ASPC..534..539M/abstract)) to employing a Bayesian approach which enables estimating uncertainties on the inferred ages and masses (e.g., [Jørgensen & Lindegren 2005](https://ui.adsabs.harvard.edu/abs/2005A%26A...436..127J/abstract), [Gennaro et al. 2012](https://ui.adsabs.harvard.edu/abs/2012MNRAS.420..986G/abstract), [Andrews et al. 2013](https://ui.adsabs.harvard.edu/abs/2013ApJ...771..129A/abstract)). 

Our primary method is a Bayesian inference approach (see [quick start](./notebooks/ysoisochrone_basics.ipynb)), and the `Python` code builds on the `IDL` version developed in [Pascucci et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P/abstract). 
The code estimates the stellar masses, ages, and associated uncertainties by comparing their stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties with different stellar evolutionary models, including those specifically developed for YSOs.
Our method also uses a combination of the pre-main-sequence evolutionary tracks from [Feiden (2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract) and [Baraffe et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract) for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This aligns with the choice as suggested in [Pascucci et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P/abstract) to derive the stellar masses of Chamaeleon I young stellar objects (YSOs). 

We choose $T_{\rm eff}$ and $L_{\rm bol}$ to estimate the stellar age and mass because extinction is significant for young stars especially when embedded in the natal cloud. Although the $T_{\rm eff}$ and $L_{\rm bol}$ are not directly observed quantities, they are the two main quantities that evolutionary models can be compared with. When median or high-resolution spectroscopy is employed on individual targets, $T_{\rm eff}$ and $L_{\rm bol}$ can be well determined, and the best estimates for YSOs are from works where a stellar spectrum is fitted simutaneously with extinction and accretional heating (e.g., [Alcalá et al. (2017)](https://ui.adsabs.harvard.edu/abs/2017A%26A...600A..20A/abstract)). **NOTE: to obtain the best results from these input parameters, users should ensure that $T_{\rm eff}$ and $L_{\rm bol}$ (with their uncertainties) are derived simutaneously through spectroscopy.** 

`ysoisochrone` also has a new algorithm to find the zero age main sequence (ZAMS) automatically so that post-main sequence tracks are not included when interpolating to a finer grid of evolutionary tracks (e.g., [Fernandes et al. 2023](https://ui.adsabs.harvard.edu/abs/2023AJ....166..175F/abstract)). 
This algorithm also enables `ysoisochrone` to handle other stellar evolutionary models that are not only focused on pre-main-sequence stars, such as PARSEC tracks [Bressan et al. (2012)](https://ui.adsabs.harvard.edu/abs/2012MNRAS.427..127B). User-developed evolutionary tracks can be also utilized when provided in the specific format described in this documentation (see [models](./models.md) for all available models, and [how to use your own isochrones](./notebooks/ysoisochrone_customize_isochrone.ipynb)).

We also provide two other ways to estimate the stellar masses and ages from these isochrones. 

1. In some cases, when a good measurement of the stellar luminosity is unavailable,  we provide an option to set up the assumed age and then derive the stellar mass. Some examples when this method is useful include: targets that are very young and exceptionally bright; and targets with an edge-on disk so that the stellar $L_{\rm bol}$ is significantly underestimated. 
   
2. The classical method that finds the closest point from the isochrones for each YSOs based on their $T_{\rm eff}$ and $L_{\rm bol}$. **NOTE: This stand alone function is primarily used for verification purposes as it does not provide uncertainties; and we recommend using the Bayesian approaches as described above where the uncertainties are provided in the results**. 

## Installation

You can easily install the package via

```bash
pip install ysoisochrone
```

Or, you can also install your preferred release by downloading the package release from the GitHub page. Then unzip the package. In the terminal and in the directory of this package where `setup.py` exists.

```bash 
pip install .
```

which should install the necessary dependencies.

If the installation went to plan you should be able to run the tutorial notebooks.

After installing the package, you can try import the package as

```python
import ysoisochrone
```

Then you can start check out the [Quick Start Guide](./notebooks/ysoisochrone_basics.ipynb) as well as the [tutorial notebooks here](https://github.com/DingshanDeng/ysoisochrone/tree/main/tutorial_notebooks).

## Citations

If you end up using this package, please cite xxx (TBA)

If you use any [stellar evolutionary models](./models.md), please also refer to their original work/website for citations.

## Community Guidelines
We welcome contributions, issue reports, and questions about `ysoisochrone`! If you encounter a bug or issue, check out the [Issues page](https://github.com/DingshanDeng/ysoisochrone/issues) and provide a report with details about the problem and steps to reproduce it. For general support, usage questions and suggestions, you can start a discussion in [Discussions page](https://github.com/DingshanDeng/ysoisochrone/discussions), and of course feel free to send emails directly to us. If you want to contribute, feel free to fork the repository and create pull requests here. `ysoisochrone` is licensed under MIT license, so feel free to make use of the source code in any part of your own work/software.

## Useful links

There are a few other useful tools and packages that can be used to handle stellar evolutionary tracks and to estimate stellar mass and age for pre-main sequence stars. Including:

- [`MADYS`](https://madys.readthedocs.io/en/latest/) is `Python` package that can be used to derive ages and masses for pre-main sequence stars from multi-wavelengths photometric data with the extinction corrected according to extinction maps and laws; and it could ustilize different stellar evolutionary models, including MIST, PARSEC (v1.2 and 2.0), Feiden, Baraffe and many other models for pre-MS or MS stars.

- [`isochrones`](https://github.com/timothydmorton/isochrones) is a `Python` package that provides interface to access the [MIST](https://waps.cfa.harvard.edu/MIST/) grids.

- `PARSEC` team provides a [web interface](http://stev.oapd.inaf.it/PARSEC/tools.html) to access different versions of their tracks together with some useful web-based tools. 
  
## Contents:
```{toctree}
notebooks/ysoisochrone_basics
models
notebooks/ysoisochrone_customize_isochrone
apidocs/index
```
