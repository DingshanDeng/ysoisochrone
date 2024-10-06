import os
import scipy.io
# from scipy.interpolate import griddata
from ysoisochrone import utils

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
        self.data_dir = data_dir if data_dir else os.path.join(os.getcwd(), 'isochrones_data')
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
        
        input_file = os.path.join(self.data_dir, 'Baraffe_AgeMassGrid_YSO_matrix.mat')
        # Check if the original Baraffe 2015 data file exists, download if necessary
        if not os.path.exists(input_file):
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
        
        input_file = os.path.join(self.data_dir, 'Feiden_AgeMassGrid_YSO_matrix.mat')
        # Check if the original Feiden 2016 data file exists, download if necessary
        if not os.path.exists(input_file):
            self.prepare_feiden_tracks()
            
        data = scipy.io.loadmat(input_file)
        
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
        
        self.masses = data['mass'][0]
        self.log_age = data['log_age'][0]
        self.logtlogl = data['logt_logl']
        
        return 1

    def set_tracks(self, track_type, load_file=''):
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
        elif track_type.lower() == 'feiden2016':
            self.load_feiden2016_tracks()
        elif track_type.lower() in ['parsec', 'parsec_v2p0']:
            self.load_parsecv2p0_tracks()
        elif track_type.lower() == 'parsec_v1p2':
            self.load_parsecv1p2_tracks()
        elif track_type.lower() in ['mist', 'mist_v1p2']:
            self.load_mistv1p2_tracks()
        elif track_type.lower() == 'customize':
            self.load_tracks_from_customize_matrix(load_file)
        else:
            raise ValueError("Invalid track type. Please choose either 'Baraffe2015' or 'Feiden2016'.")
        
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
