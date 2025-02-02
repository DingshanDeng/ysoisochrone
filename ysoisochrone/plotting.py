import numpy as np
import copy
import os

import matplotlib.pyplot as plt
from matplotlib import gridspec

# style = [
#     'seaborn-ticks',
#     {
#     'figure.dpi': 300,
#     'font.size': 12,
#     'image.cmap': 'inferno',
#     'font.family': 'serif',
#     'font.serif': ['Times', 'Times New Roman'] + plt.rcParams['font.serif'],
#     'xtick.top': True,
#     'xtick.direction': 'in',
#     'ytick.right': True,
#     'ytick.direction': 'in',
#     'mathtext.fontset': 'cm'
#     }]
style = [
    {
    'figure.dpi': 300,
    'font.size': 12,
    'image.cmap': 'inferno',
    'font.family': 'serif',
    'font.serif': ['Times', 'Times New Roman'] + plt.rcParams['font.serif'],
    'xtick.top': True,
    'xtick.direction': 'in',
    'ytick.right': True,
    'ytick.direction': 'in',
    'mathtext.fontset': 'cm'
    }]
plt.style.use(style)

from ysoisochrone import utils
from ysoisochrone import isochrone

def plot_bayesian_results(log_age_dummy, log_masses_dummy, L, best_age, best_mass, age_unc, mass_unc, source=None, save_fig=False, fig_save_dir='figure', customized_fig_name='', color_bestfit='red', color_likelihood='blue', cmap_likelihood='viridis'):
    """
    Plots the likelihood distributions and the best-fit age and mass.

    Args:
    
        log_age_dummy: [array]
            The log of stellar ages.
        log_masses_dummy: [array]
            The log of stellar masses.
        L: [2D array]
            The likelihood function grid.
        best_age: [float]
            The best-fit age in log scale.
        best_mass: [float]
            The best-fit mass in log scale.
        age_unc: [list]
            The uncertainty range for age.
        mass_unc: [list]
            The uncertainty range for mass.
        source: [str, optional]
            The source name for labeling the plot.
        save_fig: [bool, optional]
            Whether to save the figure.
        fig_save_dir: [str, optional]
            Directory to save the figure if save_fig is True.
        customized_fig_name [str, optional]: 
            Customized figure name.
        color_bestfit [str, optional]:
            Customized color to show the best fit point and uncertainties
        color_likelihood [str, optional]:
            Customized color to show the the likelihood function
        cmap_likelihood [str, optional]:
            Customized color to show the the likelihood cmap
        
    Output:
    
        a formatted figure (or save to the fig_save_dir)
    
    Returns:
    
        1 if the code could be ran through
    """
    
    fig = plt.figure(figsize=(6, 5), dpi=300)
    # Use constrained_layout=True to automatically adjust spacing
    fig.subplots_adjust(wspace=0.05, hspace=0.05)
    
    # ratio = 3
    # gs = plt.GridSpec(ratio+1, ratio+1)
    # # gs = plt.GridSpec(4, 4, figure=fig, width_ratios=[1, 1, 1, 0.1], height_ratios=[0.25, 1, 1, 1])
    
    # ax_joint = fig.add_subplot(gs[1:, :-1])
    # ax_marg_x = fig.add_subplot(gs[0, :-1], sharex=ax_joint)
    # ax_marg_y = fig.add_subplot(gs[1:, -1], sharey=ax_joint)
    # # Define a new axis for the colorbar
    # cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.7])  # [left, bottom, width, height]
    
    # Define the size of the main grid for the panels
    grid_width = 0.8  # Fraction of the figure width allocated to the grid (80%)
    grid_height = 0.8  # Fraction of the figure height allocated to the grid (80%)

    # Define the positions of the grid and colorbar
    left_margin = 0.1  # Left margin for the grid
    bottom_margin = 0.1  # Bottom margin for the grid
    colorbar_width = 0.03  # Width of the colorbar
    spacing = 0.02  # Spacing between the grid and the colorbar

    # Create the main grid layout
    gs = gridspec.GridSpec(
        4, 4,
        left=left_margin,
        bottom=bottom_margin,
        right=left_margin + grid_width,
        top=bottom_margin + grid_height,
        wspace=0.05, hspace=0.05
    )

    # Axes for the main panels
    ax_marg_x = fig.add_subplot(gs[0, :-1])  # Top marginal plot
    ax_joint = fig.add_subplot(gs[1:, :-1])  # Main joint plot
    ax_marg_y = fig.add_subplot(gs[1:, -1])  # Right marginal plot

    # Add an independent axis for the colorbar
    cbar_ax = fig.add_axes([
        left_margin + grid_width + spacing,  # Left position of colorbar
        bottom_margin,    # Bottom position of colorbar
        colorbar_width,   # Width of colorbar
        grid_height*0.75  # Height of colorbar
    ])
    
    ax_joint.tick_params(bottom=True, top=True, right=True, left=True, which='major')
    ax_joint.tick_params(bottom=True, top=True, right=True, left=True, which='minor')

    # Turn off tick visibility for the measure axis on the marginal plots
    plt.setp(ax_marg_x.get_xticklabels(), visible=False)
    plt.setp(ax_marg_y.get_yticklabels(), visible=False)
    plt.setp(ax_marg_x.get_xticklabels(minor=True), visible=False)
    plt.setp(ax_marg_y.get_yticklabels(minor=True), visible=False)
    plt.setp(ax_marg_x.yaxis.get_majorticklines(), visible=False)
    plt.setp(ax_marg_x.yaxis.get_minorticklines(), visible=False)
    plt.setp(ax_marg_y.xaxis.get_majorticklines(), visible=False)
    plt.setp(ax_marg_y.xaxis.get_minorticklines(), visible=False)
    plt.setp(ax_marg_x.get_yticklabels(), visible=False)
    plt.setp(ax_marg_y.get_xticklabels(), visible=False)
    plt.setp(ax_marg_x.get_yticklabels(minor=True), visible=False)
    plt.setp(ax_marg_y.get_xticklabels(minor=True), visible=False)
    ax_marg_x.yaxis.grid(False)
    ax_marg_y.xaxis.grid(False)
    
    # Plot marginal age likelihood
    ax_marg_x.plot(log_age_dummy, np.sum(L, axis=1), color=color_likelihood, linestyle='-', marker='o')
    ax_marg_x.set_xlim(log_age_dummy.min(), log_age_dummy.max())
    ax_marg_x.axvline(best_age, color=color_bestfit, linestyle='-')
    ax_marg_x.axvline(age_unc[0], color=color_bestfit, linestyle='--')
    ax_marg_x.axvline(age_unc[1], color=color_bestfit, linestyle='--')
    ax_marg_x.set_ylabel('Likelihood')

    # Plot marginal mass likelihood
    ax_marg_y.plot(np.sum(L, axis=0), log_masses_dummy, color=color_likelihood, linestyle='-', marker='o')
    ax_marg_y.set_ylim(log_masses_dummy.min(), log_masses_dummy.max())
    ax_marg_y.axhline(best_mass, color=color_bestfit, linestyle='-')
    ax_marg_y.axhline(mass_unc[0], color=color_bestfit, linestyle='--')
    ax_marg_y.axhline(mass_unc[1], color=color_bestfit, linestyle='--')
    ax_marg_y.set_xlabel('Likelihood')

    # Prepare data for the joint likelihood plot
    data = copy.deepcopy(L)
    # data[np.isnan(data)] = 1e-99
    # data[data == np.inf] = 1e-99
    data[~np.isfinite(data)] = 1e-99
    data = data/np.nanmax(data)
    data[data <= 0.0] = 1e-99
    data = np.log10(data)

    # Joint plot of likelihood (log-scale)
    im = ax_joint.imshow(data.T, extent=[log_age_dummy.min(), log_age_dummy.max(), 
                                         log_masses_dummy.min(), log_masses_dummy.max()],
                         origin='lower', aspect='auto', cmap=cmap_likelihood, vmin=-2.0)
    
    # Add colorbar for the likelihood
    # cb = plt.colorbar(im, ax=[ax_joint, ax_marg_y], location='right', pad=0.02)
    cb = fig.colorbar(im, cax=cbar_ax)
    cb.set_label(r'$\log_{10}{\rm Likelihood}$', labelpad=15, y=0.5, rotation=270., fontsize=12)

    # Mark the best-fit point on the joint plot
    ax_joint.scatter([best_age], [best_mass], color=color_bestfit, label='Best Fit')

    # Mark uncertainties on joint plot
    ax_joint.axvline(age_unc[0], color=color_bestfit, linestyle='--')
    ax_joint.axvline(age_unc[1], color=color_bestfit, linestyle='--')
    ax_joint.axhline(mass_unc[0], color=color_bestfit, linestyle='--')
    ax_joint.axhline(mass_unc[1], color=color_bestfit, linestyle='--')
    
    ax_joint.set_xlabel('log(age)')
    ax_joint.set_ylabel('log(mass)')
    
    # Add legend and title
    # ax_joint.legend(loc='lower left', bbox_to_anchor=(1.10,1.20), frameon=False)
    ax_joint.annotate(f'{source}'+'\nBest Fit:\nage = %.2e [yrs]\nmass = %.2f[ms]'%(10**best_age, 10**best_mass), xy=(1.02, 1.02), xycoords='axes fraction', va='bottom', ha='left')
    # fig.suptitle(f'{source}')

    # Save the figure if needed
    if save_fig:
        if not os.path.exists(fig_save_dir):
            os.makedirs(fig_save_dir)
        if customized_fig_name == '':
            fig_file = os.path.join(fig_save_dir, f'lfunc_age_mass_{source}.png')
        else: fig_file = customized_fig_name
        plt.savefig(fig_file, dpi=300, bbox_inches='tight', pad_inches=0.1)

    plt.show()
    
    return 1


def plot_hr_diagram(isochrone, df_prop=None, ax_set=None,
                    ages_to_plot=None, masses_to_plot=None, 
                    age_positions=None, mass_positions=None, 
                    age_rotation=None, mass_rotation=None, 
                    age_xycoords='data', mass_xycoords='data',
                    color_stars='C0', color_zams='magenta',
                    color_masses='darkred', color_ages='grey',
                    color_masses_text='', color_ages_text='',
                    linestyle_zams='-.',
                    linestyle_masses='-', linestyle_ages='--',
                    xlim_set = None, ylim_set = None,
                    no_uncertainties = False,
                    zams_curve = True,
                    bool_mass_annotate=True, 
                    bool_age_annotate=True,
                    bool_labels=True,
                    teff_range=None,
                    annotate_unit_age='all',
                    annotate_unit_mass='none',
                    bare=False):
    """
    Plots the Hertzsprung–Russell diagram with the stars from df_prop and isochrones from the Isochrone class.
    Allows for custom selection of ages and masses to plot, with the option to manually set annotations
    for ages and masses (positions and rotations).

    Args:
    
        isochrone: [Isochrone]
            An instance of the Isochrone class containing the evolutionary tracks with attributes:
            log_age, masses, logtlogl (2D array for Teff and L/Lo).
        df_prop: [pd.DataFrame, optional]
            DataFrame containing the stellar properties with columns:
            ['Source', 'Teff[K]', 'e_Teff[K]', 'Luminosity[Lsun]', 'e_Luminosity[Lsun]'].
            If None, no scatter points are plotted.
        ax_set: [axes, optional] Default is None
            If not None, the ax_set is the ax for the plot
        ages_to_plot: [list, optional]
            List of ages in years to plot as isochrones (default: [0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6, 30.0e6, 100.0e6]).
        masses_to_plot: [list, optional]
            List of masses in solar masses to plot as mass tracks (default: [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]).
        age_positions: [list of tuples, optional]
            List of (x, y) positions for age annotations. Default is automatic placement.
        mass_positions: [list of tuples, optional]
            List of (x, y) positions for mass annotations. Default is automatic placement.
        age_rotation: [list, optional]
            List of rotation angles (degrees) for the age annotations. Default is 0 for all.
        mass_rotation: [list, optional]
            List of rotation angles (degrees) for the mass annotations. Default is 0 for all.
        age_xycoords: [str, optional]
            The xycoords for the age annotate. Default is 'data'. Refer to plt.annotate for details on this arg
        mass_xycoords: [str, optional]
            The xycoords for the mass annotate. Default is 'data'. Refer to plt.annotate for details on this arg
        color_stars: [str, optional]
            The colors for the stars, default is the default color 'C0' in Python.
        color_zams: [str, optional]
            The color for the zams line, default is 'magenta'.
        color_masses: [str, optional]
            The color for evolutionary tracks for each mass, default is 'darkred'
        color_masses_text: [str, optional]
            The color for texts for evolutionary tracks for each mass, default is the same as color_masses
        color_ages: [str, optional]
            The color for isochrones for ages, default is 'grey'
        color_ages_text: [str, optional]
            The color for the texts for isochrones for ages, default is 'black'
        linestyle_zams: [str, optional]
            The linestyle for zams, default is '-.' (solid dashed lines)
        linestyle_masses: [str, optional]
            The linestyle for evolutionary tracks for each mass, default is '-' (solid lines)
        linestyle_ages: [str, optional]
            The linestyle for isochrones for ages, default is '--' (dashed lines)
        xlim_set: [list, optional]
            The xlim from left to right [xlim_left, xlim_right]; default is None, so the code set it automatically
        ylim_set: [list, optional]
            The ylim from bottom to top [ylim_bottom, ylim_top]; default is None, so the code set it automatically
        no_uncertainties: [bool, optional]
            Whether to assume no uncertainties in Teff and Luminosity (default: False).
        zams_curve: [bool, optional]
            Whether to plot the curve of zero-age-main-sequence (default it True)
            If True, the evolutionary tracks after ZAMS will not be plotted
        bool_age_annotate: [bool, optional]
            If true, add the annotate for ages (isochrones)
        bool_mass_annotate: [bool, optional]
            If true, add the annotate for mass (tracks)
        bool_labels: [bool, optional]
            If true, add the labels as legend
        teff_range: [None or np.array(), optional]
            e.g., teff_range = np.array([3000, 3900])
            If set to an array, the plotted isochrone will only cover from selected teff_range
        annotate_unit_age: [array, optional]
            if 'simple' plot only the unit for one time
            if 'all' plot unit on all annotates
            if 'none' do not plot the unit
        annotate_unit_mass: [array, optional]
            if 'simple' plot only the unit for one time
            if 'all' plot unit on all annotates
            if 'none' do not plot the unit
        bare: [bool, optional]
            If true, just plot the scatters from the DataFrame, and the isochromes, but do not add the annotates, legend, nor the labels.
    """
    
    # Default values for ages and masses if not provided
    if ages_to_plot is None:
        ages_to_plot = [0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 30.0e6, 100.0e6]  # in years
    ages_to_plot = np.log10(ages_to_plot)  # convert to log scale for plotting

    if masses_to_plot is None:
        masses_to_plot = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # solar masses

    # Set auto positions if not provided
    if age_positions is None:
        age_positions = ['auto'] * len(ages_to_plot)
    if mass_positions is None:
        mass_positions = ['auto'] * len(masses_to_plot)
    
    # Set default rotations if not provided
    if age_rotation is None:
        age_rotation = [0] * len(ages_to_plot)
    if mass_rotation is None:
        mass_rotation = [0] * len(masses_to_plot)
        
    # set the default color for mass and age texts
    if color_masses_text == '':
        color_masses_text = color_masses
    if color_ages_text == '':
        color_ages_text = 'k'

    # If df_prop is provided, extract values
    if df_prop is not None and not df_prop.empty:
        teff = df_prop['Teff[K]'].values
        luminosity = df_prop['Luminosity[Lsun]'].values
        if no_uncertainties:
            teff_err = luminosity_err = None
        else:
            teff_err = df_prop['e_Teff[K]'].values
            luminosity_err = df_prop['e_Luminosity[Lsun]'].values
    else:
        teff = teff_err = luminosity = luminosity_err = None

    # Plot HR diagram
    if ax_set == None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        ax = ax_set

    # Plot stars with error bars if df_prop is not None or empty
    if teff is not None and luminosity is not None:
        if teff_err is not None and luminosity_err is not None:
            if bool_labels: label_t='stars'
            else: label_t = None
            ax.errorbar(teff, luminosity, xerr=teff_err, yerr=luminosity_err, fmt='o', color=color_stars, label=label_t, alpha=0.7)
        else:
            ax.scatter(teff, luminosity, color=color_stars)
        
    if zams_curve:
        # find the ZAMS
        teff_zams, lum_zams, mask_pms = utils.find_zams_curve(isochrone)
        if teff_range is not None:
            mask_teff_limit = np.logical_and(teff_zams >= np.nanmin(teff_range), teff_zams <= np.nanmax(teff_range))
            teff_zams = teff_zams[mask_teff_limit]
            lum_zams  = lum_zams[mask_teff_limit]
        
        # Plot ZAMS curve
        if bool_labels: label_t='ZAMS'
        else: label_t = None
        ax.plot(teff_zams, lum_zams, color=color_zams, linestyle=linestyle_zams, label=label_t)    

    # Convert isochrone logtlogl data to Teff and L/Lo
    teff_iso = 10**isochrone.logtlogl[:, :, 0]  # Teff
    lum_iso = 10**isochrone.logtlogl[:, :, 1]   # L/Lo

    # First, set the limits based on the data (df_prop) or isochrones
    if xlim_set == None:
        if teff is not None:
            xlim = [np.nanmax(teff) + 100, np.nanmin(teff) - 100]
        else:
            xlim = [np.nanmax(teff_iso), np.nanmin(teff_iso)]
    else: xlim = xlim_set
    if ylim_set == None:
        if luminosity is not None:
            ylim = [np.nanmin(luminosity) * 0.3, np.nanmax(luminosity) * 3.0]
        else:
            ylim = [np.nanmin(lum_iso), np.nanmax(lum_iso)]
    else: ylim = ylim_set

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Plot constant age lines and annotate them at the left (max Teff)
    for i, age in enumerate(ages_to_plot):
        if age < np.nanmin(isochrone.log_age):
            print(f'{10**age/1e6:.2f} Myrs'+' is skipped because it is smaller than the grid min mass of'+' %.2f Myrs'%(10**np.nanmin(isochrone.log_age)/1e6))
            continue
        elif age > np.nanmax(isochrone.log_age):
            print(f'{10**age/1e6:.2f} Myrs'+' is skipped because it is larger than the grid max mass of'+' %.2f Myrs'%(10**np.nanmax(isochrone.log_age)/1e6))
            continue
        
        if i == 0 and bool_labels:
            label_t = 'isochrones' # f'{10**age/1e6:.1f} Myr'
        else:
            label_t = None
        
        idx_age = np.nanargmin(np.abs(isochrone.log_age - age))  # Find closest age
        if zams_curve:
            teff_filtered = teff_iso[idx_age, :][mask_pms[idx_age, :]]
            lum_filtered = lum_iso[idx_age, :][mask_pms[idx_age, :]]

            if teff_range is not None:
                mask_teff_limit = np.logical_and(teff_filtered >= np.nanmin(teff_range), teff_filtered <= np.nanmax(teff_range))
                teff_filtered = teff_filtered[mask_teff_limit]
                lum_filtered  = lum_filtered[mask_teff_limit]
            # Plot the pre-main-sequence part of the isochrone
            ax.plot(teff_filtered, lum_filtered, linestyle_ages, label=label_t, color=color_ages)
        else:
            ax.plot(teff_iso[idx_age, :], lum_iso[idx_age, :], linestyle_ages, label=label_t, color=color_ages)
        
        if not bare:
            if bool_age_annotate:
                if age_positions[i] == 'auto': 
                    # Get automatic annotation position
                    max_teff = np.nanmax(teff_iso[idx_age, :])
                    x_point = np.nanmin([xlim[0], max_teff])
                    idx_max_x_point = np.nanargmin(np.abs(teff_iso[idx_age, :] - x_point))
                    y_point = lum_iso[idx_age, idx_max_x_point] * 0.9
                    age_position = (x_point, y_point)
                else:
                    age_position = age_positions[i]

                if 10**age/1e6 < 1.0:
                    annotate_t = f'{10**age/1e6:.1f}' # Myr
                elif 10**age/1e6 <= 1000:
                    annotate_t = f'{10**age/1e6:.0f}'
                else:
                    annotate_t = f'{10**age/1e6:.0e}'
                if annotate_unit_age == 'simple' and i == int(len(ages_to_plot)-1):
                    annotate_t = annotate_t + ' Myr'
                elif annotate_unit_age == 'all':
                    annotate_t = annotate_t + ' Myr'
                
                # Annotate with custom or default rotation
                ax.annotate(annotate_t, 
                            xy=age_position,  # Place based on automatic or provided position
                            xycoords=age_xycoords,
                            ha='left', va='top', fontsize=12, color=color_ages_text, 
                            rotation=age_rotation[i])
        
    # Plot constant mass lines and annotate them at the top (max Luminosity)
    for i, mass in enumerate(masses_to_plot):
        if mass < np.nanmin(isochrone.masses):
            print(f'{mass:.2f} Msun is skipped because it is smaller than the grid min mass of'+' %.2f Msun'%(np.nanmin(isochrone.masses)))
            continue
        elif mass > np.nanmax(isochrone.masses):
            print(f'{mass:.2f} Msun is skipped because it is larger than the grid max mass of'+' %.2f Msun'%(np.nanmax(isochrone.masses)))
            continue
        
        if i == 0 and bool_labels:
            label_t = 'tracks' # f'{mass:.1f} Msun'
        else:
            label_t = None
        
        idx_mass = np.nanargmin(np.abs(isochrone.masses - mass))  # Find closest mass
        if zams_curve:
            teff_filtered = teff_iso[:, idx_mass][mask_pms[:, idx_mass]]
            lum_filtered = lum_iso[:, idx_mass][mask_pms[:, idx_mass]]
            ax.plot(teff_filtered, lum_filtered, linestyle_masses, label=label_t, color=color_masses)
        else:
            ax.plot(teff_iso[:, idx_mass], lum_iso[:, idx_mass], linestyle_masses, label=label_t, color=color_masses)

        if not bare:
            if bool_mass_annotate:
                if mass_positions[i] == 'auto':
                    # Get automatic annotation position
                    x_point = teff_iso[np.nanargmax(lum_iso[:, idx_mass]), idx_mass]
                    max_lum = np.nanmax(lum_iso[:, idx_mass])
                    y_point = np.nanmin([max_lum, ylim[1]])
                    mass_position = (x_point, y_point)
                else:
                    mass_position = mass_positions[i]

                if mass >= 0.1:
                    annotate_t = f'{mass:.1f}' #  Msun
                elif mass >= 0.01:
                    annotate_t = f'{mass:.2f}'
                else:
                    annotate_t = f'{mass:.1e}'
                if annotate_unit_mass.lower() == 'simple' and i == 0:
                    annotate_t = annotate_t + ' Msun'
                elif annotate_unit_mass.lower() == 'all':
                    annotate_t = annotate_t + ' Msun'
                else:
                    annotate_t = annotate_t
                
                # Annotate with custom or default rotation
                ax.annotate(annotate_t, 
                            xy=mass_position,  # Place based on automatic or provided position
                            xycoords=mass_xycoords,
                            ha='center', va='bottom', fontsize=12, color=color_masses_text,
                            rotation=mass_rotation[i])
    
    ax.set_yscale('log')  # Luminosity is plotted on a logarithmic scale
    
    if not bare:
        # Labeling the plot
        ax.set_xlabel(r'$T_{\rm eff}$ [K]', fontsize=14)
        ax.set_ylabel(r'$L_\star$ [$L_\odot$]', fontsize=14)
        # ax.set_title('Hertzsprung-Russell Diagram')
        # ax.invert_xaxis()  # HR diagram has decreasing Teff from left to right

        # Legend
        ax.legend(loc='upper left', bbox_to_anchor=[1.0, 1.0])

    # Show plot
    if ax_set == None:
        plt.show()

    return 1


def plot_likelihood_1d(log_masses_dummy, likelihood, best_log_mass, lower_mass, upper_mass, source=None):
    """
    Plots the likelihood function for stellar mass.

    Args:
    
        log_masses_dummy: [array]
            Array of log10(mass) values from the evolutionary track.
        likelihood: [array]
            Likelihood function evaluated for each mass point.
        best_log_mass: [float]
            The best-fit log10 mass.
        lower_mass: [float]
            The lower bound of the uncertainty in log10 mass.
        upper_mass: [float]
            The upper bound of the uncertainty in log10 mass.
        source: [str, optional]
            The source name to include in the plot title. Default is None.
    """
    
    likelihood[likelihood <= 1e-98] = np.nan
    
    fig = plt.figure(figsize=(8, 6))
    ax  = fig.add_subplot(1,1,1)
    ax.plot(10**log_masses_dummy, likelihood, label='Likelihood', lw=2)
    ax.axvline(x=10**best_log_mass, color='r', linestyle='--', label=f'Best Mass: {10**best_log_mass:.2f} $M_\\odot$')
    ax.axvline(x=10**lower_mass, color='k', linestyle=':', label=f'Lower Bound: {10**lower_mass:.2f} $M_\\odot$')
    ax.axvline(x=10**upper_mass, color='k', linestyle=':', label=f'Upper Bound: {10**upper_mass:.2f} $M_\\odot$')

    ax.set_xlabel(r'Stellar Mass [$M_\odot$]', fontsize=14)
    ax.set_ylabel('Likelihood', fontsize=14)
    # ax.set_xscale('log')
    ax.set_yscale('log')
    ylim_t = ax.get_ylim()
    ax.set_ylim(bottom=np.nanmax(ylim_t)*1e-15)
    
    if source:
        ax.set_title(f'Likelihood for Stellar Mass ({source})', fontsize=16)
    else:
        ax.set_title('Likelihood for Stellar Mass', fontsize=16)

    ax.legend(loc='lower center')
    ax.grid(True)
    plt.show()
    
    return 1


def simple_plot_hr_diagram_feiden_n_baraffe(df_prop=None, ax_set=None):
    """
    Plots HR diagrams using isochrone tracks from two different models ('Feiden2016' and 'Baraffe2015').

    Args:
        df_prop: [pd.DataFrame, optional]
            DataFrame containing the stellar properties with columns:
            ['Source', 'Teff[K]', 'e_Teff[K]', 'Luminosity[Lsun]', 'e_Luminosity[Lsun]'].
            If None, no scatter points are plotted.
        ax_set: [axes, optional] Default is None
            If not None, the ax_set is the ax for the plot
    """
    # Define plot limits and the ages and masses to plot
    xlim_set = [5200, 2500]
    ylim_set = [1e-3, 30]

    ages_to_plot_t   = [0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6, 30.0e6, 100.0e6]
    masses_to_plot_f = [0.6, 0.8, 1.0, 1.4]
    masses_to_plot_b = [0.05, 0.1, 0.2, 0.3, 0.4]

    # Create the figure and axes
    if ax_set == None:
        fig, axes = plt.subplots(figsize=(8, 6))
    else:
        axes = ax_set
    
    # Plot the 'Feiden2016' isochrones
    iso = isochrone.Isochrone()
    iso.set_tracks('Feiden2016')

    age_positions_set = [
        (5200, 25),
        (5200, 13),
        (5200, 7),
        (5200, 4.5),
        (5200, 3),
        (5200, 1.2),
        (5200, 0.55),
        (5200, 0.35),
    ]
    # For the first 4 ages, use a rotation of -22, then -13 for the rest
    age_rotation_t = [-22] * 4 + [-13] * (len(ages_to_plot_t) - 4)
    # For masses, first mass gets -10, the rest get -22
    mass_ration_set = [-10] * 1 + [-22] * (len(masses_to_plot_f) - 1)

    plot_hr_diagram(
        iso, df_prop, ax_set=axes,
        xlim_set=xlim_set, ylim_set=ylim_set,
        ages_to_plot=ages_to_plot_t,
        masses_to_plot=masses_to_plot_f,
        teff_range=np.array([xlim_set[0], 3700]),
        age_positions=age_positions_set,
        age_rotation=age_rotation_t,
        mass_rotation=mass_ration_set
    )

    # Plot the 'Baraffe2015' isochrones
    iso = isochrone.Isochrone()
    iso.set_tracks('Baraffe2015')
    mass_ration_set = [-45] * 1 + [-22] * (len(masses_to_plot_b) - 1)

    plot_hr_diagram(
        iso, df_prop, ax_set=axes,
        xlim_set=xlim_set, ylim_set=ylim_set,
        ages_to_plot=ages_to_plot_t,
        masses_to_plot=masses_to_plot_b,
        teff_range=np.array([xlim_set[1], 4200]),
        bool_age_annotate=False,
        bool_labels=False,
        mass_rotation=mass_ration_set
    )

    # Annotate and finalize the plot
    axes.annotate('Feiden+Baraffe', xy=(0.95, 0.95), xycoords='axes fraction',
                  ha='right', va='top', fontsize=20)
    axes.legend(loc='lower left')
    axes.set_xlim(xlim_set)
    axes.set_ylim(ylim_set)
    
    return 1
    

def plot_comparison(log_age_idl, masses_idl, logtlogl_interp_py, logtlogl_idl, logtlogl_diff, logtlogl_diff_norm, gridnames=['Python', 'IDL']):
    """
    Plots the Python grid (interpolated onto IDL grid), IDL grid, and their differences for both Teff and L/Lo.

    Args:
        
        log_age_idl: [array]
            Array of log(age) values from the IDL grid.
        masses_idl: [array]
            Array of mass values from the IDL grid.
        logtlogl_interp_py: [array]
            Python-generated logtlogl data (Teff and L/Lo) interpolated onto the IDL grid.
        logtlogl_idl: [array]
            IDL-generated logtlogl data (Teff and L/Lo).
        logtlogl_diff: [array]
            Difference between interpolated Python and IDL logtlogl data.
        logtlogl_diff_norm: [array]
            Normalized difference between interpolated Python and IDL logtlogl data.
        gridnames: [list of strings, optional]
            The names of the grid names, default is Python and IDL
    """
    
    fig, axs = plt.subplots(4, 2, figsize=(12, 16), constrained_layout=True)

    # Set the extent of the grid to match the IDL grid
    extent = [masses_idl.min(), masses_idl.max(), log_age_idl.max(), log_age_idl.min()]

    # Teff Plot (Interpolated Python Grid)
    im1 = axs[0, 0].imshow(logtlogl_interp_py[:, :, 0], aspect='auto', extent=extent)
    axs[0, 0].set_title('%s Grid (Interpolated to IDL): Teff'%(gridnames[0]))
    axs[0, 0].set_xlabel(r'Mass [M$_\odot$]')
    axs[0, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im1, ax=axs[0, 0])

    # Teff Plot (IDL Grid)
    im2 = axs[0, 1].imshow(logtlogl_idl[:, :, 0], aspect='auto', extent=extent)
    axs[0, 1].set_title('%s Grid: Teff'%(gridnames[1]))
    axs[0, 1].set_xlabel(r'Mass [M$_\odot$]')
    axs[0, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im2, ax=axs[0, 1])

    # Teff Difference Plot
    im3 = axs[1, 0].imshow(logtlogl_diff[:, :, 0], aspect='auto', cmap='coolwarm', extent=extent)
    axs[1, 0].set_title('Difference: Teff (%s - %s)'%(gridnames[0], gridnames[1]))
    axs[1, 0].set_xlabel(r'Mass [M$_\odot$]')
    axs[1, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im3, ax=axs[1, 0])

    # Teff Normalized Difference Plot
    im4 = axs[1, 1].imshow(logtlogl_diff_norm[:, :, 0], aspect='auto', cmap='coolwarm', extent=extent)
    axs[1, 1].set_title('Normalized Difference: Teff')
    axs[1, 1].set_xlabel(r'Mass [M$_\odot$]')
    axs[1, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im4, ax=axs[1, 1])

    # L/Lo Plot (Interpolated Python Grid)
    im5 = axs[2, 0].imshow(logtlogl_interp_py[:, :, 1], aspect='auto', extent=extent)
    axs[2, 0].set_title('%s Grid (Interpolated to IDL): L/Lo'%(gridnames[0]))
    axs[2, 0].set_xlabel(r'Mass [M$_\odot$]')
    axs[2, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im5, ax=axs[2, 0])

    # L/Lo Plot (IDL Grid)
    im6 = axs[2, 1].imshow(logtlogl_idl[:, :, 1], aspect='auto', extent=extent)
    axs[2, 1].set_title('%s Grid: L/Lo'%(gridnames[1]))
    axs[2, 1].set_xlabel(r'Mass [M$_\odot$]')
    axs[2, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im6, ax=axs[2, 1])

    # L/Lo Difference Plot
    im7 = axs[3, 0].imshow(logtlogl_diff[:, :, 1], aspect='auto', cmap='coolwarm', extent=extent)
    axs[3, 0].set_title('Difference: L/Lo (%s - %s)'%(gridnames[0], gridnames[1]))
    axs[3, 0].set_xlabel(r'Mass [M$_\odot$]')
    axs[3, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im7, ax=axs[3, 0])

    # L/Lo Normalized Difference Plot
    im8 = axs[3, 1].imshow(logtlogl_diff_norm[:, :, 1], aspect='auto', cmap='coolwarm', extent=extent)
    axs[3, 1].set_title('Normalized Difference: L/Lo')
    axs[3, 1].set_xlabel(r'Mass [M$_\odot$]')
    axs[3, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im8, ax=axs[3, 1])

    plt.show()
    
    return 1
