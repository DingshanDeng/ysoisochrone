# ysoisochrone

`ysoisochrone` is a `Python3` package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

## Contributors

Dingshan Deng (dingshandeng@arizona.edu), The University of Arizona

Ilaria Pascucci, The University of Arizona

Rachel B. Fernandes, The Pennsylvania State University

## Feature 

- Handle different formats of the isochrones from different reference sources. The available evolutionary models include Baraffe et al. (2015), Feiden et al. (2016), PARSEC (both version 1.2 and 2.0), and MIST (version 1.2). See the reference section below for details. Other tracks will also be added in the future.
- Derive the stellar masses and ages from the isochrones by:
	- (a) Using the Bayesian inference approach. The required inputs are stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties.
	- (b) Using the Bayesian inference approach where we do not have a good luminosity measurement. Therefore, we need to assume an age for the target.
	- (c) Using a simple approach to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target.
- Basic plot utils to show Hertzsprung–Russell diagram, Bayesian inference results and others.

## Installation

In the terminal and in the directory of this package where `setup.py` exists.

```bash 
pip install .
```

## Quick Start

A [Quick Start Guide](./tutorials/ysoisochrone_basics.ipynb) is provided as a [tutorial `Jupyter Notebook`](./tutorials/) together with other `Jupyter Notebook`.

For detailed description and usage, please refer to this [documentation](./docs/build/html/index.html).

## Citations
If you use `ysoisochrone` as part of your research, please cite the xxx
