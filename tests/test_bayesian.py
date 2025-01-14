#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/14/2025

import pytest
import os
import numpy as np
import pandas as pd
from ysoisochrone.bayesian import bayesian_mass_age, derive_stellar_mass_age

# Mock inputs for testing
log_age_dummy = np.linspace(6, 8, 10)  # log(age) from 1 Myr to 10 Myr
log_masses_dummy = np.linspace(np.log10(0.5), np.log10(3), 10)  # log(mass) from 0.5 to 3 Msun
# Define a 2D Gaussian likelihood centered at a specific point
center_logage, center_logmass = 7.0, 0.0  # Center of the Gaussian
L = np.exp(
    -0.5 * (((log_age_dummy[:, None] - center_logage) / 0.2) ** 2
            + ((log_masses_dummy[None, :] - center_logmass) / 0.1) ** 2)
)

def test_bayesian_mass_age():
    """Test the bayesian_mass_age function."""
    # Run the function with mock data
    result, logage_likelihood, logmass_likelihood = bayesian_mass_age(
        log_age_dummy, log_masses_dummy, L, confidence_interval=0.68
    )
    
    # Check that the result structure is correct
    assert len(result) == 4, "Result should contain 4 elements (best age, age_unc, best mass, mass_unc)."
    assert isinstance(logage_likelihood, np.ndarray), "Log-age likelihood should be a NumPy array."
    assert isinstance(logmass_likelihood, np.ndarray), "Log-mass likelihood should be a NumPy array."
    
    # Check that the likelihoods are normalized
    assert np.isclose(np.trapz(logage_likelihood[1], logage_likelihood[0]), 1), "Log-age likelihood should be normalized."
    assert np.isclose(np.trapz(logmass_likelihood[1], logmass_likelihood[0]), 1), "Log-mass likelihood should be normalized."

def test_bayesian_mass_age_edge_cases():
    """Test bayesian_mass_age with edge cases."""
    # Case: Likelihood grid is zero
    L_zero = np.zeros((10, 10))
    with pytest.raises(ValueError):
        bayesian_mass_age(log_age_dummy, log_masses_dummy, L_zero)

def test_invalid_inputs():
    """Test functions with invalid inputs."""
    # Test invalid grid sizes
    # invalid_L = np.random.random((10, 10))
    
    center_logage, center_logmass = 5.0, 0.0  # Center of the Gaussian
    invalid_L = np.exp(
        -0.5 * (((log_age_dummy[:, None] - center_logage) / 0.2) ** 2
                + ((log_masses_dummy[None, :] - center_logmass) / 0.1) ** 2)
    )
    
    with pytest.raises(ValueError):
        bayesian_mass_age(log_age_dummy, log_masses_dummy, invalid_L)

# def test_derive_stellar_mass_age():
#     """Test the derive_stellar_mass_age function."""
#     # Create mock input DataFrame
#     df_mock = pd.DataFrame({
#         "Source": ["Star1", "Star2"],
#         "Teff[K]": [3632, 4060],
#         "e_Teff[K]": [100, 100],
#         "Luminosity[Lsun]": [0.33, 0.43],
#         "e_Luminosity[Lsun]": [0.1, 0.1],
#     })

#     mock_data_dir = os.path.join('tests', 'mock_dir')
    
#     # Call the function
#     best_mass, best_age, _, _ = derive_stellar_mass_age(
#         df_mock, model="Baraffe_n_Feiden", isochrone_data_dir=mock_data_dir, no_uncertainties=True
#     )
    
#     # Check outputs
#     assert best_mass.shape == (2, 3), "Best mass output should have shape (2, 3) for two stars."
#     assert best_age.shape == (2, 3), "Best age output should have shape (2, 3) for two stars."
