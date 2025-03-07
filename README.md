# ysoisochrone

`ysoisochrone` is a `Python3` package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

## Contributors

Dingshan Deng (dingshandeng@arizona.edu), The University of Arizona

Ilaria Pascucci, The University of Arizona

Rachel B. Fernandes, The Pennsylvania State University

## Feature 

- Handle different formats of the isochrones from different reference sources. The available evolutionary models include [Baraffe et al. (2015)](https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract), [Feiden (2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract), and [PARSEC (both version 1.2 and 2.0)](http://stev.oapd.inaf.it/PARSEC/index.html). Other tracks will also be added in the future.

- Derive the stellar masses and ages from the isochrones by:

	- (a) Using the Bayesian inference approach. The required inputs are stellar effective temperature ($T_{\rm eff}$), bolometric luminosity ($L_{\rm bol}$), and their uncertainties.
  
	- (b) Using the Bayesian inference approach where we do not have a good luminosity measurement. Therefore, we need to assume an age for the target.
	
> The code also includes a stand alone function to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target. 

- Basic plot utils to show Hertzsprung–Russell diagram, Bayesian inference results and others.

## Installation

You can easily install the package via

```bash
pip install ysoisochrone
```

Or, you can also install your preferred release by downloading the package release from the GitHub page. Then unzip the package.

In the terminal and in the directory of this package where `setup.py` exists.

```bash 
pip install .
```

## Quick Start

A [Quick Start Guide](https://github.com/DingshanDeng/ysoisochrone/blob/main/tutorial_notebooks/tutorial1_quick_start.ipynb) is provided as a `Jupyter Notebook` together with other [tutorial `Jupyter Notebooks`](https://github.com/DingshanDeng/ysoisochrone/tree/main/tutorial_notebooks). You can also find these tutorial notebooks in the folder called `tutorial_notebooks`.

This Guide is also provided in the [documentation](https://ysoisochrone.readthedocs.io/en/latest/index.html) together with some other detailed explainations.

## Citations
If you use `ysoisochrone` as part of your research, please cite 

"Deng et al. (2025), based on the IDL code developed by Pascucci et al. (2016)"

[![DOI](https://joss.theoj.org/papers/10.21105/joss.07493/status.svg)](https://doi.org/10.21105/joss.07493)

```
@article{Deng2025,
doi = {10.21105/joss.07493},
url = {https://doi.org/10.21105/joss.07493},
year = {2025},
publisher = {The Open Journal},
volume = {10},
number = {106},
pages = {7493},
author = {Dingshan Deng and Ilaria Pascucci and Rachel B. Fernandes},
title = {ysoisochrone: A Python package to estimate masses and ages for YSOs},
journal = {Journal of Open Source Software}
}

@article{Pascucci2016,
author = {{Pascucci}, I. and {Testi}, L. and {Herczeg}, G.~J. and {Long}, F. and {Manara}, C.~F. and {Hendler}, N. and {Mulders}, G.~D. and {Krijt}, S. and {Ciesla}, F. and {Henning}, Th. and {Mohanty}, S. and {Drabek-Maunder}, E. and {Apai}, D. and {Sz{\H{u}}cs}, L. and {Sacco}, G. and {Olofsson}, J.},
title = {A Steeper than Linear Disk Mass-Stellar Mass Scaling Relation},
journal = {The Astrophysical Journal},
keywords = {brown dwarfs, protoplanetary disks, stars: pre-main sequence, submillimeter: planetary systems, Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Solar and Stellar Astrophysics},
year = 2016,
month = nov,
volume = {831},
number = {2},
eid = {125},
pages = {125},
doi = {10.3847/0004-637X/831/2/125},
archivePrefix = {arXiv},
eprint = {1608.03621},
primaryClass = {astro-ph.EP},
adsurl = {https://ui.adsabs.harvard.edu/abs/2016ApJ...831..125P},
adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

If you use any [stellar evolutionary models](./models.md), please also refer to their original work/website for citations.

## Community Guidelines
We welcome contributions, issue reports, and questions about `ysoisochrone`! If you encounter a bug or issue, check out the [Issues page](https://github.com/DingshanDeng/ysoisochrone/issues) and provide a report with details about the problem and steps to reproduce it. For general support, usage questions and suggestions, you can start a discussion in [Discussions page](https://github.com/DingshanDeng/ysoisochrone/discussions), and of course feel free to send emails directly to us. If you want to contribute, feel free to fork the repository and create pull requests here. `ysoisochrone` is licensed under MIT license, so feel free to make use of the source code in any part of your own work/software.

## Useful links

There are a few other useful tools and packages that can be used to handle stellar evolutionary tracks and to estimate stellar mass and age for pre-main sequence stars. Including:

- [`MADYS`](https://madys.readthedocs.io/en/latest/) is `Python` package that can be used to derive ages and masses for pre-main sequence stars from multi-wavelengths photometric data with the extinction corrected according to extinction maps and laws; and it could ustilize different stellar evolutionary models, including MIST, PARSEC (v1.2 and 2.0), Feiden, Baraffe and many other models for pre-MS or MS stars.
  
- [`isochrones`](https://github.com/timothydmorton/isochrones) is a `Python` package that provides interface to access the [MIST](https://waps.cfa.harvard.edu/MIST/) grids.

- `PARSEC` team provides a [web interface](http://stev.oapd.inaf.it/PARSEC/tools.html) to access different versions of their tracks together with some useful web-based tools. 
