import os # , sys, copy
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from scipy.integrate import simps
try:
    # Try to import simpson (the newer version)
    from scipy.integrate import simpson
except ImportError:
    # If simpson doesn't exist, fallback to simps (the older version)
    from scipy.integrate import simps as simpson
# from scipy.interpolate import interp1d

import tqdm

from ysoisochrone import plotting
from ysoisochrone import utils
from ysoisochrone.isochrone import Isochrone

def bayesian_mass_age(log_age_dummy, log_masses_dummy, L, plot=False, source=None, confidence_interval=0.68, verbose=False, save_fig=False, fig_save_dir='figure', customized_fig_name='', force_through=False):
    ''' 
    derive the mass and ages for a star from a likelihood distribution
    
    Args:

        log_age_dummy [array]: 
            The log of stellar ages.
        log_masses_dummy [array]: 
            The log of stellar masses.
        L [2D array]: 
            The likelihood function grid.
        confidence_interval [float]:
            the desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
        source [str, optional]: 
            The source name for labeling the plot.
        save_fig [bool, optional]: 
            Whether to save the figure.
        fig_save_dir [str, optional]:
            Directory to save the figure if save_fig is True.
        customized_fig_name [str, optional]: 
            Customized figure name.
        force_through [bool, optional, DANGEROUS]: 
            (DANGEROUS: Only use for testing and debugging proposes!!!)
            if True, do not raise when best mass is at the upper grid edge; 
            proceed with plotting and set the upper mass uncertainty
            to the grid maximum (with a warning if verbose).
    
    Returns:
    
        A tupe with three things: [0] best age and mass and their uncertainties; [1] the logage array and its likelihood function; [2] the logmass array and its likelihood function.
        [best_age, age_unc, best_mass, mass_unc], np.array([log_age_dummy, L_age_norm]), np.array([log_masses_dummy, L_mass_norm])
    '''
    
    half_sigma_perc = confidence_interval/2.0
    
    # if verbose: # for debugging
    #     print('the shape of logage', log_age_dummy.shape)   
    #     print('the shape of logmass', log_masses_dummy.shape)
    #     print('the shape of L', L.shape)
        
    # Integrate L over mstar for each age bin
    L_age = np.array([simpson(L[jj, :], x=log_masses_dummy) for jj in range(len(log_age_dummy))])
    L_age /= simpson(L_age, x=log_age_dummy)
    
    # if verbose: # for debugging
    #     print('L_age:', L_age)
    #     print(np.cumsum(L_age))
    #     print(np.cumsum(L_age)/np.sum(L_age))
    
    best_age_idx = np.argmax(L_age)
    best_age = log_age_dummy[best_age_idx]
    
    #
    # find the age_unc
    #
    
    # # earler version: find the closest index
    # L_age_array = np.cumsum(L_age) / np.sum(L_age)
    # age_low_idx = np.argmin(np.abs(L_age_array[:best_age_idx] - (L_age_array[best_age_idx] - half_sigma_perc)))
    # age_up_idx = best_age_idx + np.argmin(np.abs(L_age_array[best_age_idx:] - (L_age_array[best_age_idx] + half_sigma_perc)))
    
    L_age_array = np.cumsum(L_age) / np.sum(L_age)

    # --- SAFE GUARDS for edge best_age_idx ---
    if best_age_idx == 0:
        age_low_idx = 0
        # find upper bound in the full array
        target_up = L_age_array[best_age_idx] + half_sigma_perc
        age_up_idx = int(np.argmin(np.abs(L_age_array - target_up)))
        age_up_idx = max(age_up_idx, age_low_idx)

    elif best_age_idx == len(L_age_array) - 1:
        age_up_idx = len(L_age_array) - 1
        # find lower bound in the full array
        target_low = L_age_array[best_age_idx] - half_sigma_perc
        age_low_idx = int(np.argmin(np.abs(L_age_array - target_low)))
        age_low_idx = min(age_low_idx, age_up_idx)

    else:
        target_low = L_age_array[best_age_idx] - half_sigma_perc
        target_up  = L_age_array[best_age_idx] + half_sigma_perc

        age_low_idx = int(np.argmin(np.abs(L_age_array[:best_age_idx] - target_low)))
        age_up_idx = int(best_age_idx + np.argmin(np.abs(L_age_array[best_age_idx:] - target_up)))
    
    # Handle cases where the cumulative sum exceeds the desired confidence interval
    if L_age_array[best_age_idx] - half_sigma_perc < 0:
        i_idx = best_age_idx
        
        # if verbose:
        #     print('this i_idx:', i_idx)
        
        key = 0
        while key == 0:
            if i_idx == 0:
                key = 1
                age_low_idx = i_idx
            else:    
                i_idx = int(i_idx) - 1
                if L_age_array[i_idx] < 1e-3:
                    key = 1
                    age_low_idx = i_idx 
                
    if L_age_array[best_age_idx] + half_sigma_perc > 1:
        i_idx = best_age_idx
        key = 0
        while key == 0:
            if i_idx == int(len(L_age_array) - 1):
                key = 1
                age_up_idx = i_idx
            else:
                i_idx = int(i_idx) + 1
                if np.abs(L_age_array[i_idx] - 1) < 1e-3:
                    key = 1
                    age_up_idx = i_idx
    
    age_unc = [log_age_dummy[age_low_idx], log_age_dummy[age_up_idx]]
    
    if age_unc[0] != best_age and age_unc[1] != best_age:
        if age_unc[0] == min(log_age_dummy) or age_unc[1] == max(log_age_dummy):
            if age_unc[0] == min(log_age_dummy):
                age_unc[0] = log_age_dummy[np.argmin(np.abs(L_age_array[:best_age_idx] - (L_age_array[best_age_idx] - half_sigma_perc)))]
            else:
                age_unc[1] = log_age_dummy[best_age_idx + np.argmin(np.abs(L_age_array[best_age_idx:] - (L_age_array[best_age_idx] + half_sigma_perc)))]
    
    # Integrate L over age for each mass bin
    L_mass = np.array([simpson(L[:, jj], x=log_age_dummy) for jj in range(len(log_masses_dummy))])
    L_mass /= simpson(L_mass, x=log_masses_dummy)
    
    best_mass_idx = np.argmax(L_mass)
    best_log_mass = best_mass = log_masses_dummy[best_mass_idx]
    
    # # earler version: find the closest index
    # L_mass_array = np.cumsum(L_mass) / np.sum(L_mass)
    # mass_low_idx = np.argmin(np.abs(L_mass_array[:best_mass_idx] - (L_mass_array[best_mass_idx] - half_sigma_perc)))
    # mass_up_idx = best_mass_idx + np.argmin(np.abs(L_mass_array[best_mass_idx:] - (L_mass_array[best_mass_idx] + half_sigma_perc)))
    
    L_mass_array = np.cumsum(L_mass) / np.sum(L_mass)

    # --- SAFE GUARDS for edge best_mass_idx ---
    if best_mass_idx == 0:
        mass_low_idx = 0
        # find upper bound within remaining array
        mass_up_idx = np.argmin(np.abs(L_mass_array - (L_mass_array[best_mass_idx] + half_sigma_perc)))
        mass_up_idx = max(mass_up_idx, 0)

    elif best_mass_idx == len(L_mass_array) - 1:
        mass_up_idx = len(L_mass_array) - 1
        # find lower bound within array up to last
        mass_low_idx = np.argmin(np.abs(L_mass_array - (L_mass_array[best_mass_idx] - half_sigma_perc)))
        mass_low_idx = min(mass_low_idx, mass_up_idx)

    else:
        mass_low_idx = np.argmin(
            np.abs(L_mass_array[:best_mass_idx] - (L_mass_array[best_mass_idx] - half_sigma_perc))
        )
        mass_up_idx = best_mass_idx + np.argmin(
            np.abs(L_mass_array[best_mass_idx:] - (L_mass_array[best_mass_idx] + half_sigma_perc))
        )
    
    # Handle cases where the cumulative sum exceeds the desired confidence interval
    if L_mass_array[best_mass_idx] - half_sigma_perc < 0:
        i_idx = best_mass_idx
        key = 0
        while key == 0:
            if i_idx == 0:
                key = 1
                mass_low_idx = i_idx
            else:
                i_idx = int(i_idx) - 1
                if L_mass_array[i_idx] < 1e-3:
                    key = 1
                    mass_low_idx = i_idx
                
    if L_mass_array[best_mass_idx] + half_sigma_perc > 1:
        i_idx = best_mass_idx
        key = 0
        while key == 0:
            if i_idx == int(len(L_mass_array) - 1):
                key = 1
                mass_up_idx = i_idx
            else:
                i_idx = int(i_idx) + 1
                if np.abs(L_mass_array[i_idx] - 1) < 1e-3:
                    key = 1
                    mass_up_idx = i_idx
    
    if verbose:
        print('sum of Lmass', np.sum(L_mass))
        print('the last index of Lmass', L_mass[-1])
        print('sum of Lmass array', np.sum(L_mass_array))
        print('the last index of Lmass array', L_mass_array[-1])
        # print('the best mass and its index: ', best_log_mass, best_mass_idx, L_mass_array[best_mass_idx])
        # print('lw: ', log_masses_dummy[mass_low_idx], mass_low_idx, L_mass_array[mass_low_idx])
        # print('up: ', log_masses_dummy[mass_up_idx], mass_up_idx, L_mass_array[mass_up_idx])
        print('check the sum of confidence interval (default 0.68)')
        print(L_mass_array[mass_up_idx] - L_mass_array[mass_low_idx])
    
    mass_unc = [log_masses_dummy[mass_low_idx], log_masses_dummy[mass_up_idx]]
    
    if mass_unc[0] != best_mass and mass_unc[1] != best_mass:
        if mass_unc[0] == min(log_masses_dummy) or mass_unc[1] == max(log_masses_dummy):
            if mass_unc[0] == min(log_masses_dummy):
                mass_unc[0] = log_masses_dummy[np.argmin(np.abs(L_mass_array[:best_mass_idx] - (L_mass_array[best_mass_idx] - half_sigma_perc)))]
            else:
                # Upper edge case: previously raised ValueError; now optionally force through
                if force_through:
                    if verbose:
                        print(
                            "[force_through] Best mass / CI hits the upper grid edge; "
                            "setting upper mass uncertainty to the grid maximum. "
                            "Consider extending the mass grid upward for unbiased CI."
                        )
                    mass_unc[1] = log_masses_dummy[-1]
                    # Ensure the interval is non-decreasing
                    if mass_unc[1] < mass_unc[0]:
                        mass_unc[1] = mass_unc[0]
                else:
                    raise ValueError('The mass is the largest in the grid. This needs to be sorted out! Consider extending the isochrone grid or removing this target from the list.')
    
    #
    # save the normalized probability distributions
    #
    L_age_norm = L_age / np.trapz(L_age, log_age_dummy) # / max(L_age) * (max(log_masses_dummy) - min(log_masses_dummy)) # + min(log_masses_dummy)
    L_mass_norm = L_mass / np.trapz(L_mass, log_masses_dummy) # / max(L_mass) * (max(log_age_dummy) - min(log_age_dummy)) # + min(log_age_dummy)
    
    if plot:
        plotting.plot_bayesian_results(log_age_dummy, log_masses_dummy, L, best_age, best_mass, age_unc, mass_unc, source, save_fig, fig_save_dir, customized_fig_name)
    
    return [best_age, age_unc, best_mass, mass_unc], np.array([log_age_dummy, L_age_norm]), np.array([log_masses_dummy, L_mass_norm])


def derive_stellar_mass_age(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68, single_bayesian_for_nolum_target=True, prior_age=None, prior_mass=None, prior_joint=None, prior_normalize='maxone', force_through=False):
    """
    Derives stellar mass and age from evolutionary tracks using a Bayesian framework.

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff, Luminosity, etc.).
            The formated column needs to be: ['Source', 'Teff[K]', 'e_Teff[K]', 'Luminosity[Lsun]', 'e_Luminosity[Lsun]']
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
        isochrone_data_dir: [str, optional]
            The datadir where all the data files for the isochrones are stored
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use
            This is needed if you want to set the model as 'customize'.
        no_uncertainties: [bool, optional]
            Whether to assume no uncertainties in Teff and Luminosity (default: False).
        plot: [bool, optional]
            Whether to plot the likelihood distributions (default: False).
        save_fig: [bool, optional]
            Whether to save the figure (default: False).
        save_lfunc: [bool, optional]
            Whether to save the likelihood functions to CSV (default: False).
        fig_save_dir: [str, optional]
            Directory where figures are saved if save_fig is True (default: 'figures').
        csv_save_dir: [str, optional]
            Directory where likelihood function data is saved if save_lfunc is True (default: 'lfunc_data').
        verbose: [bool, optional]
            Whether to print verbose output (default: False).
        toofaint: [list, optional]
            A list of target names (in the 'Source' column) that are toofaint, 
            will assign the median age (that is setup here) to them. If this one is not empty, `median_age` needs to be assigned.
        toobright: [list, optional]
            A list of target names (in the 'Source' column) that are toobirght, 
            will assign the minimum age in the read in evolutionary tracks to them. If this one is not empty, `median_age` needs to be assigned.
        median_age: [float, optional] unit: Myrs
            The median age that will be asigned tothe targets that are toofaint.
        confidence_interval: [float, optional]
            The desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
        single_bayesian_for_nolum_target: [bool, optional] Default: True
            Whether to still run a single Bayesian for the target that does not have good luminosity measurement (too bright or faint or anyother). If True, will still run a single Bayesian method to derive the stellar mass with the assumed `median_age`, otherwise will only find the closest track and will not obtain an uncertainty. Turn this to False to simply find the closest model grid point as in Pascucci+2016.
        === handle Priors ===
        prior_age:  one of
            - callable: f(log_age_yrs) -> non-negative density
            - dict(tabulated): {'grid': log_age_array, 'pdf': pdf_array, 'extrapolate': 'edge'|'zero', 'normalize': 'max1'|'sum1'|'none'}
        prior_mass: one of
            - callable: f(log_mass_msun) -> non-negative density
            - dict(tabulated): {'grid': log_mass_array, 'pdf': pdf_array, ...}
        prior_joint: callable taking (log_age_yrs, log_mass_msun) and returning a 2D density.
            NOTE: if provided, it overrides the separable prior_age/prior_mass product.
        prior_normalize: default normalization used for 1D priors if not specified in the dict.
        === DANGER ZONE ===
        force_through [bool, optional, DANGEROUS]: 
            (DANGEROUS: Only use for testing and debugging proposes!!!)
            if True, do not raise errors when best mass is at the upper grid edge; 
            proceed with plotting and set the upper mass uncertainty
            to the grid maximum (with a warning if verbose).
    
    Returns:
    
        best_logmass_output: [array]
            Array containing the best-fit masses and uncertainties (represent as lower and upper boundaries of the confidence interval).
        best_logage_output: [array]
            Array containing the best-fit ages and uncertainties (represent as lower and upper boundaries of the confidence interval).
        lage_all: [dictionary]
            The likelihood function of age for all target
        lmass_all: [dictionary]
            The likelihood function of mass for all target
        flag_all: [list of strs]
            The list of flags (in string) for all target
    """
    
    # Prepare output lists
    # source_info_output = []
    best_logage_output = []
    best_logmass_output = []
    lage_all = {}
    lmass_all = {}
    flag_all = []
    
    # Loop through each star in the source list
    for ii in tqdm.tqdm(df_prop.index):
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print('')
            print(f'Working on: {source_t}')
        
        # Observables
        # Extract current values and uncertainties
        L_this = df_prop.loc[ii, 'Luminosity[Lsun]']
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logL = np.log10(L_this)
        c_logT = np.log10(T_this)

        if no_uncertainties:
            sigma_logL = 0.1  # Assume fixed uncertainty for Luminosity
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else: 
            err_L_this = df_prop.loc[ii, 'e_Luminosity[Lsun]']
            sigma_logL = utils.unc_log10(L_this, err_L_this)

            err_T_this = df_prop.loc[ii, 'e_Teff[K]']
            sigma_logT = utils.unc_log10(T_this, err_T_this)

        # Initialize the isochrone class with default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
                
            if verbose:
                print(f'Adopted the { "Feiden" if T_this > 3900.0 else "Baraffe" } track.')
                
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
            
            if verbose:
                print(f'Adopted the %s track.'%(model))
                
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
            
            if verbose:
                print(f'Adopted the customize track from %s.'%(isochrone_mat_file))
                
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        log_masses_dummy = np.log10(masses_dummy)
        
        # === SPECIAL CASE: too faint / too bright handling ===
        if np.any([source_t in toofaint, source_t in toobright]):
            if verbose:
                if source_t in toofaint:
                    print('this target %s is too faint, it is likely to have an edge-on disk, so we assign the median age (%.2f Myrs) of the region to the target'%(source_t, median_age))
                    
                elif source_t in toobright:
                    print('this target %s is too bright, so we assign the smallest age to this target.'%(source_t))
            
            # Handle special cases for faint or bright stars
            if source_t in toofaint:
                c_age = median_age
            else:  # too bright
                c_age = np.min(log_age_dummy)

            if single_bayesian_for_nolum_target:
                res = derive_stellar_mass_assuming_age(
                    df_prop.loc[[ii]],
                    assumed_age=c_age,
                    model=model,
                    isochrone_data_dir=isochrone_data_dir,
                    isochrone_mat_file=isochrone_mat_file,
                    no_uncertainties=no_uncertainties,
                    confidence_interval=confidence_interval,
                    verbose=verbose,
                    plot=plot,
                    prior_mass=prior_mass,
                    prior_normalize=prior_normalize,
                    )
                best_logmass_wunc = res[0]
            else:
                if verbose:
                    print('we find the closest point from the model to this target (%s) instead of using Bayesian framework'%(source_t))
                res = derive_stellar_mass_assuming_age_closest_trk(
                    df_prop.loc[[ii]],
                    assumed_age=1.5e6,
                    model=model,
                    isochrone_data_dir=isochrone_data_dir,
                    isochrone_mat_file=isochrone_mat_file,
                    verbose=verbose
                    )
                best_logmass_wunc = [res[0], np.nan, np.nan]
            
            # this_age = np.where(log_age_dummy == c_age)
            # Tdiff_index = np.abs(logtlogl_dummy[this_age, :, 0] - c_logT).argmin()
            
            """
            the targets that are too bright or too faint are are assigned with age without uncertainties
            """
            # best_mass = [np.log10(masses_dummy[Tdiff_index]), np.nan, np.nan]
            best_logage_wunc = [c_age, np.nan, np.nan]
            
        else:
            # === Standard Bayesian branch ===
            
            # == first check whether (logT, logL) is within the model grid domain ==
            logTe_grid = logtlogl_dummy[:, :, 0]  # (Nm, Na)
            logL_grid  = logtlogl_dummy[:, :, 1]

            grid_logT_min = np.nanmin(logTe_grid)
            grid_logT_max = np.nanmax(logTe_grid)
            grid_logL_min = np.nanmin(logL_grid)
            grid_logL_max = np.nanmax(logL_grid)

            outside_T = (c_logT < grid_logT_min) or (c_logT > grid_logT_max)
            outside_L = (c_logL < grid_logL_min) or (c_logL > grid_logL_max)

            if outside_T or outside_L:
                # record NaNs and flag; optionally store empty marginals
                best_logmass_wunc = [np.nan, np.nan, np.nan]
                best_logage_wunc  = [np.nan, np.nan, np.nan]

                # optional: store placeholders so the returned dicts have keys
                lage_all[f'target_{ii}'] = np.array([log_age_dummy, np.full_like(log_age_dummy, np.nan)]).T
                lmass_all[f'target_{ii}'] = np.array([log_masses_dummy, np.full_like(log_masses_dummy, np.nan)]).T

                # add informative flag
                if outside_T and outside_L:
                    flag_all.append('out_of_grid_TL')
                elif outside_T:
                    flag_all.append('out_of_grid_T')
                else:
                    flag_all.append('out_of_grid_L')

                if verbose:
                    print("WARNING: target outside model grid.")
                    print(f"  logT={c_logT:.3f} grid=[{grid_logT_min:.3f}, {grid_logT_max:.3f}]")
                    print(f"  logL={c_logL:.3f} grid=[{grid_logL_min:.3f}, {grid_logL_max:.3f}]")

                # skip Bayesian for this target
                best_logmass_output.append(best_logmass_wunc)
                best_logage_output.append(best_logage_wunc)
                continue
            
            # == for targets within the grid, proceed with Bayesian estimation ==
            # Compute the likelihood using the Bayesian framework
            # in p2016, a log uniform prior is adopted
            # therefore it equals to the cases without assuming any prior
            lfunc = utils.get_likelihood_p2016(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL)
            lfunc[np.isnan(lfunc)] = 1e-99 # Set NaN positions to 1e-99 to ignore them
            
            # Create the mask to mask out the trks after zero-age-main-sequence
            _, _, mask_pms = utils.find_zams_curve(isochrone)
            lfunc[np.logical_not(mask_pms)] = 1e-99 # Set the main-sequence and post-main-sequence positions to 1e-99
            
            # === NEW in v1.0.1: Evaluate priors on this grid ===
            # separable prior (age * mass) unless a joint prior is provided
            if prior_joint is not None:
                if not callable(prior_joint):
                    raise TypeError("prior_joint must be a callable: f(log_age, log_mass) -> 2D pdf")
                # Evaluate on mesh
                A, M = np.meshgrid(log_age_dummy, log_masses_dummy, indexing='ij')  # shapes: (Na, Nm)
                prior_2d = np.asarray(prior_joint(A, M), dtype=float)
                if prior_2d.shape != lfunc.shape:
                    raise ValueError("prior_joint callable must return an array matching the lfunc shape "
                                     f"{lfunc.shape}, got {prior_2d.shape}")
                # Normalize for stability (optional)
                prior_2d = utils._normalize_pdf(prior_2d, method=prior_normalize)
            else:
                # 1D priors
                prior_age_1d = utils._eval_1d_prior_on_grid(
                    prior_age, log_age_dummy, normalize=prior_normalize, name='prior_age'
                )
                prior_mass_1d = utils._eval_1d_prior_on_grid(
                    prior_mass, log_masses_dummy, normalize=prior_normalize, name='prior_mass'
                )
                # Outer product to get 2D prior aligned with (age, mass)
                prior_2d = np.outer(prior_age_1d, prior_mass_1d)
            
            # Combine: posterior grid (unnormalized)
            post_2d = lfunc * np.clip(prior_2d, 0.0, np.inf)
            # Guard against all-zero arrays
            if not np.isfinite(post_2d).any() or np.max(post_2d) <= 0:
                if verbose:
                    print("WARNING: posterior collapsed to zero; falling back to likelihood-only for stability.")
                post_2d = lfunc.copy()

            # Use Bayesian mass and age estimation
            bayes_res, lage_res, lmass_res = bayesian_mass_age(
                log_age_dummy, log_masses_dummy, post_2d,
                plot=plot, source=source_t, verbose=verbose,
                save_fig=save_fig, fig_save_dir=fig_save_dir, confidence_interval=confidence_interval,
                force_through=force_through
                )
            best_logmass_wunc = [bayes_res[2], bayes_res[3][0], bayes_res[3][1]]
            best_logage_wunc = [bayes_res[0], bayes_res[1][0], bayes_res[1][1]]

            # Store the posterior marginals
            lage_all[f'target_{ii}'] = lage_res
            lmass_all[f'target_{ii}'] = lmass_res

            # Save the likelihood functions if requested
            if save_lfunc:
                df_lage = pd.DataFrame(lage_res.T, columns=['logage[yrs]', 'Lage'])
                df_lmass = pd.DataFrame(lmass_res.T, columns=['logmass[Msun]', 'Lmass'])
                if not os.path.exists(csv_save_dir):
                    os.makedirs(csv_save_dir)
                df_lage.to_csv(os.path.join(csv_save_dir, f'{source_t}_lage.csv'), index=False)
                df_lmass.to_csv(os.path.join(csv_save_dir, f'{source_t}_lmass.csv'), index=False)

        # # Save the best-fit mass and age results
        # if no_uncertainties:
        #     source_info_output.append([source_t, T_this, L_this])
        # else:
        #     source_info_output.append([source_t, T_this, df_prop.loc[ii, 'e_Teff[K]'], L_this, df_prop.loc[ii, 'e_Luminosity[Lsun]']])
        
        # Collect outputs
        best_logmass_output.append(best_logmass_wunc)
        best_logage_output.append(best_logage_wunc)
        
        if verbose:
            print(f'Results for target: {source_t}')
            print(f'Best Mass: {10**best_logmass_wunc[0]:.2f} [Msun], Age: {10**best_logage_wunc[0]:.2e} [yrs]')

        if source_t in toobright:        
            flag_all.append('toobright')
        elif source_t in toofaint:
            flag_all.append('toofaint')
        else:
            flag_all.append('good')
        
    return np.array(best_logmass_output), np.array(best_logage_output), lmass_all, lage_all, flag_all


def derive_stellar_mass_age_uniprior(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68, single_bayesian_for_nolum_target=True):
    """
    Derives stellar mass and age from evolutionary tracks using a Bayesian framework.
    This is the original derive_stellar_mass_age in the v1.0.0 release
    where we do not allow the change of the prior in the Bayesian framework
    and it uses log-uniform priors in both Mass and Age, as in Pascucci+2016 and Deng+2025 (AGE-PRO. III)

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff, Luminosity, etc.).
            The formated column needs to be: ['Source', 'Teff[K]', 'e_Teff[K]', 'Luminosity[Lsun]', 'e_Luminosity[Lsun]']
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
        isochrone_data_dir: [str, optional]
            The datadir where all the data files for the isochrones are stored
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use
            This is needed if you want to set the model as 'customize'.
        no_uncertainties: [bool, optional]
            Whether to assume no uncertainties in Teff and Luminosity (default: False).
        plot: [bool, optional]
            Whether to plot the likelihood distributions (default: False).
        save_fig: [bool, optional]
            Whether to save the figure (default: False).
        save_lfunc: [bool, optional]
            Whether to save the likelihood functions to CSV (default: False).
        fig_save_dir: [str, optional]
            Directory where figures are saved if save_fig is True (default: 'figures').
        csv_save_dir: [str, optional]
            Directory where likelihood function data is saved if save_lfunc is True (default: 'lfunc_data').
        verbose: [bool, optional]
            Whether to print verbose output (default: False).
        toofaint: [list, optional]
            A list of target names (in the 'Source' column) that are toofaint, 
            will assign the median age (that is setup here) to them. If this one is not empty, `median_age` needs to be assigned.
        toobright: [list, optional]
            A list of target names (in the 'Source' column) that are toobirght, 
            will assign the minimum age in the read in evolutionary tracks to them. If this one is not empty, `median_age` needs to be assigned.
        median_age: [float, optional] unit: Myrs
            The median age that will be asigned tothe targets that are toofaint.
        confidence_interval: [float, optional]
            The desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
        single_bayesian_for_nolum_target: [bool, optional] Default: True
            Whether to still run a single Bayesian for the target that does not have good luminosity measurement (too bright or faint or anyother). If True, will still run a single Bayesian method to derive the stellar mass with the assumed `median_age`, otherwise will only find the closest track and will not obtain an uncertainty. Turn this to False to simply find the closest model grid point as in Pascucci+2016.
    
    Returns:
    
        best_logmass_output: [array]
            Array containing the best-fit masses and uncertainties (represent as lower and upper boundaries of the confidence interval).
        best_logage_output: [array]
            Array containing the best-fit ages and uncertainties (represent as lower and upper boundaries of the confidence interval).
        lage_all: [dictionary]
            The likelihood function of age for all target
        lmass_all: [dictionary]
            The likelihood function of mass for all target
        flag_all: [list of strs]
            The list of flags (in string) for all target
    """
    
    # Prepare output lists
    # source_info_output = []
    best_logage_output = []
    best_logmass_output = []
    lage_all = {}
    lmass_all = {}
    flag_all = []
    
    # Loop through each star in the source list
    for ii in tqdm.tqdm(df_prop.index):
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print('')
            print(f'Working on: {source_t}')
        
        # Extract current values and uncertainties
        L_this = df_prop.loc[ii, 'Luminosity[Lsun]']
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logL = np.log10(L_this)
        c_logT = np.log10(T_this)

        if no_uncertainties:
            sigma_logL = 0.1  # Assume fixed uncertainty for Luminosity
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else: 
            err_L_this = df_prop.loc[ii, 'e_Luminosity[Lsun]']
            sigma_logL = utils.unc_log10(L_this, err_L_this)

            err_T_this = df_prop.loc[ii, 'e_Teff[K]']
            sigma_logT = utils.unc_log10(T_this, err_T_this)

        # Initialize the isochrone class with default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
                
            if verbose:
                print(f'Adopted the { "Feiden" if T_this > 3900.0 else "Baraffe" } track.')
                
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
            
            if verbose:
                print(f'Adopted the %s track.'%(model))
                
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
            
            if verbose:
                print(f'Adopted the customize track from %s.'%(isochrone_mat_file))
                
        else:
            # raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")
        
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()

        # Check if the source is in the toofaint or toobright lists 
        if np.any([source_t in toofaint, source_t in toobright]):
            if verbose:
                if source_t in toofaint:
                    print('this target %s is too faint, it is likely to have an edge-on disk, so we assign the median age (%.2f Myrs) of the region to the target'%(source_t, median_age))
                    
                elif source_t in toobright:
                    print('this target %s is too bright, so we assign the smallest age to this target.'%(source_t))
            
            # Handle special cases for faint or bright stars
            if source_t in toofaint:
                c_age = median_age
            else:  # too bright
                c_age = np.min(log_age_dummy)

            if single_bayesian_for_nolum_target:
                res = derive_stellar_mass_assuming_age(df_prop.loc[[ii]], assumed_age=c_age, model=model, isochrone_data_dir=isochrone_data_dir, isochrone_mat_file=isochrone_mat_file, no_uncertainties=no_uncertainties, confidence_interval=confidence_interval, verbose=verbose, plot=plot)
                best_logmass_wunc = res[0]
            else:
                if verbose:
                    print('we find the closest point from the model to this target (%s) instead of using Bayesian framework'%(source_t))
                res = derive_stellar_mass_assuming_age_closest_trk(df_prop.loc[[ii]], assumed_age=1.5e6, model=model, isochrone_data_dir=isochrone_data_dir, isochrone_mat_file=isochrone_mat_file, verbose=verbose)
                best_logmass_wunc = [res[0], np.nan, np.nan]
            
            # this_age = np.where(log_age_dummy == c_age)
            # Tdiff_index = np.abs(logtlogl_dummy[this_age, :, 0] - c_logT).argmin()
            
            """
            the targets that are too bright or too faint are are assigned with age without uncertainties
            """
            # best_mass = [np.log10(masses_dummy[Tdiff_index]), np.nan, np.nan]
            best_logage_wunc = [c_age, np.nan, np.nan]
            
        else:
            # Compute the likelihood using the Bayesian framework
            lfunc = utils.get_likelihood_p2016(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL)
            lfunc[np.isnan(lfunc)] = 1e-99 # Set NaN positions to 1e-99 to ignore them
            
            # Create the mask to mask out the trks after zero-age-main-sequence
            _, _, mask_pms = utils.find_zams_curve(isochrone)
            lfunc[np.logical_not(mask_pms)] = 1e-99 # Set the main-sequence and post-main-sequence positions to 1e-99
            
            # Use Bayesian mass and age estimation
            bayes_res, lage_res, lmass_res = bayesian_mass_age(log_age_dummy, np.log10(masses_dummy), lfunc, plot=plot, source=source_t, verbose=verbose, save_fig=save_fig, fig_save_dir=fig_save_dir, confidence_interval=confidence_interval)
            best_logmass_wunc = [bayes_res[2], bayes_res[3][0], bayes_res[3][1]]
            best_logage_wunc = [bayes_res[0], bayes_res[1][0], bayes_res[1][1]]

            # Store likelihood results
            lage_all[f'target_{ii}'] = lage_res
            lmass_all[f'target_{ii}'] = lmass_res

            # Save the likelihood functions if requested
            if save_lfunc:
                df_lage = pd.DataFrame(lage_res.T, columns=['logage[yrs]', 'Lage'])
                df_lmass = pd.DataFrame(lmass_res.T, columns=['logmass[Msun]', 'Lmass'])
                if not os.path.exists(csv_save_dir):
                    os.makedirs(csv_save_dir)
                df_lage.to_csv(os.path.join(csv_save_dir, f'{source_t}_lage.csv'), index=False)
                df_lmass.to_csv(os.path.join(csv_save_dir, f'{source_t}_lmass.csv'), index=False)

        # # Save the best-fit mass and age results
        # if no_uncertainties:
        #     source_info_output.append([source_t, T_this, L_this])
        # else:
        #     source_info_output.append([source_t, T_this, df_prop.loc[ii, 'e_Teff[K]'], L_this, df_prop.loc[ii, 'e_Luminosity[Lsun]']])
        
        best_logmass_output.append(best_logmass_wunc)
        best_logage_output.append(best_logage_wunc)
        
        if verbose:
            print(f'Results for target: {source_t}')
            print(f'Best Mass: {10**best_logmass_wunc[0]:.2f} [Msun], Age: {10**best_logage_wunc[0]:.2e} [yrs]')

        if source_t in toobright:        
            flag_all.append('toobright')
        elif source_t in toofaint:
            flag_all.append('toofaint')
        else:
            flag_all.append('good')
        
    return np.array(best_logmass_output), np.array(best_logage_output), lmass_all, lage_all, flag_all


def derive_stellar_mass_age_legacy(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68, single_bayesian_for_nolum_target=False):
    """
    Derives stellar mass and age from evolutionary tracks using a Bayesian framework.
    This is the method with the criteria that has been used in Pascucci2016

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff, Luminosity, etc.).
            The formated column needs to be: ['Source', 'Teff[K]', 'e_Teff[K]', 'Luminosity[Lsun]', 'e_Luminosity[Lsun]']
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
        isochrone_data_dir: [str, optional]
            The datadir where all the data files for the isochrones are stored
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use
            This is needed if you want to set the model as 'customize'.
        no_uncertainties: [bool, optional]
            Whether to assume no uncertainties in Teff and Luminosity (default: False).
        plot: [bool, optional]
            Whether to plot the likelihood distributions (default: False).
        save_fig: [bool, optional]
            Whether to save the figure (default: False).
        save_lfunc: [bool, optional]
            Whether to save the likelihood functions to CSV (default: False).
        fig_save_dir: [str, optional]
            Directory where figures are saved if save_fig is True (default: 'figures').
        csv_save_dir: [str, optional]
            Directory where likelihood function data is saved if save_lfunc is True (default: 'lfunc_data').
        verbose: [bool, optional]
            Whether to print verbose output (default: False).
        toofaint: [list, optional]
            A list of target names (in the 'Source' column) that are toofaint, 
            will assign the median age (that is setup here) to them. If this one is not empty, `median_age` needs to be assigned.
        toobright: [list, optional]
            A list of target names (in the 'Source' column) that are toobirght, 
            will assign the minimum age in the read in evolutionary tracks to them. If this one is not empty, `median_age` needs to be assigned.
        median_age: [float, optional] unit: Myrs
            The median age that will be asigned tothe targets that are toofaint.
        confidence_interval: [float, optional]
            The desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
        single_bayesian_for_nolum_target: [bool, optional]
            Whether to still run a single Bayesian for the target that does not have good luminosity measurement (too bright or faint or anyother). If True, will still run a single Bayesian method to derive the stellar mass with the assumed `median_age`, otherwise will only find the closest track and will not obtain an uncertainty.
    
    Returns:
    
        best_logmass_output: [array]
            Array containing the best-fit masses and uncertainties (represent as lower and upper boundaries of the confidence interval).
        best_logage_output: [array]
            Array containing the best-fit ages and uncertainties (represent as lower and upper boundaries of the confidence interval).
        lage_all: [dictionary]
            The likelihood function of age for all target
        lmass_all: [dictionary]
            The likelihood function of mass for all target
    """
    
    # Prepare output lists
    # source_info_output = []
    best_logage_output = []
    best_logmass_output = []
    lage_all = {}
    lmass_all = {}
    flag_all = []
    
    # Loop through each star in the source list
    for ii in tqdm.tqdm(df_prop.index):
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract current values and uncertainties
        L_this = df_prop.loc[ii, 'Luminosity[Lsun]']
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logL = np.log10(L_this)
        c_logT = np.log10(T_this)

        if no_uncertainties:
            sigma_logL = 0.1  # Assume fixed uncertainty for Luminosity
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else: 
            err_L_this = df_prop.loc[ii, 'e_Luminosity[Lsun]']
            sigma_logL = utils.unc_log10(L_this, err_L_this)

            err_T_this = df_prop.loc[ii, 'e_Teff[K]']
            sigma_logT = utils.unc_log10(T_this, err_T_this)

        # Initialize the isochrone class with default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
                
            if verbose:
                print(f'Adopted the { "Feiden" if T_this > 3900.0 else "Baraffe" } track.')
                
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
            
            if verbose:
                print(f'Adopted the %s track.'%(model))
                
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
            
            if verbose:
                print(f'Adopted the customize track from %s.'%(isochrone_mat_file))
                
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()

        # Check if the source is in the toofaint or toobright lists
        if np.any([source_t in toofaint, source_t in toobright]):
            if verbose:
                if source_t in toofaint:
                    print('this target %s is too faint, it is likely to have an edge-on disk, so we assign the median age (%.2f Myrs) of the region to the target'%(source_t, median_age))
                    
                elif source_t in toobright:
                    print('this target %s is too bright, so we assign the smallest age to this target.'%(source_t))
            
            # Handle special cases for faint or bright stars
            if source_t in toofaint:
                c_age = median_age
            else:  # too bright
                c_age = np.min(log_age_dummy)

            if single_bayesian_for_nolum_target:
                res = derive_stellar_mass_assuming_age(df_prop.loc[[ii]], assumed_age=c_age, model=model, isochrone_data_dir=isochrone_data_dir, isochrone_mat_file=isochrone_mat_file, no_uncertainties=no_uncertainties, confidence_interval=confidence_interval, verbose=verbose, plot=plot)
                best_logmass_wunc = res[0]
            else:
                res = derive_stellar_mass_assuming_age_closest_trk(df_prop.loc[[ii]], assumed_age=1.5e6, model=model, isochrone_data_dir=isochrone_data_dir, isochrone_mat_file=isochrone_mat_file, verbose=verbose)
                best_logmass_wunc = [res[0], 0, 0]
            
            # this_age = np.where(log_age_dummy == c_age)
            # Tdiff_index = np.abs(logtlogl_dummy[this_age, :, 0] - c_logT).argmin()
            
            """
            In this legacy version, the targets that are too bright or too faint are are assigned with age without uncertainties
            """
            # best_mass = [np.log10(masses_dummy[Tdiff_index]), 0, 0]
            best_logage_wunc = [c_age, np.nan, np.nan]
        else:
            # Compute the likelihood using the Bayesian framework
            lfunc = utils.get_likelihood_p2016(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL)
            lfunc[np.isnan(lfunc)] = 1e-99 # Set NaN positions to 1e-99 to ignore them
            
            """
            In this legacy version, we do not consider where is the zams curve
            we simply remove all the tracks beyond 50 Myrs
            """
            # # Create the mask to mask out the trks after zero-age-main-sequence
            # _, _, mask_pms = utils.find_zams_curve(isochrone)
            # lfunc[np.logical_not(mask_pms)] = 1e-99 # Set the main-sequence and post-main-sequence positions to 1e-99
            idx_age = np.nanargmin(np.abs(isochrone.log_age - np.log10(50.0e6)))  # Find the closest age
            lfunc[idx_age:, :] = 1e-99
            
            # Use Bayesian mass and age estimation
            bayes_res, lage_res, lmass_res = bayesian_mass_age(log_age_dummy, np.log10(masses_dummy), lfunc, plot=plot, source=source_t, verbose=verbose, save_fig=save_fig, fig_save_dir=fig_save_dir, confidence_interval=confidence_interval)
            best_logmass_wunc = [bayes_res[2], bayes_res[3][0], bayes_res[3][1]]
            best_logage_wunc = [bayes_res[0], bayes_res[1][0], bayes_res[1][1]]

            # Store likelihood results
            lage_all[f'target_{ii}'] = lage_res
            lmass_all[f'target_{ii}'] = lmass_res

            # Save the likelihood functions if requested
            if save_lfunc:
                df_lage = pd.DataFrame(lage_res.T, columns=['logage[yrs]', 'Lage'])
                df_lmass = pd.DataFrame(lmass_res.T, columns=['logmass[Msun]', 'Lmass'])
                if not os.path.exists(csv_save_dir):
                    os.makedirs(csv_save_dir)
                df_lage.to_csv(os.path.join(csv_save_dir, f'{source_t}_lage.csv'), index=False)
                df_lmass.to_csv(os.path.join(csv_save_dir, f'{source_t}_lmass.csv'), index=False)

        # # Save the best-fit mass and age results
        # if no_uncertainties:
        #     source_info_output.append([source_t, T_this, L_this])
        # else:
        #     source_info_output.append([source_t, T_this, df_prop.loc[ii, 'e_Teff[K]'], L_this, df_prop.loc[ii, 'e_Luminosity[Lsun]']])
        
        best_logmass_output.append(best_logmass_wunc)
        best_logage_output.append(best_logage_wunc)
        
        if verbose:
            print(f'Results for target: {source_t}')
            print(f'Best Mass: {10**best_logmass_wunc[0]:.2f} [Msun], Age: {10**best_logage_wunc[0]:.2e} [yrs]')

        if source_t in toobright:        
            flag_all.append('toobright')
        elif source_t in toofaint:
            flag_all.append('toofaint')
        else:
            flag_all.append('good')
        
    return np.array(best_logmass_output), np.array(best_logage_output), lmass_all, lage_all, flag_all


def derive_stellar_mass_age_closest_track(df_prop,  model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', verbose=False):
    """
    Derives stellar mass and age by picking the closest point from the isochrone grid based on Teff and Luminosity.

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff, Luminosity, etc.).
            The format for the columns needs to be: ['Source', 'Teff[K]', 'Luminosity[Lsun]']
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
        isochrone_data_dir: [str, optional] 
            The directory where the isochrone data is stored.
            Default = None, and data will be saved to './isochrone_data'
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use
            This is needed if you want to set the model as 'customize'.
        verbose: [bool, optional]
            Whether to print verbose output. Default is False.

    Returns:
    
        best_mass_output: [array] unit Msolar
            Array containing the closest log10mass for each star.
        best_age_output: [array] unit yr
            Array containing the closest log10age for each star.
    """
    
    # Prepare output lists
    best_mass_output = []
    best_age_output = []

    # Loop through each star in the source list
    for ii in tqdm.tqdm(df_prop.index):
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract current values
        L_this = df_prop.loc[ii, 'Luminosity[Lsun]']
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logL = np.log10(L_this)
        c_logT = np.log10(T_this)

        # Initialize the isochrone class with default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # # Select tracks based on model
        # if model == 'Baraffe_n_Feiden':
        #     # Select appropriate evolutionary tracks based on Teff
        #     if T_this > 3900.0:
        #         isochrone.set_tracks('Feiden2016')
        #     else:
        #         isochrone.set_tracks('Baraffe2015')
        # elif model == 'Feiden2016':
        #     isochrone.set_tracks('Feiden2016')
        # elif model == 'Baraffe2015':
        #     isochrone.set_tracks('Baraffe2015')
        # else:
        #     raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Feiden2016', or 'Baraffe2015'.")
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        
        # Create a mask for NaNs in logtlogl_dummy
        nan_mask = np.isnan(logtlogl_dummy[:, :, 0]) | np.isnan(logtlogl_dummy[:, :, 1])
        
        # Create the mask to mask out the trks after zero-age-main-sequence
        _, _, mask_pms = utils.find_zams_curve(isochrone)
        
        # Find the closest point on the grid
        distance_grid = np.sqrt((logtlogl_dummy[:, :, 0] - c_logT)**2 + (logtlogl_dummy[:, :, 1] - c_logL)**2)
        distance_grid[nan_mask] = np.inf  # Set NaN positions to infinity to ignore them
        distance_grid[np.logical_not(mask_pms)] = np.inf  # Set the main-sequence and post-main-sequence positions to inf
        
        idx_age, idx_mass = np.unravel_index(np.nanargmin(distance_grid), distance_grid.shape)
        
        best_age = log_age_dummy[idx_age]
        best_mass = np.log10(masses_dummy[idx_mass])

        best_age_output.append(best_age)
        best_mass_output.append(best_mass)

        if verbose:
            print(f"Closest match for {source_t}: Age = {10**best_age:.2e} yrs, Mass = {10**best_mass:.2e} Msun")
    
    return np.array(best_mass_output), np.array(best_age_output)


def derive_stellar_mass_assuming_age(df_prop, assumed_age, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, confidence_interval=0.68, verbose=False, plot=False, prior_mass=None, prior_normalize='maxone'):
    """
    Derives stellar mass assuming a known age, even when luminosity is unavailable, considering uncertainties in Teff.

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff) and (optional) Luminosity. 
            The formatted column needs to be: ['Source', 'Teff[K]', 'e_Teff[K]']
        assumed_age: [float] unit yrs
            The assumed age of the stars (in years). Can be a single value or an array.
        e_assumed_age: [float, optional] unit yrs (NOT considered for now)
            Uncertainty in the assumed age. Can be a single value or an array. Default is None.
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
        isochrone_data_dir: [str, optional]
            The directory where the isochrone data is stored.
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use
            This is needed if you want to set the model as 'custom'.
        no_uncertainties: [bool, optional]
            Whether to assume no uncertainties in Teff and Luminosity (default: False).
        confidence_interval [float]:
            the desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
        verbose: [bool, optional]
            Whether to print verbose output. Default is False.
        plot: [bool, optional]
            Whether to plot the likelihood function for stellar mass. Default is False.
        prior_mass: [callable or tabulated dict]
            same interface as the derive_stellar_mass_and_age, evaluated on log_masses.
    

    NOTE:
        the e_assumed_age=None has not been considered for now.
    
    Returns:
    
        best_logmass_output: [array]
            Array containing the best-fit masses and uncertainties (represent as lower and upper boundaries of the confidence interval).
    """
    
    # Prepare output list for the masses and their uncertainties
    best_logmass_output = []
    # mass_uncertainties = []

    # # If e_assumed_age is not provided, set it to 0 (no uncertainty)
    # if e_assumed_age is None:
    #     e_assumed_age = np.zeros(len(df_prop)) if isinstance(assumed_age, (list, np.ndarray)) else 0

    # Loop through each star in the source list
    for ii in df_prop.index:
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract the stellar Teff and its uncertainty
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logT = np.log10(T_this)
        
        if no_uncertainties:
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else: 
            err_T_this = df_prop.loc[ii, 'e_Teff[K]']
            sigma_logT = utils.unc_log10(T_this, err_T_this)
        
        # Get the assumed age and its uncertainty for this star
        c_log_age = np.log10(assumed_age) if isinstance(assumed_age, (float, int)) else np.log10(assumed_age[ii])
        # sigma_log_age = utils.unc_log10(e_assumed_age) if isinstance(e_assumed_age, (float, int)) else utils.unc_log10(e_assumed_age[ii])
        
        # Initialize the isochrone class with the default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        log_masses_dummy = np.log10(masses_dummy)
        
        # Create a mask for NaNs in logtlogl_dummy
        nan_mask = np.isnan(logtlogl_dummy[:, :, 0])

        # Create the mask to mask out the trks after zero-age-main-sequence
        _, _, mask_pms = utils.find_zams_curve(isochrone)
        
        # Find the closest log10(age) in the grid (closest age slice)
        idx_age = np.argmin(np.abs(log_age_dummy - c_log_age))
        
        # Create a likelihood function based on Teff matching
        # likelihood = np.exp(-0.5 * ((logtlogl_dummy[idx_age, :, 0] - c_logT) ** 2) / e_Teff_this**2)
        fT = ((logtlogl_dummy[idx_age, :, 0]) - c_logT)**2 / sigma_logT**2
        likelihood = np.exp(-0.5 * fT)
        # apply masks (use a tiny floor instead of 0 to keep integrals finite)
        tiny = 1e-300
        likelihood[nan_mask[idx_age, :]] = tiny
        likelihood[~mask_pms[idx_age, :]] = tiny
        # likelihood[nan_mask[idx_age, :]] = np.nanmin(likelihood) # 1e-99  # Ignore NaNs
        # likelihood[np.logical_not(mask_pms)[idx_age, :]] = np.nanmin(likelihood) # 1e-99 # Ignore main-sequence and post-main-sequence positions
        
        # Normalize the likelihood (simple routine)
        # likelihood /= simpson(likelihood, x=np.log10(masses_dummy)) 
        # normalize over log-mass axis (a safer routine)
        denom = simpson(likelihood, x=log_masses_dummy)
        if not np.isfinite(denom) or denom <= 0:
            # fallback to discrete sum if Simpson fails (e.g., degenerate grid)
            denom = np.nansum(likelihood)
        if denom > 0:
            likelihood = likelihood / denom
        else:
            # if completely collapsed, make it uniform over valid (rare)
            valid = np.isfinite(likelihood) & (likelihood > 0)
            if np.any(valid):
                likelihood = valid.astype(float) / np.sum(valid)
            else:
                likelihood = np.ones_like(likelihood) / likelihood.size

        # ===== NEW in v1.0.1: apply mass prior on log_masses_dummy =====
        prior_1d = utils._eval_1d_prior_on_grid(prior_mass, log_masses_dummy,
                                          normalize=prior_normalize, name='prior_mass')
        posterior = np.clip(likelihood, 0.0, np.inf) * np.clip(prior_1d, 0.0, np.inf)
        
        # re-normalize posterior
        denom_post = simpson(posterior, x=log_masses_dummy)
        if not np.isfinite(denom_post) or denom_post <= 0:
            denom_post = np.nansum(posterior)
        if denom_post > 0:
            posterior = posterior / denom_post
        else:
            # if prior collapsed everything, fall back to likelihood
            posterior = likelihood
        
        # Find the best-fit mass
        # best_mass_idx = np.argmax(likelihood)
        # best_log_mass = np.log10(masses_dummy[best_mass_idx])
        best_mass_idx = int(np.nanargmax(posterior))
        best_log_mass = log_masses_dummy[best_mass_idx]
        
        if verbose:
            print(f"Best match for {source_t}: Age = {10**c_log_age:.2e} yrs, Mass = {10**best_log_mass:.2e} Msun")
        
        # Calculate uncertainties in mass based on the likelihood distribution
        # likelihood_cumsum = np.cumsum(likelihood) / np.sum(likelihood)
        # half_sigma_perc = confidence_interval/2.0
        # lower_bound_perc = 0.5 - half_sigma_perc
        # upper_bound_perc = 1.0 - lower_bound_perc
        # lower_bound_idx = np.argmin(np.abs(likelihood_cumsum - lower_bound_perc))  # default 16th percentile
        # upper_bound_idx = np.argmin(np.abs(likelihood_cumsum - upper_bound_perc))  # default 84th percentile
        
        # credible interval from posterior CDF
        cdf = np.cumsum(posterior)
        cdf /= cdf[-1] if cdf[-1] > 0 else 1.0
        half = confidence_interval / 2.0
        lo_p, hi_p = 0.5 - half, 0.5 + half

        lower_bound_idx = int(np.argmin(np.abs(cdf - lo_p)))
        upper_bound_idx = int(np.argmin(np.abs(cdf - hi_p)))
        
        # Uncertainties in log10(mass)
        lower_mass = np.log10(masses_dummy[lower_bound_idx])
        upper_mass = np.log10(masses_dummy[upper_bound_idx])
        # mass_unc = [best_log_mass - lower_mass, upper_mass - best_log_mass]
        # mass_uncertainties.append(mass_unc)
        
        best_logmass_wunc = [best_log_mass, lower_mass, upper_mass]
        best_logmass_output.append(best_logmass_wunc)
        
        # Optionally plot the likelihood function for stellar mass
        if plot:
            plotting.plot_likelihood_1d(np.log10(masses_dummy), likelihood, best_log_mass, lower_mass, upper_mass, source=source_t)

    return np.array(best_logmass_output)


def derive_stellar_mass_assuming_age_closest_trk(df_prop, assumed_age, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', verbose=False):
    """
    Derives stellar mass assuming a known age by finding the closest track on the isochrone grid based on Teff, without using the Bayesian method.

    Args:
    
        df_prop: [DataFrame]
            DataFrame containing stellar properties (Teff) and (optional) Luminosity. 
            The format for the columns needs to be: ['Source', 'Teff[K]', 'e_Teff[K]']
        assumed_age: [float] unit yrs
            The assumed age of the stars (in years). Can be a single value or an array.
        model: [str, optional] Default: 'Baraffe_n_Feiden'
            Model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2', 'MIST_v1p2' (same as 'MIST') or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file.
        isochrone_data_dir: [str, optional]
            The directory where the isochrone data is stored.
        isochrone_mat_file: [str, optional] Default = ''
            The ABSOLUTE directory for the matrix file for the isochrones that you want to use if using a custom model.
        verbose: [bool, optional]
            Whether to print verbose output. Default is False.

    Returns:
    
        best_log_mass_output: [array] in Msolar
            Array containing the closest log10 mass for each star.
    """
    
    # Prepare output list for the masses
    best_log_mass_output = []

    # Loop through each star in the source list
    for ii in df_prop.index:
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract the stellar Teff and its uncertainty
        T_this = df_prop.loc[ii, 'Teff[K]']
        c_logT = np.log10(T_this)
        
        # Initialize the isochrone class with the default data directory
        isochrone = Isochrone(isochrone_data_dir)
        
        # Select tracks based on model
        if model.lower() == 'baraffe_n_feiden':
            # Select appropriate evolutionary tracks based on Teff
            if T_this > 3900.0:
                isochrone.set_tracks('Feiden2016')
            else:
                isochrone.set_tracks('Baraffe2015')
        elif model.lower() in ['baraffe2015', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2', 'feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic', 'feiden2016_b', 'feiden2016_magnetic', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'customize':
            isochrone.set_tracks('customize', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        
        # Create a mask for NaNs in logtlogl_dummy
        nan_mask = np.isnan(logtlogl_dummy[:, :, 0])

        # Create the mask to mask out the trks after zero-age-main-sequence
        _, _, mask_pms = utils.find_zams_curve(isochrone)
        
        # Find the closest log10(age) in the grid
        c_log_age = np.log10(assumed_age) if isinstance(assumed_age, (float, int)) else np.log10(assumed_age[ii])
        idx_age = np.argmin(np.abs(log_age_dummy - c_log_age))
        
        # Find the closest mass based on the distance in Teff
        distance_grid = np.abs(logtlogl_dummy[idx_age, :, 0] - c_logT)
        distance_grid[nan_mask[idx_age, :]] = np.inf  # Ignore NaNs by setting them to infinity
        distance_grid[np.logical_not(mask_pms)[idx_age, :]] = np.inf  # Ignore main-sequence and post-main-sequence positions
        
        best_mass_idx = np.argmin(distance_grid)
        best_log_mass = np.log10(masses_dummy[best_mass_idx])

        best_log_mass_output.append(best_log_mass)

        if verbose:
            print(f"Closest match for {source_t}: Age = {10**c_log_age:.2e} yrs, Mass = {10**best_log_mass:.2e} Msun")
    
    return np.array(best_log_mass_output)
