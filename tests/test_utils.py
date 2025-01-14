#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/14/2025

import pytest
import requests
from ysoisochrone.utils import download_baraffe_tracks, read_baraffe_file

def test_download_n_read_baraffe_tracks(monkeypatch, tmpdir):
    """Test download_baraffe_tracks with mocked requests.get."""
    
    # Create a mock response object
    class MockResponse:
        def __init__(self, content, headers, status_code=200):
            self.content = content
            self.headers = headers
            self.status_code = status_code

        def iter_content(self, chunk_size=1):
            yield self.content

    # Mock requests.get to return a MockResponse
    def mock_get(url, stream=False):
        assert url == "http://perso.ens-lyon.fr/isabelle.baraffe/BHAC15dir/BHAC15_tracks+structure", "Unexpected URL in request."
        return MockResponse(b"mock file content", {"Content-Type": "application/octet-stream"})

    # Apply the monkeypatch
    monkeypatch.setattr(requests, "get", mock_get)

    # Temporary directory for saving the file
    save_dir = tmpdir.mkdir("mock_isochrones_data")

    # Call the function
    result = download_baraffe_tracks(save_dir=str(save_dir))

    # Verify that the file is created
    expected_file = save_dir.join("Baraffe2015", "BHAC15_tracks+structure")
    assert expected_file.exists(), "File was not saved correctly."

# NOTE read file is tested in the test_isochrone
# def test_read_baraffe_file(monkeypatch):
#     """Test read_baraffe_file with mocked file I/O."""
    
#     # Mock the file reading behavior
#     def mock_read_baraffe_file(file_path):
#         assert file_path == "mock_file", "Unexpected file path."
#         return {"mock_key": "mock_value"}  # Simulated data

#     # Apply the monkeypatch
#     monkeypatch.setattr("ysoisochrone.utils.read_baraffe_file", mock_read_baraffe_file)

#     # Call the function
#     result = read_baraffe_file("mock_file")
#     assert result == {"mock_key": "mock_value"}, "Unexpected result from read_baraffe_file."
