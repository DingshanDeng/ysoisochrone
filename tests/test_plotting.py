#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dingshan Deng @ University of Arizona
# contact: dingshandeng@arizona.edu
# created: 01/14/2025

import pytest
import matplotlib
matplotlib.use("Agg") # Use a non-interactive backend for testing
import matplotlib.pyplot as plt
import numpy as np
from ysoisochrone.plotting import plot_bayesian_results

def test_plot_bayesian_results(monkeypatch):
    def mock_plot(*args, **kwargs):
        pass

    # Apply the mock to matplotlib.pyplot.savefig
    monkeypatch.setattr(plt, "savefig", mock_plot)

    # Call the function (replace ... with actual arguments)
    # # assert plot_bayesian_results(...) is None # the simple way does not work
    try:
        plot_bayesian_results(
            log_age_dummy=np.array([6, 7, 8]),
            log_masses_dummy=np.array([-1, 0, 1]),
            L=np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]),
            best_age=7,
            best_mass=0,
            age_unc=np.array([6.8, 7.2]),
            mass_unc=np.array([-0.1, 0.1]),
            source="TestStar",
            save_fig=True,
            fig_save_dir=".",
            customized_fig_name="test_plot.png",
        )
    except AttributeError as e:
        pytest.fail(f"plot_bayesian_results raised AttributeError: {e}")
        