#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/14/2025

import os
import pytest
from ysoisochrone.isochrone import Isochrone

@pytest.fixture
def isochrone():
    return Isochrone(data_dir="mock_data")

def test_isochrone_initialization(isochrone):
    assert isochrone.data_dir == "mock_data"
    assert isochrone.log_age is None
    assert isochrone.masses is None
    assert isochrone.logtlogl is None

def test_prepare_baraffe_tracks(isochrone, monkeypatch):
    """Test the prepare_baraffe_tracks method."""
    mock_data_dir = "mock_data"
    mock_input_file = os.path.join(mock_data_dir, "Baraffe2015", "BHAC15_tracks+structure")

    # Mock the os.path.exists to simulate file existence
    def mock_exists(path):
        if path == mock_input_file:
            return True  # Simulate that the input file already exists
        return False

    # Mock utility functions
    def mock_read_baraffe_file(file_path):
        assert file_path == mock_input_file, "Incorrect file path passed to read_baraffe_file."
        return {"data": "mock_data"}

    def mock_create_meshgrid(data):
        assert data == {"data": "mock_data"}, "Incorrect data passed to create_meshgrid."
        return [[], [], [], [], []]  # Mocked meshgrid result

    def mock_save_as_mat(masses, log_ages, grid, output_path):
        assert "Baraffe_AgeMassGrid_YSO_matrix.mat" in output_path, "Incorrect output file name."

    # Monkeypatch the utility functions and os.path.exists
    monkeypatch.setattr(os.path, "exists", mock_exists)
    monkeypatch.setattr("ysoisochrone.utils.read_baraffe_file", mock_read_baraffe_file)
    monkeypatch.setattr("ysoisochrone.utils.create_meshgrid", mock_create_meshgrid)
    monkeypatch.setattr("ysoisochrone.utils.save_as_mat", mock_save_as_mat)

    # Call the method
    result = isochrone.prepare_baraffe_tracks()
    assert result == 1, "prepare_baraffe_tracks did not return 1."
    
