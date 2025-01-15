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
	- (c) Using a simple approach to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target.
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
If you use `ysoisochrone` as part of your research, please cite the xxx

## Community Guidelines
We welcome contributions, issue reports, and questions about `ysoisochrone`! If you encounter a bug or issue, check out the [Issues page](https://github.com/DingshanDeng/ysoisochrone/issues) and provide a report with details about the problem and steps to reproduce it. For general support, usage questions and suggestions, you can start a discussion in [Discussions page](https://github.com/DingshanDeng/ysoisochrone/discussions), and of course feel free to send emails directly to us. If you want to contribute, feel free to fork the repository and create pull requests here. `ysoisochrone` is licensed under MIT license, so feel free to make use of the source code in any part of your own work/software.