import os
import requests
import tarfile
import zipfile
from tqdm import tqdm
import re
import numpy as np
import scipy.io
from scipy.interpolate import griddata
from ysoisochrone import plotting


def unc_log10(x, err_x):
    """
    Propagates uncertainties from the linear scale to the logarithmic scale (base 10).

    Args:
    ------------
    value: [float]
        The value in linear scale (e.g., Teff, Luminosity, etc.).
    err_x: [float]
        The uncertainty in the linear value.

    Returns:
    ------------
    err_log10_x: [float]
        The propagated uncertainty in the logarithmic scale (base 10).
    """
    ln10 = np.log(10)
    err_log10_x = err_x / (x * ln10)
    return err_log10_x


def unc_linear_from_log(log_value, log_uncertainty):
    """
    Propagates uncertainties from the logarithmic scale (base 10) back to the linear scale.

    Args:
    ------------
    log_value: [float]
        The value in logarithmic scale (e.g., log(Teff), log(L), etc.).
    log_uncertainty: [float]
        The uncertainty in the logarithmic value.

    Returns:
    ------------
    linear_uncertainty: [float]
        The propagated uncertainty in the linear scale.
    """
    # Convert log_value back to linear scale
    linear_value = 10 ** log_value
    # Propagate uncertainty
    return linear_value * np.log(10) * log_uncertainty


def assign_unc_teff(teff_ar, sigma_logT_set=None):
    """
    assign the Teff uncertainties
    
    Args:
    ------------
    teff_ar: [array]
        the array for Teff
    
        
    Returns:
    ------------
    err_teff_ar: [array]
        the array of Teff
    """
    err_teff_ar = np.ones(len(teff_ar)) * np.nan 
    for ii, T_this in enumerate(teff_ar):
        if sigma_logT_set == None:
            sigma_logT = 0.02 if T_this > 3420.0 else 0.01  # Uncertainty for Teff
        else:
            sigma_logT == sigma_logT_set
        err_teff_ar[ii] = unc_linear_from_log(np.log10(T_this), sigma_logT)
    return err_teff_ar
    
    
def assign_unc_lumi(lumi_ar, sigma_logL_set=None):
    """
    assign the luminosity uncertainties
    
    Args:
    ------------
    lumi_ar: [array]
        the array for luminosity
    
        
    Returns:
    ------------
    err_lumi_ar: [array]
        the array of luminosity
    """
    err_lumi_ar = np.ones(len(lumi_ar)) * np.nan
    if sigma_logL_set == None:
        sigma_logL = 0.1
    else:
        sigma_logL = sigma_logL_set
    for ii, L_this in enumerate(lumi_ar):
        err_lumi_ar[ii] = unc_linear_from_log(np.log10(L_this), sigma_logL)
    return err_lumi_ar


def get_likelihood_andrews2013(logtlogl_dummy, c_logT, c_logL, sigma_logT, sigma_logL):
    """
    Calculates the likelihood function lfunc given the input log temperature and luminosity.
    L is the likelihood function see eq. 1 in Andrews2013 (or anyone you would like to set up)
    
    Args:
    ------------
    logtlogl_dummy: [array]
        Array of log(T) and log(L) values for the evolutionary tracks.
    c_logT: [float]
        Logarithm of the stellar effective temperature.
    c_logL: [float]
        Logarithm of the stellar luminosity.
    sigma_logT: [float]
        Uncertainty in log(Teff).
    sigma_logL: [float]
        Uncertainty in log(Luminosity).

    Output:
    ------------
    Returns:
    ------------
    lfunc: [2D array]
        The likelihood function values for each combination of age and mass.
    """
    fT = ((logtlogl_dummy[:, :, 0]) - c_logT)**2 / sigma_logT**2
    fL = ((logtlogl_dummy[:, :, 1]) - c_logL)**2 / sigma_logL**2
    lfunc = 1.0 / (2 * np.pi * sigma_logT * sigma_logL) * np.exp(-0.5 * (fT + fL))
    return lfunc


def download_file_simple(url, save_path):
    """
    Downloads a file from a given URL and saves it to the specified path.

    Args:
    ------------
    url: [str]
        URL of the file to download.
    save_path: [str]
        Local path to save the file.
    """
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded {save_path}")
    else:
        raise ValueError(f"Failed to download file: {url}")

    return 1


def download_file(url, save_path):
    """
    Downloads a file from a given URL and saves it to the specified path with a customizable progress bar.

    Args:
    ------------
    url: [str]
        URL of the file to download.
    save_path: [str]
        Local path to save the file.
    """
    # Get the total size of the file to be downloaded
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))  # Total size in bytes

    if response.status_code == 200:
        # Customize the progress bar display
        with open(save_path, 'wb') as f, tqdm(
            desc=f"Downloading",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            ncols=100,  # Set the width of the progress bar (in characters)
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',  # Customize bar format
        ) as progress_bar:
            # Write the data in chunks, updating the progress bar
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        print(f"\nDownloaded {save_path}")
    else:
        raise ValueError(f"Failed to download file: {url}")
    
    return 1

    
def extract_tarball(tar_file_path, extract_dir):
    """
    Extracts a tarball file into a specified directory.

    Args:
    ------------
    tar_file_path: [str]
        Path to the tarball file.
    extract_dir: [str]
        Directory to extract the tarball contents into.
    """
    with tarfile.open(tar_file_path, "r:gz") as tar:
        tar.extractall(path=extract_dir)
    print(f"Extracted {tar_file_path} into {extract_dir}")


def download_baraffe_tracks(save_dir='isochrones_data'):
    """
    Downloads the Baraffe BHAC15 tracks file and saves it to the specified directory.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the file should be saved. Defaults to 'isochrones_data'.

    Output:
    ------------
    Downloads the file and saves it in the specified directory.
    
    Raises:
    ------------
    ValueError: If the file could not be downloaded.
    """
    
    # URL of the file to download
    url = 'http://perso.ens-lyon.fr/isabelle.baraffe/BHAC15dir/BHAC15_tracks+structure'

    # Create the directory if it doesn't exist
    save_dir_baraffe = os.path.join(save_dir, 'Baraffe2015')
    if not os.path.exists(save_dir_baraffe):
        os.makedirs(save_dir_baraffe)

    # Name of the file to save (you can modify this if needed)
    file_name = os.path.join(save_dir, 'Baraffe2015', 'BHAC15_tracks+structure')

    download_file(url, file_name)

    # try:
    #     print('start downloading the evolutionary tracks from Baraffe et al. (2015)')
    #     # Download the file
    #     response = requests.get(url, stream=True)

    #     # Check if the request was successful
    #     if response.status_code == 200:
    #         # Write the content to a file in chunks
    #         with open(file_name, 'wb') as f:
    #             for chunk in response.iter_content(chunk_size=1024):
    #                 if chunk:
    #                     f.write(chunk)
    #         print(f"File downloaded successfully and saved to {file_name}")
    #         print('If you end up using the Baraffe et al. (2015) tracks, please cite from: https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract')
    #     else:
    #         raise ValueError(f"Failed to download file. Status code: {response.status_code}")
    # except requests.RequestException as e:
    #     raise ValueError(f"An error occurred while downloading the file: {e}")
    
    print('If you end up using the Baraffe et al. (2015) tracks, please cite from: https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract')
    
    return 1


def read_baraffe_file(file_path):
    """
    Reads the original BHAC15 tracks file and parses the mass, age, and logtlogl.

    Args:
    ------------
    file_path: [str]
        Path to the original BHAC15 tracks file.

    Returns:
    ------------
    data_points: [np.array]
        Array of [log_age, mass, teff, luminosity] data points.
    """
    data_points = []

    start_reading = False

    with open(file_path, 'r') as f:
        lines = f.readlines()

        # Iterate over each line
        for line in lines:
            # Start reading after 'END OF NOTE'
            if 'END OF NOTE' in line:
                start_reading = True
                continue

            # Skip lines that start with !, -, or are empty
            if not start_reading or line.startswith('!') or line.startswith('-') or len(line.strip()) == 0:
                continue

            # Split the line into individual values
            parts = line.split()

            if len(parts) >= 12:  # Ensure there are enough columns
                # Parse the columns:
                mass = float(parts[0])        # M/Ms
                log_age = float(parts[1])     # log t (age in years)
                teff = float(parts[2])        # Teff (effective temperature in K)
                luminosity = float(parts[3])  # log L/Ls (log luminosity in solar units)

                data_points.append([mass, log_age, teff, luminosity])

    # Convert lists to numpy arrays for easy manipulation
    data_points = np.array(data_points)

    return data_points


# def download_feiden_tracks(save_dir='isochrones_data'):
#     """
#     Downloads the Feiden tracks file from GitHub and saves it to the specified directory.

#     Args:
#     ------------
#     save_dir: [str, optional]
#         The directory where the file should be saved. Defaults to 'isochrones_data'.

#     Output:
#     ------------
#     Downloads the Feiden tracks as a tarball, saves it, and extracts it in the specified directory.
    
#     Raises:
#     ------------
#     ValueError: If the file could not be downloaded or extracted.
#     """
    
#     # URL of the file to download
#     url = 'https://github.com/gfeiden/MagneticUpperSco/blob/master/models/iso/std/dmestar_isochrones_z%2B0.00_a%2B0.00_phx.tgz?raw=true'

#     # Create the directory if it doesn't exist
#     feiden_dir = os.path.join(save_dir, 'Feiden2016')
#     if not os.path.exists(feiden_dir):
#         os.makedirs(feiden_dir)

#     # Name of the file to save (you can modify this if needed)
#     tar_file_name = os.path.join(feiden_dir, 'dmestar_isochrones_z+0.00_a+0.00_phx.tgz')

#     try:
#         print('Start downloading the Feiden tracks from GitHub...')
#         # Download the file
#         response = requests.get(url, stream=True)

#         # Check if the request was successful
#         if response.status_code == 200:
#             # Write the content to a file in chunks
#             with open(tar_file_name, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=1024):
#                     if chunk:
#                         f.write(chunk)
#             print(f"File downloaded successfully and saved to {tar_file_name}")
#         else:
#             raise ValueError(f"Failed to download file. Status code: {response.status_code}")
        
#         # Extract the tarball file
#         print(f"Extracting the tarball file: {tar_file_name}")
#         with tarfile.open(tar_file_name, "r:gz") as tar:
#             tar.extractall(path=feiden_dir)
#         print(f"File extracted successfully to {feiden_dir}")
#         print("If you use the Feiden tracks, please cite from: https://ui.adsabs.harvard.edu/abs/2016IAUS..314...79F/abstract")
        
#     except requests.RequestException as e:
#         raise ValueError(f"An error occurred while downloading the file: {e}")
#     except (tarfile.TarError, IOError) as e:
#         raise ValueError(f"An error occurred while extracting the tarball file: {e}")

#     return 1


def download_feiden_trk_tracks(save_dir='isochrones_data', download_original_trks=False):
    """
    Downloads (all .trk files and [optional]) the tarball from the specified GitHub folder and saves them to the given directory.
    The tarball is extracted after downloading.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data'.
    download_original_trks: [bool, optional] default = False
        If true, download the original trk files provided on their gibhub page,
        otherwise, only download the tgz file and then untar it

    Output:
    ------------
    Downloads (all .iso files and) the tarball from the GitHub folder, saves them, and extracts the tarball.
    """

    # Create Feiden2016 directory if it doesn't exist
    feiden_dir = os.path.join(save_dir, 'Feiden2016_trk')
    if not os.path.exists(feiden_dir):
        os.makedirs(feiden_dir)

    # Base URL for GitHub raw files
    base_url = 'https://raw.githubusercontent.com/gfeiden/MagneticUpperSco/master/models/trk/std/'
    # URL for the directory on GitHub API
    api_url = 'https://api.github.com/repos/gfeiden/MagneticUpperSco/contents/models/trk/std'

    try:
        # Request to GitHub API to list files in the directory
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if the request failed
        files = response.json()

        # Loop through all the files in the GitHub folder
        for file_info in files:
            file_name = file_info['name']
            file_download_url = base_url + file_name

            # Handle .trk files and the tarball
            if file_name.endswith('.tgz'):
                print(f"Downloading and extracting {file_name}...")
                tar_file_path = os.path.join(feiden_dir, file_name)

                # Download the tarball
                download_file(file_download_url, tar_file_path)

                # Extract the tarball
                extract_tarball(tar_file_path, feiden_dir)
            
            if download_original_trks:
                if file_name.endswith('.trk'):
                    print(f"Downloading {file_name}...")
                    iso_file_path = os.path.join(feiden_dir, file_name)

                    # Download and save the .iso file
                    download_file(file_download_url, iso_file_path)

    except requests.RequestException as e:
        raise ValueError(f"An error occurred while accessing GitHub: {e}")

    print(f"All files downloaded and extracted in {feiden_dir}")
    print("If you use the Feiden tracks, please cite from: https://ui.adsabs.harvard.edu/abs/2016IAUS..314...79F/abstract")
    
    return 1


def read_feiden_trk_file(feiden_dir):
    """
    Reads all the Feiden track files (*.trk) in the given directory, extracts the age and stellar parameters,
    and organizes the data into numpy arrays.

    Args:
    ------------
    feiden_dir: [str]
        Directory where the Feiden track files are stored.

    Returns:
    ------------
    data_points: [list]
        List of [mass, log_age, Teff, log(L/Lo)] for each star across all .trk files.
    """
    
    # Initialize list to store data points
    data_points = []

    # Iterate over all files ending with '.trk' in the directory
    for file_name in os.listdir(feiden_dir):
        if file_name.endswith('.trk') and file_name[0] != '.':
            file_path = os.path.join(feiden_dir, file_name)

            # Open the file and read its contents
            with open(file_path, 'r') as f:
                mass = None  # To store the mass extracted from the title
                log_age_value = None  # To store the log age for each entry

                # Read through the lines
                for line in f:
                    if line.startswith('#'):
                        # Extract the mass from the line starting with "M="
                        mass_match = re.search(r'M=(\d+\.\d+)', line)
                        if mass_match:
                            mass = float(mass_match.group(1))

                    else:
                        # Parse the columns for stellar parameters (age, log Teff, log L, etc.)
                        parts = line.split()
                        if len(parts) >= 6:
                            age = float(parts[0])  # Age in years
                            log_teff = float(parts[1])  # log Teff
                            teff = 10**log_teff  # Convert log Teff to Teff
                            log_l = float(parts[3])  # log(L/Lo)

                            # Convert age to log(age)
                            log_age_value = np.log10(age)

                            # Append the data point: [mass, log_age, Teff, log(L/Lo)]
                            data_points.append([mass, log_age_value, teff, log_l])

    # Convert data_points to a numpy array for easy manipulation
    data_points = np.array(data_points)

    return data_points


def download_feiden_iso_tracks(save_dir='isochrones_data'):
    """
    Downloads all .iso files and the tarball from the specified GitHub folder and saves them to the given directory.
    The tarball is extracted after downloading.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data'.

    Output:
    ------------
    Downloads all .iso files and the tarball from the GitHub folder, saves them, and extracts the tarball.
    """

    # Create Feiden2016 directory if it doesn't exist
    feiden_dir = os.path.join(save_dir, 'Feiden2016_iso')
    if not os.path.exists(feiden_dir):
        os.makedirs(feiden_dir)

    # Base URL for GitHub raw files
    base_url = 'https://raw.githubusercontent.com/gfeiden/MagneticUpperSco/master/models/iso/std/'
    # URL for the directory on GitHub API
    api_url = 'https://api.github.com/repos/gfeiden/MagneticUpperSco/contents/models/iso/std'

    try:
        # Request to GitHub API to list files in the directory
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if the request failed
        files = response.json()

        # Loop through all the files in the GitHub folder
        for file_info in files:
            file_name = file_info['name']
            file_download_url = base_url + file_name

            # Handle .iso files and the tarball
            if file_name.endswith('.iso'):
                print(f"Downloading {file_name}...")
                iso_file_path = os.path.join(feiden_dir, file_name)

                # Download and save the .iso file
                download_file(file_download_url, iso_file_path)

            elif file_name.endswith('.tgz'):
                print(f"Downloading and extracting {file_name}...")
                tar_file_path = os.path.join(feiden_dir, file_name)

                # Download the tarball
                download_file(file_download_url, tar_file_path)

                # Extract the tarball
                extract_tarball(tar_file_path, feiden_dir)

    except requests.RequestException as e:
        raise ValueError(f"An error occurred while accessing GitHub: {e}")

    print(f"All files downloaded and extracted in {feiden_dir}")
    print("If you use the Feiden tracks, please cite from: https://ui.adsabs.harvard.edu/abs/2016IAUS..314...79F/abstract")
    
    return 1


def read_feiden_iso_file(feiden_dir):
    """
    Reads all the Feiden track files (*.iso) in the given directory, extracts the age and stellar parameters,
    and organizes the data into numpy arrays.

    Args:
    ------------
    feiden_dir: [str]
        Directory where the Feiden track files are stored.

    Returns:
    ------------
    data_points: [list]
        List of [mass, log_age, log(Teff), log(L/Lo)] for each star across all .iso files.
    """
    
    # Initialize list to store data points
    data_points = []

    # Iterate over all files ending with '.iso' in the directory
    for file_name in os.listdir(feiden_dir):
        if file_name.endswith('.iso') and file_name[0] != '.':
            file_path = os.path.join(feiden_dir, file_name)

            # Open the file and read its contents
            with open(file_path, 'r') as f:
                age = None  # To store the age extracted from the title

                # Read through the lines
                for line in f:
                    if line.startswith('#'):
                        # Extract the age from the line starting with "Age ="
                        match = re.search(r'Age\s*=\s*(\d+\.?\d*)\s*Myr', line)
                        if match:
                            age = float(match.group(1))  # Age in Myr
                            log_age_value = np.log10(age * 1e6)  # Convert age to years and take log10

                    else:
                        # Parse the columns for stellar parameters (mass, log(Teff), log(g), etc.)
                        parts = line.split()
                        if len(parts) >= 7:
                            mass = float(parts[0])
                            log_teff = float(parts[1])
                            teff = 10**log_teff
                            log_l = float(parts[3])  # log(L/Lo)

                            # Append the data point: [mass, log_age, Teff, log(L/Lo)]
                            data_points.append([mass, log_age_value, teff, log_l])

    # Convert data_points to a numpy array for easy manipulation
    data_points = np.array(data_points)

    return data_points


def download_parsec_v1p2_tracks(save_dir='isochrones_data'):
    """
    Downloads the PARSECv1p2 tracks tarball from the specified link and saves it to the given directory.
    The tarball is extracted after downloading.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data'.

    Output:
    ------------
    Downloads the tarball from the provided link, saves it, and extracts the tarball.
    """

    # Create PARSECv1p2 directory if it doesn't exist
    parsec_dir = os.path.join(save_dir, 'PARSECv1p2')
    if not os.path.exists(parsec_dir):
        os.makedirs(parsec_dir)

    # URL of the tarball to download
    parsec_url = 'https://people.sissa.it/~sbressan/CAF09_V1.2S_M36_LT/Z0.014Y0.273.tar.gz'

    try:
        # Name of the file to save
        tar_file_name = os.path.join(parsec_dir, 'Z0.014Y0.273.tar.gz')

        # Download the tarball
        print(f"Downloading PARSECv1p2 tracks from {parsec_url}...")
        download_file(parsec_url, tar_file_name)

        # Extract the tarball
        print("Extracting the PARSECv1p2 tarball...")
        extract_tarball(tar_file_name, parsec_dir)

    except requests.RequestException as e:
        raise ValueError(f"An error occurred while downloading the PARSECv1p2 tracks: {e}")

    print(f"All PARSECv1p2 tracks downloaded and extracted in {parsec_dir}")
    print("If you use the PARSEC tracks, please refer to the appropriate papers: https://ui.adsabs.harvard.edu/abs/2012MNRAS.427..127B/abstract as well as the citations mentioned on their webpage: http://stev.oapd.inaf.it/PARSEC/tracks_v12s.html")
    
    return 1


def read_parsec_v1p2_dat_file(parsec_dir):
    """
    Reads all the PARSECv1p2 track files (*.DAT) in the given directory, extracts the mass, age, and stellar parameters (log(Teff), log(L)).
    Organizes the data into numpy arrays.

    Args:
    ------------
    parsec_dir: [str]
        Directory where the PARSECv1p2 track files are stored.

    Returns:
    ------------
    data_points: [list]
        List of [mass, log_age, Teff, log(L/Lo)] for each star across all .DAT files.
    """
    
    # Initialize list to store data points
    data_points = []

    # Iterate over all files ending with '.DAT' in the directory
    for file_name in os.listdir(parsec_dir):
        if file_name.endswith('0.DAT') and file_name[0] != '.':
            file_path = os.path.join(parsec_dir, file_name)

            # Open the file and read its contents
            with open(file_path, 'r') as f:
                mass = None  # To store the mass extracted from the data
                log_age_value = None  # To store the log age for each entry

                # Read through the lines
                for line in f:
                    if line.startswith(' MODELL'):
                        continue  # Skip the header line

                    # Split the line by whitespace
                    parts = line.split()
                    if len(parts) >= 5:
                        try:
                            mass = float(parts[1])  # Mass in solar masses
                            age = float(parts[2])   # Age in years
                            log_l = float(parts[3])  # log(L/Lo)
                            log_teff = float(parts[4])  # log(Teff)

                            if age == 0.0:
                                # skip lines that starts with 0 age
                                continue 
                            
                            else:
                                # Convert age to log(age)
                                log_age_value = np.log10(age)

                                # Convert log Teff to Teff
                                teff = 10**log_teff

                                # Append the data point: [mass, log_age, Teff, log(L/Lo)]
                                data_points.append([mass, log_age_value, teff, log_l])

                        except ValueError:
                            # Skip lines that do not contain valid data
                            continue

    # Convert data_points to a numpy array for easy manipulation
    data_points = np.array(data_points)

    return data_points


def download_parsec_v2p0_tracks(save_dir='isochrones_data'):
    """
    Downloads the PARSEC v2.0 tracks zip file and extracts it to the given directory.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data/PARSECv2p0'.

    Output:
    ------------
    Downloads the PARSEC v2.0 zip file from the specified URL, saves it, and extracts its contents.
    """
    # Define the URL for the PARSEC v2.0 zip file
    url = 'http://stev.oapd.inaf.it/PARSEC/Database/PARSECv2.0/VAR_ROT0.00_SH_Z0.014_Y0.273.zip'

    # Create the target directory if it doesn't exist
    parsec_dir = os.path.join(save_dir, 'PARSECv2p0')
    if not os.path.exists(parsec_dir):
        os.makedirs(parsec_dir)

    # Path where the zip file will be saved
    zip_file_path = os.path.join(parsec_dir, 'PARSECv2p0_tracks.zip')

    # Download the zip file
    print(f"Downloading PARSECv2p0 tracks from {url}...")
    download_file(url, zip_file_path)
    
    # try:
    #     print(f"Downloading PARSEC v2.0 tracks from {url}...")
    #     response = requests.get(url, stream=True)
    #     response.raise_for_status()  # Raise an error if the download fails

    #     # Save the downloaded zip file
    #     with open(zip_file_path, 'wb') as f:
    #         for chunk in response.iter_content(chunk_size=1024):
    #             if chunk:
    #                 f.write(chunk)
    #     print(f"File downloaded successfully and saved to {zip_file_path}")
        
    # except requests.RequestException as e:
    #     raise ValueError(f"An error occurred while downloading the file: {e}")
    
    # Extract the zip file
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(parsec_dir)
        print(f"Files extracted to {parsec_dir}")
    except zipfile.BadZipFile as e:
        raise ValueError(f"An error occurred while extracting the zip file: {e}")
    
    print(f"All PARSECv2p0 tracks downloaded and extracted in {parsec_dir}")
    print("If you use the PARSEC tracks, please refer to the appropriate papers: https://ui.adsabs.harvard.edu/abs/2012MNRAS.427..127B/abstract and https://ui.adsabs.harvard.edu/abs/2022arXiv220708642N/abstract as well as the citations mentioned on their webpage: http://stev.oapd.inaf.it/PARSEC/tracks_v2.html")
    
    # Optionally, you can remove the zip file after extraction to save space
    # os.remove(zip_file_path)
    # print(f"Downloaded zip file removed after extraction.")

    return 1


def read_parsec_v2p0_tab_file(parsec_dir):
    """
    Reads all the PARSECv2.0 track files (*.TAB) in the given directory, extracts the mass, age, and stellar parameters (log(Teff), log(L)).
    Organizes the data into numpy arrays.

    Args:
    ------------
    parsec_dir: [str]
        Directory where the PARSECv2.0 track files are stored.

    Returns:
    ------------
    data_points: [list]
        List of [mass, log_age, Teff, log(L/Lo)] for each star across all .TAB files.
    """
    
    # Initialize list to store data points
    data_points = []

    # Iterate over all files ending with '.TAB' in the directory
    for file_name in os.listdir(parsec_dir):
        if file_name.endswith('.TAB') and file_name[0] != '.':
            file_path = os.path.join(parsec_dir, file_name)

            # Open the file and read its contents
            with open(file_path, 'r') as f:
                mass = None  # To store the mass extracted from the data
                log_age_value = None  # To store the log age for each entry

                # Read lines from the 6th line onward
                for line_num, line in enumerate(f):
                    if line_num < 5:
                        continue  # Skip lines before line 6
                    
                    # Skip header lines
                    if line.startswith('BEGIN TRACK') or line.startswith(' MODE'):
                        continue

                    # Split the line by whitespace
                    parts = line.split()
                    if len(parts) >= 6:
                        try:
                            # Extract the stellar parameters
                            mass = float(parts[1])      # Mass in solar masses
                            age = float(parts[2])       # Age in years
                            log_l = float(parts[4])     # log(L/Lo)
                            log_teff = float(parts[5])  # log(Teff)

                            if age == 0.0:
                                # Skip entries with zero age
                                continue
                            
                            # Convert age to log(age)
                            log_age_value = np.log10(age)

                            # Convert log Teff to Teff
                            teff = 10**log_teff

                            # Append the data point: [mass, log_age, Teff, log(L/Lo)]
                            data_points.append([mass, log_age_value, teff, log_l])

                        except ValueError:
                            # Skip lines that do not contain valid data
                            continue

    # Convert data_points to a numpy array for easy manipulation
    data_points = np.array(data_points)

    return data_points


def download_mist_v1p2_eep_tracks(save_dir='isochrones_data'):
    """
    Downloads the MIST v1.2 tracks tarball and extracts it to the given directory.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data/MIST_v1p2'.

    Output:
    ------------
    Downloads the MIST v1.2 tarball from the specified URL, saves it, and extracts its contents.
    """
    # Define the URL for the MIST v1.2 tarball
    url = 'https://waps.cfa.harvard.edu/MIST/data/tarballs_v1.2/MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS.txz'

    # Create the target directory if it doesn't exist
    mist_dir = os.path.join(save_dir, 'MIST_v1p2_eep')
    if not os.path.exists(mist_dir):
        os.makedirs(mist_dir)

    # Path where the tarball file will be saved
    tarball_file_path = os.path.join(mist_dir, 'MIST_v1p2_tracks.txz')

    # Download the tarball
    print(f"Downloading MIST v1.2 tracks from {url}...")
    download_file(url, tarball_file_path)
    
    # Extract the tarball file
    try:
        print(f"Extracting the tarball to {mist_dir}...")
        with tarfile.open(tarball_file_path, 'r:xz') as tar_ref:
            tar_ref.extractall(mist_dir)
        print(f"Files extracted to {mist_dir}")
    except tarfile.TarError as e:
        raise ValueError(f"An error occurred while extracting the tarball: {e}")
    
    print(f"All MIST v1.2 tracks downloaded and extracted in {mist_dir}")
    print("If you use the MIST tracks, please refer to their webpage: https://waps.cfa.harvard.edu/MIST/index.html")
    
    # Optionally, you can remove the tarball file after extraction to save space
    # os.remove(tarball_file_path)
    # print(f"Downloaded tarball removed after extraction.")

    return 1


def download_mist_v1p2_iso_tracks(save_dir='isochrones_data'):
    """
    Downloads the MIST v1.2 tracks tarball and extracts it to the given directory.

    Args:
    ------------
    save_dir: [str, optional]
        The directory where the files should be saved. Defaults to 'isochrones_data/MIST_v1p2'.

    Output:
    ------------
    Downloads the MIST v1.2 tarball from the specified URL, saves it, and extracts its contents.
    """
    # Define the URL for the MIST v1.2 tarball
    url = 'https://waps.cfa.harvard.edu/MIST/data/tarballs_v1.2/MIST_v1.2_vvcrit0.0_basic_isos.txz'

    # Create the target directory if it doesn't exist
    mist_dir = os.path.join(save_dir, 'MIST_v1p2_iso')
    if not os.path.exists(mist_dir):
        os.makedirs(mist_dir)

    # Path where the tarball file will be saved
    tarball_file_path = os.path.join(mist_dir, 'MIST_v1p2_tracks.txz')

    # Download the tarball
    print(f"Downloading MIST v1.2 tracks from {url}...")
    download_file(url, tarball_file_path)
    
    # Extract the tarball file
    try:
        print(f"Extracting the tarball to {mist_dir}...")
        with tarfile.open(tarball_file_path, 'r:xz') as tar_ref:
            tar_ref.extractall(mist_dir)
        print(f"Files extracted to {mist_dir}")
    except tarfile.TarError as e:
        raise ValueError(f"An error occurred while extracting the tarball: {e}")
    
    print(f"All MIST v1.2 tracks downloaded and extracted in {mist_dir}")
    print("If you use the MIST tracks, please refer to their webpage: https://waps.cfa.harvard.edu/MIST/index.html")
    
    # Optionally, you can remove the tarball file after extraction to save space
    # os.remove(tarball_file_path)
    # print(f"Downloaded tarball removed after extraction.")

    return 1


def read_mist_v1p2_iso_file(mist_iso_file):
    """
    Reads the MISTv1p2 isochrone file in the given directory, extracts the star mass, log(Teff), and log(L/Lo).
    Organizes the data into numpy arrays.

    Args:
    ------------
    mist_iso_file: [str]
        The file where the MISTv1p2 isochrone file is stored.

    Returns:
    ------------
    data_points: [list]
        List of [star_mass, log_age, Teff, log(L/Lo)] for each entry in the iso file.
    """
    
    # Initialize list to store data points
    data_points = []

    # Iterate over files in the mist_dir, expecting one iso file
    # for file_name in os.listdir(mist_iso_file):
    #     if file_name.endswith('.iso') and file_name[0] != '.':
    #         file_path = os.path.join(mist_iso_file, file_name)
    
    # We only read in one file with the solar metallicity for now
    file_path = mist_iso_file
    
    # Open the file and read its contents
    with open(file_path, 'r') as f:
        log_age_value = None  # To store the log age for each entry

        # Read through the lines
        for line_num, line in enumerate(f):
            # Skip the first few lines until data starts (after line 11)
            if line_num < 12:
                continue

            # Skip header-like lines
            if line.startswith('#'):
                continue

            # Split the line by whitespace
            parts = line.split()
            if len(parts) >= 25:  # Ensure we have all columns we need
                try:
                    # Extract the stellar parameters from the correct columns
                    log_age_value = float(parts[1])   # log10_isochrone_age_yr
                    star_mass = float(parts[3])       # star_mass
                    log_l = float(parts[7])           # log(L/Lo)
                    log_teff = float(parts[10])       # log(Teff)

                    # Convert log Teff to Teff
                    teff = 10**log_teff

                    # Append the data point: [star_mass, log_age, Teff, log(L/Lo)]
                    data_points.append([star_mass, log_age_value, teff, log_l])

                except ValueError:
                    # Skip lines that do not contain valid data
                    continue

    # Convert data_points to a numpy array for easy manipulation
    data_points = np.array(data_points)

    return data_points


def create_meshgrid(data_points, min_age=0.5, max_age=500.0, interpolation_method='linear'):
    """
    Creates a meshgrid for log_age and masses, and populates it with Teff and luminosity.

    Args:
    ------------
    data_points: [np.array]
        Array of [log_age, mass, teff, log_luminosity] data points.
    min_age: [float, optional] unit: Myrs
        The minimum age that we will cut in this grid. Default = 0.5 Myrs
    max_age: [float, optional] unit: Myrs
        The maximum age that we will cut in this grid. Default = 500 Myrs because we are mainly interested in YSOs in this package. We set up a max_age so that we avoid the problem of dealing with the post-main-sequence targets (their luminosity rises up again and will overlay on the pre-main-sequence phase). 
        **NOTE** will add the feature to automatiaclly capture the turn-over point in the future.
    interpolation_method: [str]
        The interpolation method used in griddata. Default 'linear'.

    Returns:
    ------------
    log_age_grid: [np.array]
        2D meshgrid of log age values.
    masses_grid: [np.array]
        2D meshgrid of mass values.
    logtlogl_grid: [np.array]
        2D array of [log(Teff), log(Luminosity)] values mapped onto the grid.
    """
    masses = data_points[:, 0]
    log_age = data_points[:, 1]
    # print(masses)
    # print(log_age)
    teff = data_points[:, 2]
    log_luminosity = data_points[:, 3]
    
    # Create a grid for unique log_age and masses
    log_age_unique = np.unique(log_age)
    masses_unique = np.unique(masses)

    # create the grid points for the log_age and masses
    if np.nanmin(log_age_unique) >= np.log10(min_age * 1e6):
        min_log_age = np.nanmin(log_age_unique)
    else: min_log_age = np.log10(min_age * 1e6)
    if np.nanmax(log_age_unique) <= np.log10(max_age * 1e6):
        max_log_age = np.nanmax(log_age_unique)
    else: max_log_age = np.log10(max_age * 1e6)
    # print(max_log_age)
    log_age_i = np.arange(min_log_age, max_log_age + 0.01, 0.01) # log_age_unique
    # print(log_age_i)
    log_masses_unique = np.log10(masses_unique)
    masses_i = 10**np.arange(np.nanmin(log_masses_unique), np.nanmax(log_masses_unique) + 0.01, 0.01) # masses_unique
    
    # Create a meshgrid for log_age and masses
    log_age_grid, masses_grid = np.meshgrid(log_age_i, masses_i, indexing='ij')

    # Use griddata to interpolate Teff and Luminosity onto the meshgrid
    log_teff_grid = griddata((log_age, masses), np.log10(teff), (log_age_grid, masses_grid), method=interpolation_method)
    log_luminosity_grid = griddata((log_age, masses), log_luminosity, (log_age_grid, masses_grid), method=interpolation_method)

    # Combine Teff and Luminosity into a single 2D array (logtlogl)
    logtlogl_grid = np.stack([log_teff_grid, log_luminosity_grid], axis=-1)

    return masses_i, log_age_i, logtlogl_grid, masses_grid, log_age_grid


def save_as_mat(masses, log_age, logtlogl, save_path):
    """
    Saves the extracted data into a .mat file.

    Args:
    ------------
    masses: [np.array]
        Array of masses (M/Ms).
    log_age: [np.array]
        Array of log age values.
    logtlogl: [np.array]
        2D array of Teff and L/Ls values.
    save_path: [str]
        Path to save the .mat file.
    """
    # Create a dictionary to hold the data in a similar structure as the .sav file
    data_dict = {
        'mass': masses,
        'log_age': log_age,
        'logt_logl': logtlogl
    }

    # Save the dictionary as a .mat file
    scipy.io.savemat(save_path, data_dict)
    print(f"Data saved to {save_path}")

    return 1


def compare_grids(loaded_data_py, loaded_data_idl, gridnames=['Python', 'IDL'], plot=True):
    """
    Compares the Python and IDL-generated grids by interpolating the Python grid onto the sparser IDL grid
    and plotting the differences.

    Args:
    ------------
    loaded_data_py: [dict]
        Dictionary containing the Python-generated grid data (masses, log_age, logtlogl).
    loaded_data_idl: [dict]
        Dictionary containing the IDL-generated grid data (masses, log_age, logtlogl).
    gridnames: [list of strings, optional]
        The names of the grid names, default is Python and IDL
    plot: [bool, optional]: 
        Whether to plot the differences

    Output:
    ------------
    A visual comparison of the Python and IDL grids with difference and normalized difference plots.
    """
    
    # Load data from Python
    masses_py = loaded_data_py['mass'][0]
    log_age_py = loaded_data_py['log_age'][0]
    logtlogl_py = loaded_data_py['logt_logl']  # Shape: [n_log_age, n_mass, 2] for Teff and L/Lo

    # Load data from IDL
    masses_idl = loaded_data_idl['mass']
    log_age_idl = loaded_data_idl['log_age']
    logtlogl_idl = loaded_data_idl['logt_logl']  # Shape: [n_log_age, n_mass, 2] for Teff and L/Lo

    # Interpolation: First, create the grid to interpolate Python data onto the IDL grid
    grid_idl = np.array(np.meshgrid(log_age_idl, masses_idl)).T.reshape(-1, 2)
    
    # Interpolate Python logtlogl data onto the IDL grid
    logtlogl_interp_py = np.zeros_like(logtlogl_idl)

    for i in range(2):  # For both Teff and L/Lo
        points_py = np.array(np.meshgrid(log_age_py, masses_py)).T.reshape(-1, 2)
        values_py = logtlogl_py[:, :, i].flatten()
        
        # Use griddata to interpolate Python logtlogl onto the IDL grid
        logtlogl_interp_py[:, :, i] = griddata(points_py, values_py, grid_idl).reshape(logtlogl_idl.shape[0], logtlogl_idl.shape[1])

    # Calculate the differences between the interpolated Python data and IDL data
    logtlogl_diff = logtlogl_interp_py - logtlogl_idl

    # Calculate the normalized differences (relative differences)
    logtlogl_diff_norm = logtlogl_diff / logtlogl_interp_py

    # Plot the results
    if plot:
        plotting.plot_comparison(log_age_idl, masses_idl, logtlogl_interp_py, logtlogl_idl, logtlogl_diff, logtlogl_diff_norm, gridnames)

    return logtlogl_diff, logtlogl_diff_norm


# the job of calling these classes are now moved into another py file called isochrone

# def use_tracks_Baraffe():
#     """
#     Returns the log_age_dummy and masses_dummy for the Baraffe tracks.

#     Args:
#     ------------
#     None

#     Output:
#     ------------
#     Returns:
#     ------------
#     log_age_dummy: [array]
#         Array of log(age) values for the Baraffe tracks.
#     masses_dummy: [array]
#         Array of mass values for the Baraffe tracks.
#     logtlogl_dummy: [array]
#         Array of log(T) and log(L) for the Baraffe tracks.
#     """
#     log_age_dummy = ba_logage
#     masses_dummy = ba_masses
#     logtlogl_dummy = ba_logt_logl
#     return log_age_dummy, masses_dummy, logtlogl_dummy


# def use_tracks_Feiden():
#     """
#     Returns the log_age_dummy and masses_dummy for the Feiden tracks.

#     Args:
#     ------------
#     None

#     Output:
#     ------------
#     Returns:
#     ------------
#     log_age_dummy: [array]
#         Array of log(age) values for the Feiden tracks.
#     masses_dummy: [array]
#         Array of mass values for the Feiden tracks.
#     logtlogl_dummy: [array]
#         Array of log(T) and log(L) for the Feiden tracks.
#     """
#     log_age_dummy = f_logage
#     masses_dummy = f_masses
#     logtlogl_dummy = f_logt_logl
#     return log_age_dummy, masses_dummy, logtlogl_dummy

