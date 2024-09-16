# ysoisochrone

`ysoisochrone` is a Python package that handles the isochrones for young-stellar-objects. One of the primary goals of this package is to derive the stellar mass and ages from the isochrones.

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

After installing the package, you can try import the package as
```python
import pandas as pd
import ysoisochrone
```

Then you need to format an input `pandas.DataFrame` file with the following columns `['Source', 'Teff', 'e_Teff', 'Luminosity', 'e_Luminosity']`. The 'Source' is the list of source names; it can be just the ID numbers you prefer; 'Teff' is the effective temperature in the unit of Kelvin, and 'e_Teff' is the associated uncertainties; 'Luminosity' is the bolometric luminosities of these targets un the unit of solar luminosity, and 'e_Luminosity' is their uncertainties.

The easiest way to do so is to create a `.csv` file using EXCEL or similar software, and this file includes these columns (for example, see `example_targets.csv`), and then you can utilize `pandas` to read in this file. Later you use this as an input.
```python
df_prop = pd.read_csv('example_targets.csv')

best_logmass_output, best_logage_output, lmass_all, lage_all =\
    ysoisochrone.bayesian.derive_stellar_mass_age(df_prop, method='Baraffe_n_Feiden', isochrone_data_dir=None, no_uncertainties=False, plot=True, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False)
```

The method here is for calling different evolutionary tracks. The choices are: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the `method = 'custome'`, you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix (see documentation for details).

The outputs are:
(a) `best_logmass_output` (log10 of mass in the unit of solar masses), `best_logage_output` (log10 of age in the unit of yrs) are the arrays that includes the best derived values and their lower and upper boundaries from the 68% confidence intervals. 
(b) `lmass_all` and `lage_all` are the distributions of the likelihood functions for each source; they could be used to estimate the medians based on the likelihood distributions.

An example of saving these `output` numbers are
```python
df_output_mass = pd.DataFrame(np.array(best_mass_output), columns=['logmass[msolar]', 'lw_logmass[msolar]', 'up_logmass[msolar]'])
df_output_age = pd.DataFrame(np.array(best_age_output), columns=['logage[yrs]', 'lw_logage[yrs]', 'up_logage[yrs]']) 
df_output = pd.concat([df_prop, df_output_mass, df_output_age], axis=1)
# Then you can save this output file
df_output.to_csv('example_targets_o.csv', index=False))
```

We also provide two other ways to estimate the stellar masses and ages from these isochrones. 

In some cases, when a good measurement of stellar luminosity is unavailable,  we also provide an option to set up the assumed age (`assumed_age=1.5e6` in the example, it is in the unit of yr) to derive the stellar mass from the Bayesian inference. 
```python
ysoisochrone.bayesian.derive_stellar_mass_assuming_age(df_prop, assumed_age=1.5e6, method='Baraffe_n_Feiden', verbose=True, plot=True)
```

A simple approach to estimate the stellar masses and ages from the grid point that has the closest $T_{\rm eff}$ and $L_{\rm bol}$ to the target.
```python
ysoisochrone.bayesian.derive_stellar_mass_age_simple(df_prop, method='Baraffe2015', verbose=True)
```

There are also detailed tutorials available in the documentation.

## Citations
If you use `ysoisochrone` as part of your research, please cite the xxx
