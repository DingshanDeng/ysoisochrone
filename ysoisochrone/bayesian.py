import os, sys, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.interpolate import interp1d

from ysoisochrone import plotting
from ysoisochrone import utils
from ysoisochrone.isochrone import Isochrone

def bayesian_mass_age(log_age_dummy, log_masses_dummy, L, plot=False, source=None, confidence_interval=0.68, verbose=False, save_fig=False, fig_save_dir='figure', customized_fig_name=''):
    ''' 
    derive the mass and ages for a star from a likelihood distribution
    
    Args:
    ------------
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
    
    Returns:
    ------------
    A tupe with three things: [0] best age and mass and their uncertainties; [1] the logage array and its likelihood function; [2] the logmass array and its likelihood function.
    [best_age, age_unc, best_mass, mass_unc], np.array([log_age_dummy, L_age_norm]), np.array([log_masses_dummy, L_mass_norm])
    '''
    
    half_sigma_perc = confidence_interval/2.0
    
    # if verbose: # for debugging
    #     print('the shape of logage', log_age_dummy.shape)   
    #     print('the shape of logmass', log_masses_dummy.shape)
    #     print('the shape of L', L.shape)
        
    # Integrate L over mstar for each age bin
    L_age = np.array([simps(L[jj, :], log_masses_dummy) for jj in range(len(log_age_dummy))])
    L_age /= simps(L_age, log_age_dummy)
    
    # if verbose: # for debugging
    #     print('L_age:', L_age)
    #     print(np.cumsum(L_age))
    #     print(np.cumsum(L_age)/np.sum(L_age))
    
    best_age_idx = np.argmax(L_age)
    best_age = log_age_dummy[best_age_idx]
    
    L_age_array = np.cumsum(L_age) / np.sum(L_age)
    age_low_idx = np.argmin(np.abs(L_age_array[:best_age_idx] - (L_age_array[best_age_idx] - half_sigma_perc)))
    age_up_idx = best_age_idx + np.argmin(np.abs(L_age_array[best_age_idx:] - (L_age_array[best_age_idx] + half_sigma_perc)))
    
    age_unc = [log_age_dummy[age_low_idx], log_age_dummy[age_up_idx]]
    
    if age_unc[0] != best_age and age_unc[1] != best_age:
        if age_unc[0] == min(log_age_dummy) or age_unc[1] == max(log_age_dummy):
            if age_unc[0] == min(log_age_dummy):
                age_unc[0] = log_age_dummy[np.argmin(np.abs(L_age_array[:best_age_idx] - (L_age_array[best_age_idx] - half_sigma_perc)))]
            else:
                age_unc[1] = log_age_dummy[best_age_idx + np.argmin(np.abs(L_age_array[best_age_idx:] - (L_age_array[best_age_idx] + half_sigma_perc)))]
    
    # Integrate L over age for each mass bin
    L_mass = np.array([simps(L[:, jj], log_age_dummy) for jj in range(len(log_masses_dummy))])
    L_mass /= simps(L_mass, log_masses_dummy)
    
    best_mass_idx = np.argmax(L_mass)
    best_log_mass = best_mass = log_masses_dummy[best_mass_idx]
    
    L_mass_array = np.cumsum(L_mass) / np.sum(L_mass)
    mass_low_idx = np.argmin(np.abs(L_mass_array[:best_mass_idx] - (L_mass_array[best_mass_idx] - half_sigma_perc)))
    mass_up_idx = best_mass_idx + np.argmin(np.abs(L_mass_array[best_mass_idx:] - (L_mass_array[best_mass_idx] + half_sigma_perc)))
    
    # Handle cases where the cumulative sum exceeds the desired confidence interval
    if L_mass_array[best_mass_idx] + half_sigma_perc > 1:
        i_idx = best_mass_idx
        key = 0
        while key == 0:
            i_idx = int(i_idx) + 1
            if np.abs(L_mass_array[i_idx] - 1) < 1e-10:
                key = 1
                mass_up_idx = i_idx
                
    if L_mass_array[best_mass_idx] - half_sigma_perc < 0:
        i_idx = best_mass_idx
        key = 0
        while key == 0:
            i_idx = int(i_idx) - 1
            if L_mass_array[i_idx] < 1e-10:
                key = 1
                mass_low_idx = i_idx
    
    if verbose:
        print('sum of Lmass', np.sum(L_mass))
        print('the last index of Lmass', L_mass[-1])
        print('sum of Lmass array', np.sum(L_mass_array))
        print('the last index of Lmass array', L_mass_array[-1])
        print('the best mass and its index: ', best_log_mass, best_mass_idx, L_mass_array[best_mass_idx])
        print('lw: ', log_masses_dummy[mass_low_idx], mass_low_idx, L_mass_array[mass_low_idx])
        print('up: ', log_masses_dummy[mass_up_idx], mass_up_idx, L_mass_array[mass_up_idx])
        print('check the L_mass_array, it should be 0.68 between the two index')
        print(L_mass_array[mass_up_idx] - L_mass_array[mass_low_idx])
    
    mass_unc = [log_masses_dummy[mass_low_idx], log_masses_dummy[mass_up_idx]]
    
    if mass_unc[0] != best_mass and mass_unc[1] != best_mass:
        if mass_unc[0] == min(log_masses_dummy) or mass_unc[1] == max(log_masses_dummy):
            if mass_unc[0] == min(log_masses_dummy):
                mass_unc[0] = log_masses_dummy[np.argmin(np.abs(L_mass_array[:best_mass_idx] - (L_mass_array[best_mass_idx] - half_sigma_perc)))]
            else:
                raise ValueError('The mass is the largest in the grid. This needs to be sorted out!')
    
    #
    # save the normalized probability distributions
    #
    L_age_norm = L_age / np.trapz(L_age, log_age_dummy) # / max(L_age) * (max(log_masses_dummy) - min(log_masses_dummy)) # + min(log_masses_dummy)
    L_mass_norm = L_mass / np.trapz(L_mass, log_masses_dummy) # / max(L_mass) * (max(log_age_dummy) - min(log_age_dummy)) # + min(log_age_dummy)
    
    if plot:
        plotting.plot_bayesian_results(log_age_dummy, log_masses_dummy, L, best_age, best_mass, age_unc, mass_unc, source, save_fig, fig_save_dir, customized_fig_name)
    
    return [best_age, age_unc, best_mass, mass_unc], np.array([log_age_dummy, L_age_norm]), np.array([log_masses_dummy, L_mass_norm])


def derive_stellar_mass_age(df_prop, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', no_uncertainties=False, plot=False, save_fig=False, save_lfunc=False, fig_save_dir='figures', csv_save_dir='lfunc_data', verbose=False, toofaint=[], toobright=[], median_age=1.0, confidence_interval=0.68):
    """
    Derives stellar mass and age from evolutionary tracks using a Bayesian framework.
    This is the method with the criteria that has been used in Pascucci2016

    Args:
    ------------
    df_prop: [DataFrame]
        DataFrame containing stellar properties (Teff, Luminosity, etc.).
        The formated column needs to be: ['Source', 'Teff', 'e_Teff', 'Luminosity', 'e_Luminosity']
    model: [str, optional] Default: 'Baraffe_n_Feiden'
        model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
    isochrone_data_dir: [str, optional]
        The datadir where all the data files for the isochrones are stored
    isochrone_mat_file: [str, optional] Default = ''
        The ABSOLUTE directory for the matrix file for the isochrones that you want to use
        This is needed if you want to set the model as 'custome'.
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
    toofaint: [list]
        A list of target names (in the 'Source' column) that are toofaint, 
        will assign the median age (that is setup here) to them.
    toobright: [list]
        A list of target names (in the 'Source' column) that are toobirght, 
        will assign the minimum age in the read in evolutionary tracks to them.
    median_age: [float] unit: Myrs
        The median age that will be asigned tothe targets that are toofaint.
    confidence_interval [float]:
        the desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
    
    Output:
    ------------
    Returns:
    ------------
    best_mass_output: [list]
        List containing the best-fit masses and uncertainties.
    best_age_output: [list]
        List containing the best-fit ages and uncertainties.
    lage_all: [dictionary]
        The likelihood function of age for all target
    lmass_all: [dictionary]
        The likelihood function of mass for all target
    """
    
    # Prepare output lists
    source_info_output = []
    best_age_output = []
    best_mass_output = []
    lage_all = {}
    lmass_all = {}
    
    # Loop through each star in the source list
    for ii in df_prop.index:
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract current values and uncertainties
        L_this = df_prop.loc[ii, 'Luminosity']
        T_this = df_prop.loc[ii, 'Teff']
        c_logL = np.log10(L_this)
        c_logT = np.log10(T_this)

        if no_uncertainties:
            sigma_logL = 0.1  # Assume fixed uncertainty for Luminosity
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else: 
            err_L_this = df_prop.loc[ii, 'e_Luminosity']
            sigma_logL = utils.unc_log10(L_this, err_L_this)

            err_T_this = df_prop.loc[ii, 'e_Teff']
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
        elif model.lower() in ['baraffe2015', 'feiden2016', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'custome':
            isochrone.set_tracks('custome', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()

        if verbose:
            print(f'Adopted the { "Feiden" if T_this > 3900.0 else "Baraffe" } track.')

        # Check if the source is in the toofaint or toobright lists
        if np.any([source_t in toofaint, source_t in toobright]):
            # Handle special cases for faint or bright stars
            if source_t in toofaint:
                c_age = median_age
            else:  # too bright
                c_age = np.min(log_age_dummy)

            this_age = np.where(log_age_dummy == c_age)
            Tdiff_index = np.abs(logtlogl_dummy[this_age, :, 0] - c_logT).argmin()
            best_mass = [np.log10(masses_dummy[Tdiff_index]), 0, 0]
            best_age = [c_age, 0, 0]
        else:
            # Compute the likelihood using the Bayesian framework
            lfunc = utils.get_likelihood_andrews2013(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL)
            lfunc[np.isnan(lfunc)] = 1e-99
            
            # Use Bayesian mass and age estimation
            bayes_res, lage_res, lmass_res = bayesian_mass_age(log_age_dummy, np.log10(masses_dummy), lfunc, plot=plot, source=source_t, verbose=verbose, save_fig=save_fig, fig_save_dir=fig_save_dir, confidence_interval=confidence_interval)
            best_mass = [bayes_res[2], bayes_res[3][0], bayes_res[3][1]]
            best_age = [bayes_res[0], bayes_res[1][0], bayes_res[1][1]]

            # Store likelihood results
            lage_all[f'target_{ii}'] = lage_res
            lmass_all[f'target_{ii}'] = lmass_res

            # Save the likelihood functions if requested
            if save_lfunc:
                df_lage = pd.DataFrame(lage_res.T, columns=['logage', 'Lage'])
                df_lmass = pd.DataFrame(lmass_res.T, columns=['logmass', 'Lmass'])
                if not os.path.exists(csv_save_dir):
                    os.makedirs(csv_save_dir)
                df_lage.to_csv(os.path.join(csv_save_dir, f'{source_t}_lage.csv'), index=False)
                df_lmass.to_csv(os.path.join(csv_save_dir, f'{source_t}_lmass.csv'), index=False)

        # Save the best-fit mass and age results
        if no_uncertainties:
            source_info_output.append([source_t, T_this, L_this])
        else:
            source_info_output.append([source_t, T_this, df_prop.loc[ii, 'e_Teff'], L_this, df_prop.loc[ii, 'e_Luminosity']])
        
        best_mass_output.append(best_mass)
        best_age_output.append(best_age)
        
        if verbose:
            print(f'Results for target: {source_t}')
            print(f'Best Mass: {10**best_mass[0]:.2f} [Msun], Age: {10**best_age[0]:.2e} [yrs]')
    
    return best_mass_output, best_age_output, lmass_all, lage_all


def derive_stellar_mass_age_closest_track(df_prop,  model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', verbose=False):
    """
    Derives stellar mass and age by picking the closest point from the isochrone grid based on Teff and Luminosity.

    Args:
    ------------
    df_prop: [DataFrame]
        DataFrame containing stellar properties (Teff, Luminosity, etc.).
        The format for the columns needs to be: ['Source', 'Teff', 'Luminosity']
    model: [str, optional] Default: 'Baraffe_n_Feiden'
        model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
    isochrone_data_dir: [str, optional] 
        The directory where the isochrone data is stored.
        Default = None, and data will be saved to './isochrone_data'
    isochrone_mat_file: [str, optional] Default = ''
        The ABSOLUTE directory for the matrix file for the isochrones that you want to use
        This is needed if you want to set the model as 'custome'.
    verbose: [bool, optional]
        Whether to print verbose output. Default is False.

    Returns:
    ------------
    best_mass_output: [list] unit Msolar
        List containing the closest log10mass for each star.
    best_age_output: [list] unit yr
        List containing the closest log10age for each star.
    """
    
    # Prepare output lists
    best_mass_output = []
    best_age_output = []

    # Loop through each star in the source list
    for ii in df_prop.index:
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract current values
        L_this = df_prop.loc[ii, 'Luminosity']
        T_this = df_prop.loc[ii, 'Teff']
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
        elif model.lower() in ['baraffe2015', 'feiden2016', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'custome':
            isochrone.set_tracks('custome', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        
        # Create a mask for NaNs in logtlogl_dummy
        nan_mask = np.isnan(logtlogl_dummy[:, :, 0]) | np.isnan(logtlogl_dummy[:, :, 1])
        
        # Find the closest point on the grid
        distance_grid = np.sqrt((logtlogl_dummy[:, :, 0] - c_logT)**2 + (logtlogl_dummy[:, :, 1] - c_logL)**2)
        distance_grid[nan_mask] = np.inf  # Set NaN positions to infinity to ignore them
        
        idx_age, idx_mass = np.unravel_index(np.nanargmin(distance_grid), distance_grid.shape)
        
        best_age = log_age_dummy[idx_age]
        best_mass = np.log10(masses_dummy[idx_mass])

        best_age_output.append(best_age)
        best_mass_output.append(best_mass)

        if verbose:
            print(f"Closest match for {source_t}: Age = {10**best_age:.2e} yrs, Mass = {10**best_mass:.2e} Msun")
    
    return best_mass_output, best_age_output


def derive_stellar_mass_assuming_age(df_prop, assumed_age, model='Baraffe_n_Feiden', isochrone_data_dir=None, isochrone_mat_file='', confidence_interval=0.68, verbose=False, plot=False):
    """
    Derives stellar mass assuming a known age, even when luminosity is unavailable, considering uncertainties in Teff.

    Args:
    ------------
    df_prop: [DataFrame]
        DataFrame containing stellar properties (Teff) and (optional) Luminosity. 
        The formatted column needs to be: ['Source', 'Teff', 'e_Teff']
    assumed_age: [float] unit yrs
        The assumed age of the stars (in years). Can be a single value or an array.
    e_assumed_age: [float, optional] unit yrs (NOT considered for now)
        Uncertainty in the assumed age. Can be a single value or an array. Default is None.
    model: [str, optional] Default: 'Baraffe_n_Feiden'
        model for selecting evolutionary tracks: 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix."
    isochrone_data_dir: [str, optional]
        The directory where the isochrone data is stored.
    isochrone_mat_file: [str, optional] Default = ''
        The ABSOLUTE directory for the matrix file for the isochrones that you want to use
        This is needed if you want to set the model as 'custom'.
    confidence_interval [float]:
        the desired percentage for describing uncertainties, default is 68% which is corresponding to the 1 sigma (68%) from Gaussian distribution.
    verbose: [bool, optional]
        Whether to print verbose output. Default is False.
    plot: [bool, optional]
        Whether to plot the likelihood function for stellar mass. Default is False.
    

    NOTE:
    ------------
    the e_assumed_age=None has not been considered for now.
    
    Returns:
    ------------
    best_mass_output: [list] in Msolar
        List containing the derived log10 mass for each star.
    mass_uncertainties: [list]
        List containing the uncertainties in the derived log10 masses for each star.
    """
    
    # Prepare output list for the masses and their uncertainties
    best_mass_output = []
    mass_uncertainties = []

    # # If e_assumed_age is not provided, set it to 0 (no uncertainty)
    # if e_assumed_age is None:
    #     e_assumed_age = np.zeros(len(df_prop)) if isinstance(assumed_age, (list, np.ndarray)) else 0

    # Loop through each star in the source list
    for ii in df_prop.index:
        source_t = df_prop.loc[ii, 'Source']
        if verbose:
            print(f'Working on: {source_t}')
        
        # Extract the stellar Teff and its uncertainty
        T_this = df_prop.loc[ii, 'Teff']
        e_Teff_this = df_prop.loc[ii, 'e_Teff']
        c_logT = np.log10(T_this)
        sigma_logT = utils.unc_log10(T_this, e_Teff_this)
        
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
        elif model.lower() in ['baraffe2015', 'feiden2016', 'parsec', 'parsec_v1p2', 'parsec_v2p0', 'mist', 'mist_v1p2']:
            isochrone.set_tracks(model.lower())
        elif model.lower() == 'custome':
            isochrone.set_tracks('custome', load_file=isochrone_mat_file)
        else:
            raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe_n_Feiden', 'Baraffe2015', 'Feiden2016', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST') or 'custome'. If you want to use the model = 'custome', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")

        # Get the tracks
        log_age_dummy, masses_dummy, logtlogl_dummy = isochrone.get_tracks()
        
        # Create a mask for NaNs in logtlogl_dummy
        nan_mask = np.isnan(logtlogl_dummy[:, :, 0])

        # Find the closest log10(age) in the grid
        idx_age = np.argmin(np.abs(log_age_dummy - c_log_age))
        
        # Create a likelihood function based on Teff matching
        # likelihood = np.exp(-0.5 * ((logtlogl_dummy[idx_age, :, 0] - c_logT) ** 2) / e_Teff_this**2)
        fT = ((logtlogl_dummy[idx_age, :, 0]) - c_logT)**2 / sigma_logT**2
        likelihood = np.exp(-0.5 * fT)
        likelihood[nan_mask[idx_age]] = 1e-99  # Ignore NaNs
        
        # Normalize the likelihood
        likelihood /= simps(likelihood, np.log10(masses_dummy))
        
        # Find the best-fit mass
        best_mass_idx = np.argmax(likelihood)
        best_log_mass = np.log10(masses_dummy[best_mass_idx])
        
        if verbose:
            print(f"Best match for {source_t}: Age = {10**c_log_age:.2e} yrs, Mass = {10**best_log_mass:.2e} Msun")
        
        best_mass_output.append(best_log_mass)
        
        # Calculate uncertainties in mass based on the likelihood distribution
        likelihood_cumsum = np.cumsum(likelihood) / np.sum(likelihood)
        half_sigma_perc = confidence_interval/2.0
        lower_bound_perc = 0.5 - half_sigma_perc
        upper_bound_perc = 1.0 - lower_bound_perc
        lower_bound_idx = np.argmin(np.abs(likelihood_cumsum - lower_bound_perc))  # default 16th percentile
        upper_bound_idx = np.argmin(np.abs(likelihood_cumsum - upper_bound_perc))  # default 84th percentile
        
        # Uncertainties in log10(mass)
        lower_mass = np.log10(masses_dummy[lower_bound_idx])
        upper_mass = np.log10(masses_dummy[upper_bound_idx])
        mass_unc = [best_log_mass - lower_mass, upper_mass - best_log_mass]
        mass_uncertainties.append(mass_unc)
        
        # Optionally plot the likelihood function for stellar mass
        if plot:
            plotting.plot_likelihood_1d(np.log10(masses_dummy), likelihood, best_log_mass, lower_mass, upper_mass, source=source_t)

    return best_mass_output, mass_uncertainties
