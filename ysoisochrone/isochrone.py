#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/14/2025

import os
import scipy.io
# from scipy.interpolate import griddata
from ysoisochrone import utils
from ysoisochrone import registry

class Isochrone:
    """
    Isochrone class for setting up log_age, masses, and logtlogl attributes
    now it works for Baraffe and Feiden tracks.

    Args:
    
        data_dir: [str, optional]
            Directory where the isochrone data files are stored. Default is a folder called 'isochrone_data' under where you are running the code.

    Attributes:
    
        log_age: [array]
            Array of log(age) values.
        masses: [array]
            Array of mass values.
        logtlogl: [array]
            Array of log(T) and log(L) values for the evolutionary tracks.
    """

    def __init__(self, data_dir=None):
        """
        Initialize Isochrone object.

        Args:
            data_dir: [str or None]
                - None  → use the built-in isochrone matrices packaged
                        inside ysoisochrone/data.
                - path  → load isochrone matrices from this directory
                        (user-supplied custom matrices).
        """
        # self.data_dir = data_dir if data_dir else os.path.join(os.getcwd(), 'isochrones_data')
        
        if data_dir is None:
            # Use packaged built-in grids
            self.use_builtin = True
            self.data_dir = None          # Don't point to a local folder
            print("using the built in isochrones")
            print("-----------------------")
        else:
            # User-specified directory
            self.use_builtin = False
            self.data_dir = data_dir
            print("using the user-specified isochrones inside")
            print("%s"%(self.data_dir))
            print("-----------------------")

        self.log_age = None
        self.masses = None
        self.logtlogl = None

    def prepare_baraffe_tracks(self):
        """
        Prepares the Baraffe BHAC15 tracks file by downloading it if necessary, reading the data,
        interpolating it into a meshgrid, and saving it as a .mat file.

        The method:
        1. Checks if the BHAC15 tracks file exists in the data directory.
        2. Downloads the file if it doesn't exist.
        3. Reads the file, creates a meshgrid for log_age and masses, and interpolates logtlogl data.
        4. Saves the resulting grid data to a .mat file.

        Args:
        
            None.

        Output:
        
            Saves the .mat file to the data directory.
        """

        # Define the paths
        input_file = os.path.join(self.data_dir, 'Baraffe2015', 'BHAC15_tracks+structure')
        output_mat_file = os.path.join(self.data_dir, 'Baraffe_AgeMassGrid_YSO_matrix.mat')

        # Check if the original BHAC15 data file exists, download if necessary
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}. Downloading the file.")
            utils.download_baraffe_tracks(save_dir=self.data_dir)

        # Read the original BHAC15 tracks file
        data_points = utils.read_baraffe_file(input_file)

        # Create meshgrid and interpolate the data onto the grid
        masses_i, log_age_i, logtlogl_grid, _, _ = utils.create_meshgrid(data_points)

        # Save the parsed data to a .mat file
        utils.save_as_mat(masses_i, log_age_i, logtlogl_grid, output_mat_file)
        print(f"File saved as: {output_mat_file}")
        
        return 1
    
    def prepare_feiden_tracks(self):
        """
        Prepares the Feiden 2016 tracks file by downloading it if necessary, reading the data,
        interpolating it into a meshgrid, and saving it as a .mat file.

        The method:
        1. Checks if the Feiden2016_trk tracks file exists in the data directory.
        2. Downloads the file if it doesn't exist.
        3. Reads the file, creates a meshgrid for log_age and masses, and interpolates logtlogl data.
        4. Saves the resulting grid data to a .mat file.

        Args:
        
            None.

        Output:
        
            Saves the .mat file to the data directory.
        """

        # Define the paths
        input_file_dir = os.path.join(self.data_dir, 'Feiden2016_trk')
        output_mat_file = os.path.join(self.data_dir, 'Feiden_AgeMassGrid_YSO_matrix.mat')

        # Check if the original feiden data file exists, download if necessary
        print('please make sure all the iso tracks for all the ages you are interested in are in the file dir, this code will not automatically check you included all of your tracks')
        if not os.path.exists(os.path.join(input_file_dir, 'all_GS98_p000_p0_y28_mlt1.884.tgz')):
            print(f"File not found: {input_file_dir}. Downloading the file.")
            utils.download_feiden_trk_tracks(save_dir=self.data_dir)

        # Read the original Feiden tracks file
        data_points = utils.read_feiden_trk_file(input_file_dir)

        # Create meshgrid and interpolate the data onto the grid
        masses_i, log_age_i, logtlogl_grid, _, _ = utils.create_meshgrid(data_points)

        # Save the parsed data to a .mat file
        utils.save_as_mat(masses_i, log_age_i, logtlogl_grid, output_mat_file)
        print(f"File saved as: {output_mat_file}")
        
        return 1
    
    
    def prepare_parsecv1p2_tracks(self):
        """
        Prepares the PARSEC v1.2 tracks file by downloading it if necessary, reading the data,
        interpolating it into a meshgrid, and saving it as a .mat file.

        The method:
        1. Checks if the PARSEC v1.2 tracks file exists in the data directory.
        2. Downloads the file if it doesn't exist.
        3. Reads the file, creates a meshgrid for log_age and masses, and interpolates logtlogl data.
        4. Saves the resulting grid data to a .mat file.

        Args:
        
            None.

        Output:
        
            Saves the .mat file to the data directory.
        """
        
        # Define the paths
        input_file_dir = os.path.join(self.data_dir, 'PARSECv1p2')
        output_mat_file = os.path.join(self.data_dir, 'PARSECv1p2_AgeMassGrid_YSO_matrix.mat')

        # Check if the original data file exists, download if necessary
        print('please make sure all the iso tracks for all the ages you are interested in are in the file dir, this code will not automatically check you included all of your tracks')
        if not os.path.exists(os.path.join(input_file_dir, 'Z0.014Y0.273.tar.gz')):
            print(f"File not found: {input_file_dir}. Downloading the file.")
            utils.download_parsec_v1p2_tracks(save_dir=self.data_dir)

        # Read the original tracks file
        data_points = utils.read_parsec_v1p2_dat_file(os.path.join(input_file_dir, 'Z0.014Y0.273'))

        # Create meshgrid and interpolate the data onto the grid
        masses_i, log_age_i, logtlogl_grid, _, _ = utils.create_meshgrid(data_points)

        # Save the parsed data to a .mat file
        utils.save_as_mat(masses_i, log_age_i, logtlogl_grid, output_mat_file)
        print(f"File saved as: {output_mat_file}")
        
        return 1
    
    
    def prepare_parsecv2p0_tracks(self):
        """
        Prepares the PARSEC v2.0 tracks file by downloading it if necessary, reading the data,
        interpolating it into a meshgrid, and saving it as a .mat file.

        The method:
        1. Checks if the PARSEC v2.0 tracks file exists in the data directory.
        2. Downloads the file if it doesn't exist.
        3. Reads the file, creates a meshgrid for log_age and masses, and interpolates logtlogl data.
        4. Saves the resulting grid data to a .mat file.

        Args:
        
            None.

        Output:
        
            Saves the .mat file to the data directory.
        """
        
        # Define the paths
        input_file_dir = os.path.join(self.data_dir, 'PARSECv2p0')
        output_mat_file = os.path.join(self.data_dir, 'PARSECv2p0_AgeMassGrid_YSO_matrix.mat')

        # Check if the original data file exists, download if necessary
        print('please make sure all the iso tracks for all the ages you are interested in are in the file dir, this code will not automatically check you included all of your tracks')
        if not os.path.exists(os.path.join(input_file_dir, 'VAR_ROT0.00_SH_Z0.014_Y0.273.zip')):
            print(f"File not found: {input_file_dir}. Downloading the file.")
            utils.download_parsec_v2p0_tracks(save_dir=self.data_dir)

        # Read the original tracks file
        data_points = utils.read_parsec_v2p0_tab_file(os.path.join(input_file_dir, 'VAR_ROT0.00_SH_Z0.014_Y0.273'))

        # Create meshgrid and interpolate the data onto the grid
        masses_i, log_age_i, logtlogl_grid, _, _ = utils.create_meshgrid(data_points)

        # Save the parsed data to a .mat file
        utils.save_as_mat(masses_i, log_age_i, logtlogl_grid, output_mat_file)
        print(f"File saved as: {output_mat_file}")
        
        return 1
    
    
    def prepare_mistv1p2_tracks(self):
        """
        Prepares the MIST v1.2 tracks file by downloading it if necessary, reading the data,
        interpolating it into a meshgrid, and saving it as a .mat file.

        The method:
        1. Checks if the MIST v1.2 tracks file exists in the data directory.
        2. Downloads the file if it doesn't exist.
        3. Reads the file, creates a meshgrid for log_age and masses, and interpolates logtlogl data.
        4. Saves the resulting grid data to a .mat file.

        Args:
        
            None.

        Output:
        
            Saves the .mat file to the data directory.
        """
        
        # Define the paths
        # input_file_dir = os.path.join(self.data_dir, 'MIST_v1p2_iso')
        input_file = os.path.join(self.data_dir, 'MIST_v1p2_iso', 'MIST_v1.2_vvcrit0.0_basic_isos', 'MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_basic.iso')
        output_mat_file = os.path.join(self.data_dir, 'MIST_v1p2_AgeMassGrid_YSO_matrix.mat')

        # Check if the original feiden data file exists, download if necessary
        print('please make sure all the iso tracks for all the ages you are interested in are in the file dir, this code will not automatically check you included all of your tracks')
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}. Downloading the file.")
            utils.download_mist_v1p2_iso_tracks(save_dir=self.data_dir)

        # Read the original tracks file
        data_points = utils.read_mist_v1p2_iso_file(input_file)

        # Create meshgrid and interpolate the data onto the grid
        masses_i, log_age_i, logtlogl_grid, _, _ = utils.create_meshgrid(data_points)

        # Save the parsed data to a .mat file
        utils.save_as_mat(masses_i, log_age_i, logtlogl_grid, output_mat_file)
        print(f"File saved as: {output_mat_file}")
        
        return 1
    
    
    def load_baraffe2015_tracks(self):
        """
        Load Baraffe isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        Uses packaged built-in matrix by default, unless user provides a custom data_dir.
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the Baraffe tracks.
        masses: [array]
            Mass values from the Baraffe tracks.
        logtlogl: [array]
            Log T and Log L values from the Baraffe tracks.
        """
        # file_path = os.path.join(self.data_dir, 'Baraffe_AgeMassGrid.sav')
        # data = scipy.io.readsav(file_path)
        # self.masses = data['mass']
        # self.log_age = data['log_age']
        # self.logtlogl = data['logt_logl']
        
        # input_file = os.path.join(self.data_dir, 'Baraffe_AgeMassGrid_YSO_matrix.mat')
        # # Check if the original Baraffe 2015 data file exists, download if necessary
        # if not os.path.exists(input_file):
        #     self.prepare_baraffe_tracks()
        
        # data = scipy.io.loadmat(input_file)
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('Baraffe_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory
        else:
            input_file = os.path.join(self.data_dir, 'Baraffe_AgeMassGrid_YSO_matrix.mat')

            if not os.path.exists(input_file):
                # Build from raw tracks if needed
                self.prepare_baraffe_tracks()

            data = scipy.io.loadmat(input_file)
             
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1

    def load_feiden2016_tracks(self):
        """
        Load Feiden isochrone tracks from .sav file and set log_age, masses, and logtlogl.

        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the Feiden tracks.
        masses: [array]
            Mass values from the Feiden tracks.
        logtlogl: [array]
            Log T and Log L values from the Feiden tracks.
        """
        # file_path = os.path.join(self.data_dir, 'Feiden_AgeMassGrid.sav')
        # data = scipy.io.readsav(file_path)
        # self.masses = data['mass']
        # self.log_age = data['log_age']
        # self.logtlogl = data['logt_logl']
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('Feiden_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory
        else:
            input_file = os.path.join(self.data_dir, 'Feiden_AgeMassGrid_YSO_matrix.mat')
            # Check if the original Feiden 2016 data file exists, download if necessary
            if not os.path.exists(input_file):
                self.prepare_feiden_tracks()
            
            data = scipy.io.loadmat(input_file)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_feiden2016_magnetic_tracks(self):
        """
        Load Feiden isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. The original Feiden
        magnetic grids contain known issues at ages < 10 Myr, and a corrected
        version is provided in the ysoisochrone built-in matrices.
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the Feiden tracks.
        masses: [array]
            Mass values from the Feiden tracks.
        logtlogl: [array]
            Log T and Log L values from the Feiden tracks.
        """
        # file_path = os.path.join(self.data_dir, 'Feiden_AgeMassGrid.sav')
        # data = scipy.io.readsav(file_path)
        # self.masses = data['mass']
        # self.log_age = data['log_age']
        # self.logtlogl = data['logt_logl']
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('Feiden_B_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: Feiden magnetic tracks cannot be generated from the "
                "raw Feiden database because the original magnetic models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected magnetic tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('Feiden2016_magnetic')\n\n"
                "If you want to use your own customized magnetic grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/Feiden_B_AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_parsecv1p2_tracks(self):
        """
        Load PARSEC v1.2 isochrone tracks from .sav file and set log_age, masses, and logtlogl.

        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the PARSEC v1.2 tracks.
        masses: [array]
            Mass values from the PARSEC v1.2 tracks.
        logtlogl: [array]
            Log T and Log L values from the PARSEC v1.2 tracks.
        """
        
        input_file = os.path.join(self.data_dir, 'PARSECv1p2_AgeMassGrid_YSO_matrix.mat')
        # Check if the original data file exists, download if necessary
        if not os.path.exists(input_file):
            self.prepare_parsecv1p2_tracks()
            
        data = scipy.io.loadmat(input_file)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    def load_parsecv2p0_tracks(self):
        """
        Load PARSEC v2.0 isochrone tracks from .sav file and set log_age, masses, and logtlogl.

        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the PARSEC v2.0 tracks.
        masses: [array]
            Mass values from the PARSEC v2.0 tracks.
        logtlogl: [array]
            Log T and Log L values from the PARSEC v2.0 tracks.
        """
        
        input_file = os.path.join(self.data_dir, 'PARSECv2p0_AgeMassGrid_YSO_matrix.mat')
        # Check if the original data file exists, download if necessary
        if not os.path.exists(input_file):
            self.prepare_parsecv2p0_tracks()
            
        data = scipy.io.loadmat(input_file)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    def load_mistv1p2_tracks(self):
        """
        Load MIST v1.2 isochrone tracks from .sav file and set log_age, masses, and logtlogl.

        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the MIST v1.2 tracks.
        masses: [array]
            Mass values from the MIST v1.2 tracks.
        logtlogl: [array]
            Log T and Log L values from the MIST v1.2 tracks.
        """
        
        input_file = os.path.join(self.data_dir, 'MIST_v1p2_AgeMassGrid_YSO_matrix.mat')
        # Check if the original data file exists, download if necessary
        if not os.path.exists(input_file):
            self.prepare_mistv1p2_tracks()
            
        data = scipy.io.loadmat(input_file)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_siess2000_tracks(self):
        """
        Load Siess2000 isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the Siess2000 tracks.
        masses: [array]
            Mass values from the Siess2000 tracks.
        logtlogl: [array]
            Log T and Log L values from the Siess2000 tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('Siess_combined_final_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: Feiden magnetic tracks cannot be generated from the "
                "raw Feiden database because the original magnetic models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected magnetic tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('Feiden2016_magnetic')\n\n"
                "If you want to use your own customized magnetic grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    
    def load_spots0000_tracks(self):
        """
        Load SPOTS isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the SPOTS tracks.
        masses: [array]
            Mass values from the SPOTS tracks.
        logtlogl: [array]
            Log T and Log L values from the SPOTS tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('SPOTS_Fspot_0000_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: SPOTS 0000 cannot be generated from the "
                "raw SPOTS database because the original SPOTS models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected SPOTS tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('SPOTS_0000')\n\n"
                "If you want to use your own customized SPOTS grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_spots0169_tracks(self):
        """
        Load SPOTS isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the SPOTS tracks.
        masses: [array]
            Mass values from the SPOTS tracks.
        logtlogl: [array]
            Log T and Log L values from the SPOTS tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('SPOTS_Fspot_0169_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: SPOTS 0169 cannot be generated from the "
                "raw SPOTS database because the original SPOTS models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected SPOTS tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('SPOTS_0169')\n\n"
                "If you want to use your own customized SPOTS grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_spots0339_tracks(self):
        """
        Load SPOTS isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the SPOTS tracks.
        masses: [array]
            Mass values from the SPOTS tracks.
        logtlogl: [array]
            Log T and Log L values from the SPOTS tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('SPOTS_Fspot_0339_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: SPOTS 0339 cannot be generated from the "
                "raw SPOTS database because the original SPOTS models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected SPOTS tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('SPOTS_0339')\n\n"
                "If you want to use your own customized SPOTS grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    
    def load_spots0508_tracks(self):
        """
        Load SPOTS isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the SPOTS tracks.
        masses: [array]
            Mass values from the SPOTS tracks.
        logtlogl: [array]
            Log T and Log L values from the SPOTS tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('SPOTS_Fspot_0508_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: SPOTS 0508 cannot be generated from the "
                "raw SPOTS database because the original SPOTS models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected SPOTS tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('SPOTS_0508')\n\n"
                "If you want to use your own customized SPOTS grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    
    def load_spots0847_tracks(self):
        """
        Load SPOTS isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the SPOTS tracks.
        masses: [array]
            Mass values from the SPOTS tracks.
        logtlogl: [array]
            Log T and Log L values from the SPOTS tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('SPOTS_Fspot_0847_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: SPOTS 0847 tracks cannot be generated from the "
                "raw SPOTS database because the original SPOTS models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected SPOTS tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('SPOTS_0847')\n\n"
                "If you want to use your own customized SPOTS grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    
    def load_pisa_tracks(self):
        """
        Load Pisa isochrone tracks from .sav file and set log_age, masses, and logtlogl.
        
        Only the built-in corrected matrix is supported. 
        
        Output:
        
        Sets:
        
        log_age: [array]
            Log age values from the Pisa tracks.
        masses: [array]
            Mass values from the Pisa tracks.
        logtlogl: [array]
            Log T and Log L values from the Pisa tracks.
        """
        
        # Case 1: packaged built-in matrix (default)
        if self.use_builtin:
            data = utils.load_builtin_matrix('Pisa_AgeMassGrid_YSO_builtin_matrix.mat')

        # Case 2: user-provided local directory → NOT allowed for magnetic tracks
        else:
            msg = (
                "\nERROR: Pisa tracks cannot be generated from the "
                "raw Pisa database because the original Pisa models contain "
                "known issues at ages younger than 10 Myr.\n\n"
                "The built-in matrix included in ysoisochrone contains corrections "
                "for these issues.\n\n"
                "To use the corrected Pisa tracks:\n"
                "    -> Initialize Isochrone without specifying data_dir:\n"
                "           iso = Isochrone()\n"
                "    -> And then use:\n"
                "           iso.set_tracks('Pisa')\n\n"
                "If you want to use your own customized Pisa grid, you must\n"
                "manually supply a corrected matrix at and use the function\n"
                "    -> iso = ysoisochrone.isochrone.Isochrone()\n"
                "Then set the absolute path to your matrix file, for example\n"
                "    -> mat_file_dir = 'User/isochrones/AgeMassGrid_YSO_customized_matrix.mat'\n"
                "    -> isochrone.set_tracks('customize', load_file=mat_file_dir)\n"
            )
            raise ValueError(msg)
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1
    
    
    def load_tracks_from_customize_matrix(self, load_file):
        """
        Load the isochromes from any customized matrix
        
        Args:
        
            load_file: [str]
                the .mat file that contains mass grid, log_age grid, and logt_logl grid
        
        Sets:
        
            log_age: [array]
                Log age values from the Feiden tracks.
            masses: [array]
                Mass values from the Feiden tracks.
            logtlogl: [array]
                Log T and Log L values from the Feiden tracks.
        """
        
        input_file = os.path.join(load_file)
        data = scipy.io.loadmat(input_file)
        
        print("using the user-specified isochrone matrix of")
        print("%s"%(load_file))
        print("-----------------------")
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1

    def set_tracks_legacy(self, track_type, load_file=''):
        """
        Set the isochrone tracks based on track_type.

        Args:
        
            track_type: [str]
                Type of the tracks to use ('baraffe2015' or 'feiden2016' or 'customize').
            load_file: [str]
                the .mat file that contains mass grid, log_age grid, and logt_logl grid
                Default is '', so if you want to read in the customized datafile, 
                remember to set up this parameter

        Output:
        
            Loads the corresponding track (Baraffe or Feiden) and sets the appropriate attributes.
        """
        if track_type.lower() == 'baraffe2015':
            self.load_baraffe2015_tracks()
        elif track_type.lower() in ['feiden2016', 'feiden2016_nob', 'feiden2016_nonmagnetic']:
            self.load_feiden2016_tracks()
        elif track_type.lower() in ['feiden2016_b', 'feiden2016_magnetic']:
            self.load_feiden2016_magnetic_tracks()
        elif track_type.lower() in ['parsec', 'parsec_v2p0']:
            self.load_parsecv2p0_tracks()
        elif track_type.lower() == 'parsec_v1p2':
            self.load_parsecv1p2_tracks()
        elif track_type.lower() in ['mist', 'mist_v1p2']:
            self.load_mistv1p2_tracks()
        elif track_type.lower() in ['siess2000']:
            self.load_siess2000_tracks()
        elif track_type.lower() in ['spots0000']:
            self.load_spots0000_tracks()
        elif track_type.lower() in ['spots0169']:
            self.load_spots0169_tracks()
        elif track_type.lower() in ['spots0339']:
            self.load_spots0339_tracks()
        elif track_type.lower() in ['spots0508']:
            self.load_spots0508_tracks()
        elif track_type.lower() in ['spots0847']:
            self.load_spots0847_tracks()
        elif track_type.lower() in ['pisa']:
            self.load_pisa_tracks()
        elif track_type.lower() == 'customize':
            self.load_tracks_from_customize_matrix(load_file)
        else:
            # raise ValueError("Invalid track type. Please choose from available tracks: 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'parsec_v1p2', 'parsec_v2p0', 'mist_v1p2', 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847'.")
            
            model = str(track_type)
            # raise ValueError(f"Invalid model: {model}. Please choose from 'Baraffe2015', 'Feiden2016', 'Feiden2016_magnetic', 'PARSEC_v2p0' (same as 'PARSEC'), 'PARSEC_v1p2',  'MIST_v1p2' (same as 'MIST'), 'siess2000', 'spots0169', 'spots0339', 'spots0508', 'spots0847', 'pisa', or 'customize'. If you want to use the model = 'customize', you need to provide the absolute directory for the isochrone matrix file isochrone_mat_file. See user manual for how to set up your own isochrone matrix.")
            
            raise ValueError(registry.invalid_track_message(model)) from e
        
        return 1
    
    def set_tracks(self, track_type, load_file='', verbose=False):
        """
        Set the isochrone tracks based on track_type.

        Args:
        
            track_type: [str]
                Type of the tracks to use ('baraffe2015' or 'feiden2016' or 'customize').
            load_file: [str]
                the .mat file that contains mass grid, log_age grid, and logt_logl grid
                Default is '', so if you want to read in the customized datafile, 
                remember to set up this parameter
            verbose: [bool]
                If True, print additional information during track loading. Default is False.

        Output:
        
            Loads the corresponding track (Baraffe or Feiden) and sets the appropriate attributes.
        """
        canonical = registry.normalize_track_name(track_type)

        # Map canonical names -> loader methods
        loaders = {
            "baraffe2015": self.load_baraffe2015_tracks,
            "feiden2016": self.load_feiden2016_tracks,
            "feiden2016_magnetic": self.load_feiden2016_magnetic_tracks,
            "parsec_v2p0": self.load_parsecv2p0_tracks,
            "parsec_v1p2": self.load_parsecv1p2_tracks,
            "mist_v1p2": self.load_mistv1p2_tracks,
            "siess2000": self.load_siess2000_tracks,
            "spots0169": self.load_spots0169_tracks,
            "spots0339": self.load_spots0339_tracks,
            "spots0508": self.load_spots0508_tracks,
            "spots0847": self.load_spots0847_tracks,
            "pisa": self.load_pisa_tracks,
            # customize handled below
        }

        if canonical == "customize":
            if not load_file:
                # standardized message + extra hint
                raise ValueError(
                    registry.invalid_track_message(track_type)
                    + " (You did not pass load_file=...)"
                )
            self.load_tracks_from_customize_matrix(load_file)
            if verbose:
                print("Using the user-specified isochrone matrix of")
                print(f"{load_file}")
            return 1

        # dispatch
        try:
            loaders[canonical]()
            if verbose:
                print(f"Isochrone tracks set to '{canonical}'.")
        except KeyError:
            # Should never happen if registry + loaders stay consistent,
            # but gives a clean error if you forget to add a loader.
            raise RuntimeError(
                f"Track '{canonical}' is registered but has no loader in Isochrone.set_tracks(). "
                "Add it to the loaders dict."
            )

        return 1

    def get_tracks(self):
        """
        Get the current isochrone tracks (log_age, masses, logtlogl).

        Output:
        
        Returns:
        
        log_age: [array]
            Array of log(age) values.
        masses: [array]
            Array of mass values.
        logtlogl: [array]
            Array of log(T) and log(L) values.
        """
        return self.log_age, self.masses, self.logtlogl
