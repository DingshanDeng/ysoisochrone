# ysoisochrone

`ysoisochrone` is a `Python3` package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

## Background
There has been a long history of estimating stellar age and masses from the stellar evolutionary models (e.g., [Siess et al. 2000](https://ui.adsabs.harvard.edu/abs/2000A&A...358..593S), [Feiden 2016](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract), [Baraffe 2015](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract)). Different methods have been employed, from finding the closest track to an object's luminosity and temperature (e.g., [Manara et al. 2022](https://ui.adsabs.harvard.edu/abs/2023ASPC..534..539M/abstract)) to employing a Bayesian approach which enables estimating uncertainties on the inferred ages and masses (e.g., [Jørgensen & Lindegren 2005](https://ui.adsabs.harvard.edu/abs/2012MNRAS.420..986G/abstract), [Gennaro et al. 2012](https://ui.adsabs.harvard.edu/abs/2005A%26A...436..127J/abstract), [Andrews et al. 2013](https://ui.adsabs.harvard.edu/abs/2013ApJ...771..129A/abstract)). 

Our primary method is a Bayesian inference approach (see [quick start](./notebooks/ysoisochrone_basics.ipynb)), and the `Python` code builds on the `IDL` version developed in [Pascucci et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P/abstract). 
The code estimates the stellar masses, ages, and associated uncertainties by comparing their stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties with different stellar evolutionary models, including those specifically developed for YSOs.
Our method also uses a combination of the pre-main-sequence evolutionary tracks from [Feiden (2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract) and [Baraffe et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract) for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This aligns with the choice as initially suggested in [Pascucci et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P/abstract) to derive the stellar masses of chameleon I young stellar objects (YSOs). 
`ysoisochrone` also has a new algorithm to find the zero age main sequence (ZAMS) automatically so that post-main sequence tracks are not included when interpolating to a finer grid of evolutionary tracks (e.g., [Fernandes et al. 2023](https://ui.adsabs.harvard.edu/abs/2023AJ....166..175F/abstract)). 
This algorithm also enables `ysoisochrone` to handle other stellar evolutionary models that are not only focused on pre-main-sequence stars, such as PARSEC tracks [Bressan et al. (2012)](https://ui.adsabs.harvard.edu/abs/2012MNRAS.427..127B). User-developed evolutionary tracks can be also utilized when provided in the specific format described in this documentation (see [models](./models.md) for all available models, and [how to use your own isochrones](./notebooks/ysoisochrone_customize_isochrone.ipynb)).

We also provide two other ways to estimate the stellar masses and ages from these isochrones. (a) The classical method that finds the closest point from the isochrones for each YSOs based on their $T_{\rm eff}$ and $L_{\rm bol}$ (the uncertainties are ignored in this method). (b) In some cases, when a good measurement of the stellar luminosity is unavailable,  we provide an option to set up the assumed age and then derive the stellar mass. Some examples when this method is useful include: targets that are very young and exceptionally bright; and targets with an edge-on disk so that the stellar $L_{\rm bol}$ is significantly underestimated.

## Installation

In the terminal and in the directory of this package where `setup.py` exists.

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

## Contents:
```{toctree}
notebooks/ysoisochrone_basics
models
notebooks/ysoisochrone_customize_isochrone
apidocs/index
```
