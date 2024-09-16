import matplotlib.pyplot as plt
import numpy as np
import copy
import os

def plot_bayesian_results(log_age_dummy, log_masses_dummy, L, best_age, best_mass, age_unc, mass_unc, source=None, save_fig=False, fig_save_dir='figure', customized_fig_name=''):
    """
    Plots the likelihood distributions and the best-fit age and mass.

    Args:
    ------------
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
        
    Output:
    ------------
    a formatted figure (or save to the fig_save_dir)
    
    Returns:
    ------------
    1 if the code could be ran through
    """
    
    fig = plt.figure(figsize=(6, 5), dpi=300)
    ratio = 3
    gs = plt.GridSpec(ratio+1, ratio+1)
    
    ax_joint = fig.add_subplot(gs[1:, :-1])
    ax_marg_x = fig.add_subplot(gs[0, :-1], sharex=ax_joint)
    ax_marg_y = fig.add_subplot(gs[1:, -1], sharey=ax_joint)
    
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
    ax_marg_x.plot(log_age_dummy, np.sum(L, axis=1), color='blue', linestyle='-', marker='o')
    ax_marg_x.axvline(best_age, color='red', linestyle='-')
    ax_marg_x.axvline(age_unc[0], color='red', linestyle='--')
    ax_marg_x.axvline(age_unc[1], color='red', linestyle='--')
    ax_marg_x.set_ylabel('Likelihood')

    # Plot marginal mass likelihood
    ax_marg_y.plot(np.sum(L, axis=0), log_masses_dummy, color='blue', linestyle='-', marker='o')
    ax_marg_y.axhline(best_mass, color='red', linestyle='-')
    ax_marg_y.axhline(mass_unc[0], color='red', linestyle='--')
    ax_marg_y.axhline(mass_unc[1], color='red', linestyle='--')
    ax_marg_y.set_xlabel('Likelihood')

    # Prepare data for the joint likelihood plot
    data = copy.deepcopy(L)
    data[np.isnan(data)] = 1e-99
    data[data == np.inf] = 1e-99
    data[data < 0.0] = 1e-99
    data = np.log10(data)

    # Joint plot of likelihood (log-scale)
    im = ax_joint.imshow(data.T, extent=[log_age_dummy.min(), log_age_dummy.max(), 
                                         log_masses_dummy.min(), log_masses_dummy.max()],
                         origin='lower', aspect='auto', cmap='viridis', vmin=-3)
    
    # Add colorbar for the likelihood
    cb = plt.colorbar(im)
    cb.set_label(r'$\log_{10}{\rm Likelihood}$', labelpad=15, y=0.5, rotation=270., fontsize=12)

    # Mark the best-fit point on the joint plot
    ax_joint.scatter([best_age], [best_mass], color='red', label='Best Fit')

    # Mark uncertainties on joint plot
    ax_joint.axvline(age_unc[0], color='red', linestyle='--')
    ax_joint.axvline(age_unc[1], color='red', linestyle='--')
    ax_joint.axhline(mass_unc[0], color='red', linestyle='--')
    ax_joint.axhline(mass_unc[1], color='red', linestyle='--')
    
    ax_joint.set_xlabel('log(age)')
    ax_joint.set_ylabel('log(mass)')
    
    # Add legend and title
    ax_joint.legend(loc='lower left', bbox_to_anchor=(0.95,1.15))
    ax_joint.annotate('\nage = %.2e [yrs]\nmass = %.2f[ms]'%(10**best_age, 10**best_mass), xy=(1.03, 1.25), xycoords='axes fraction', va='top', ha='left')
    fig.suptitle(f'{source}')

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
                    age_positions=None, mass_rotation=None, 
                    age_rotation=None, mass_positions=None,
                    age_xycoords='data', mass_xycoords='data',
                    bare=False):
    """
    Plots the Hertzsprung–Russell diagram with the stars from df_prop and isochrones from the Isochrone class.
    Allows for custom selection of ages and masses to plot, with the option to manually set annotations
    for ages and masses (positions and rotations).

    Args:
    ------------
    isochrone: [Isochrone]
        An instance of the Isochrone class containing the evolutionary tracks with attributes:
        log_age, masses, logtlogl (2D array for Teff and L/Lo).
    df_prop: [pd.DataFrame, optional]
        DataFrame containing the stellar properties with columns:
        ['Source', 'Teff', 'e_Teff', 'Luminosity', 'e_Luminosity'].
        If None, no scatter points are plotted.
    ax_set: [axes, optional] Default is None
        If not None, the ax_set is the ax for the plot
    ages_to_plot: [list, optional]
        List of ages in years to plot as isochrones (default: [0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6, 50.0e6]).
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
        the xycoords for the age annotate. Default is 'data'. Refer to plt.annotate for details on this arg
    mass_xycoords: [str, optional]
        the xycoords for the mass annotate. Default is 'data'. Refer to plt.annotate for details on this arg
    bare: [bool, optional]
        If true, just plot the scatters from the DataFrame, and the isochromes, but do not add the annotates, legend, nor the labels.
    """
    
    # Default values for ages and masses if not provided
    if ages_to_plot is None:
        ages_to_plot = [0.5e6, 1.0e6, 2.0e6, 3.0e6, 5.0e6, 10.0e6, 50.0e6]  # in years
    ages_to_plot = np.log10(ages_to_plot)  # convert to log scale for plotting

    if masses_to_plot is None:
        masses_to_plot = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # solar masses

    # Set default rotations if not provided
    if age_rotation is None:
        age_rotation = [0] * len(ages_to_plot)
    if mass_rotation is None:
        mass_rotation = [0] * len(masses_to_plot)

    # If df_prop is provided, extract values
    if df_prop is not None and not df_prop.empty:
        teff = df_prop['Teff'].values
        teff_err = df_prop['e_Teff'].values
        luminosity = df_prop['Luminosity'].values
        luminosity_err = df_prop['e_Luminosity'].values
    else:
        teff = teff_err = luminosity = luminosity_err = None

    # Plot HR diagram
    if ax_set == None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        ax = ax_set

    # Plot stars with error bars if df_prop is not None or empty
    if teff is not None and luminosity is not None:
        ax.errorbar(teff, luminosity, xerr=teff_err, yerr=luminosity_err, fmt='o', color='blue', label='Stars', alpha=0.7)

    # Convert isochrone logtlogl data to Teff and L/Lo
    teff_iso = 10**isochrone.logtlogl[:, :, 0]  # Teff
    lum_iso = 10**isochrone.logtlogl[:, :, 1]   # L/Lo

    # First, set the limits based on the data (df_prop) or isochrones
    if teff is not None and luminosity is not None:
        xlim = [np.nanmax(teff) + 100, np.nanmin(teff) - 100]
        ylim = [np.nanmin(luminosity) * 0.3, np.nanmax(luminosity) * 3.0]
    else:
        xlim = [np.nanmax(teff_iso), np.nanmin(teff_iso)]
        ylim = [np.nanmin(lum_iso), np.nanmax(lum_iso)]

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Plot constant age lines and annotate them at the left (max Teff)
    for i, age in enumerate(ages_to_plot):
        idx_age = np.nanargmin(np.abs(isochrone.log_age - age))  # Find closest age
        ax.plot(teff_iso[idx_age, :], lum_iso[idx_age, :], '--', label=f'{10**age/1e6:.1f} Myr', color='grey')
        
        if not bare:
            # Get automatic annotation position
            if age_positions is None:
                max_teff = np.nanmax(teff_iso[idx_age, :])
                x_point = np.nanmin([xlim[0], max_teff])
                idx_max_x_point = np.nanargmin(np.abs(teff_iso[idx_age, :] - x_point))
                y_point = lum_iso[idx_age, idx_max_x_point] * 0.9
                age_position = (x_point, y_point)
            else:
                age_position = age_positions[i]

            # Annotate with custom or default rotation
            ax.annotate(f'{10**age/1e6:.1f} Myr', 
                        xy=age_position,  # Place based on automatic or provided position
                        xycoords=age_xycoords,
                        ha='left', va='top', fontsize=12, color='black', 
                        rotation=age_rotation[i])
        
    # Plot constant mass lines and annotate them at the top (max Luminosity)
    for i, mass in enumerate(masses_to_plot):
        idx_mass = np.nanargmin(np.abs(isochrone.masses - mass))  # Find closest mass
        ax.plot(teff_iso[:, idx_mass], lum_iso[:, idx_mass], '-', label=f'{mass:.1f} Msun', color='darkred')

        if not bare:
            # Get automatic annotation position
            if mass_positions is None:
                x_point = teff_iso[np.nanargmax(lum_iso[:, idx_mass]), idx_mass]
                max_lum = np.nanmax(lum_iso[:, idx_mass])
                y_point = np.nanmin([max_lum, ylim[1]])
                mass_position = (x_point, y_point)
            else:
                mass_position = mass_positions[i]

            # Annotate with custom or default rotation
            ax.annotate(f'{mass:.1f} Msun', 
                        xy=mass_position,  # Place based on automatic or provided position
                        xycoords=mass_xycoords,
                        ha='center', va='bottom', fontsize=12, color='darkred',
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
    ------------
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
    
    plt.figure(figsize=(8, 6))
    plt.plot(10**log_masses_dummy, likelihood, label='Likelihood', lw=2)
    plt.axvline(x=10**best_log_mass, color='r', linestyle='--', label=f'Best Mass: {10**best_log_mass:.2f} $M_\\odot$')
    plt.axvline(x=10**lower_mass, color='k', linestyle=':', label=f'Lower Bound: {10**lower_mass:.2f} $M_\\odot$')
    plt.axvline(x=10**upper_mass, color='k', linestyle=':', label=f'Upper Bound: {10**upper_mass:.2f} $M_\\odot$')

    plt.xlabel(r'Stellar Mass [$M_\odot$]', fontsize=14)
    plt.ylabel('Likelihood', fontsize=14)
    # plt.xscale('log')
    plt.yscale('log')
    
    if source:
        plt.title(f'Likelihood for Stellar Mass ({source})', fontsize=16)
    else:
        plt.title('Likelihood for Stellar Mass', fontsize=16)

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
    
    return 1


def plot_comparison(log_age_idl, masses_idl, logtlogl_interp_py, logtlogl_idl, logtlogl_diff, logtlogl_diff_norm, gridnames=['Python', 'IDL']):
    """
    Plots the Python grid (interpolated onto IDL grid), IDL grid, and their differences for both Teff and L/Lo.

    Args:
    ------------
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
    axs[0, 0].set_xlabel('Mass [M$_\odot$]')
    axs[0, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im1, ax=axs[0, 0])

    # Teff Plot (IDL Grid)
    im2 = axs[0, 1].imshow(logtlogl_idl[:, :, 0], aspect='auto', extent=extent)
    axs[0, 1].set_title('%s Grid: Teff'%(gridnames[1]))
    axs[0, 1].set_xlabel('Mass [M$_\odot$]')
    axs[0, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im2, ax=axs[0, 1])

    # Teff Difference Plot
    im3 = axs[1, 0].imshow(logtlogl_diff[:, :, 0], aspect='auto', cmap='coolwarm', extent=extent)
    axs[1, 0].set_title('Difference: Teff (%s - %s)'%(gridnames[0], gridnames[1]))
    axs[1, 0].set_xlabel('Mass [M$_\odot$]')
    axs[1, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im3, ax=axs[1, 0])

    # Teff Normalized Difference Plot
    im4 = axs[1, 1].imshow(logtlogl_diff_norm[:, :, 0], aspect='auto', cmap='coolwarm', extent=extent)
    axs[1, 1].set_title('Normalized Difference: Teff')
    axs[1, 1].set_xlabel('Mass [M$_\odot$]')
    axs[1, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im4, ax=axs[1, 1])

    # L/Lo Plot (Interpolated Python Grid)
    im5 = axs[2, 0].imshow(logtlogl_interp_py[:, :, 1], aspect='auto', extent=extent)
    axs[2, 0].set_title('%s Grid (Interpolated to IDL): L/Lo'%(gridnames[0]))
    axs[2, 0].set_xlabel('Mass [M$_\odot$]')
    axs[2, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im5, ax=axs[2, 0])

    # L/Lo Plot (IDL Grid)
    im6 = axs[2, 1].imshow(logtlogl_idl[:, :, 1], aspect='auto', extent=extent)
    axs[2, 1].set_title('%s Grid: L/Lo'%(gridnames[1]))
    axs[2, 1].set_xlabel('Mass [M$_\odot$]')
    axs[2, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im6, ax=axs[2, 1])

    # L/Lo Difference Plot
    im7 = axs[3, 0].imshow(logtlogl_diff[:, :, 1], aspect='auto', cmap='coolwarm', extent=extent)
    axs[3, 0].set_title('Difference: L/Lo (%s - %s)'%(gridnames[0], gridnames[1]))
    axs[3, 0].set_xlabel('Mass [M$_\odot$]')
    axs[3, 0].set_ylabel('log(Age) [years]')
    fig.colorbar(im7, ax=axs[3, 0])

    # L/Lo Normalized Difference Plot
    im8 = axs[3, 1].imshow(logtlogl_diff_norm[:, :, 1], aspect='auto', cmap='coolwarm', extent=extent)
    axs[3, 1].set_title('Normalized Difference: L/Lo')
    axs[3, 1].set_xlabel('Mass [M$_\odot$]')
    axs[3, 1].set_ylabel('log(Age) [years]')
    fig.colorbar(im8, ax=axs[3, 1])

    plt.show()
