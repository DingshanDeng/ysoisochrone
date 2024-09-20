# ysoisochrone

`ysoisochrone` is a Python package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

## Background
Our primary method is a Bayesian inference approach that introduced in [Pascucci et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P/abstract) to estimate the stellar masses, ages, and associated uncertainties from the stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties. Uniform priors are assumed, and the likelihood functions are defined following [Andrews et al. (2013)](https://ui.adsabs.harvard.edu/abs/2013ApJ...771..129A/abstract). The pre-main-sequence evolutionary tracks from both [Feiden (2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract) and [Baraffe et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract) are adopted for hot ($T_{\rm eff} > 3,900$) and cool stars ($T_{\rm eff} \leq 3,900$), respectively. This method was also adopted in other works (e.g., [Fernandes et al. 2023](https://ui.adsabs.harvard.edu/abs/2023AJ....166..175F/abstract) and ALMA large program AGE-PRO). 

We also provide two other ways to estimate the stellar masses and ages from these isochrones: (b) In some cases, when a good measurement of stellar luminosity is unavailable,  we also provide an option to set up the assumed age to derive the stellar mass from the Bayesian inference. (c) A simple approach to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target.

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

You can start using this package from the [Quick Start Guide](./notebooks/ysoisochrone_basics.ipynb).

## Citations

If you end up using this package, please cite xxx (TBA)

## Contents:
```{toctree}
notebooks/ysoisochrone_basics
notebooks/ysoisochrone_methods
models
use_your_own_isochrone
apidocs/index
```
