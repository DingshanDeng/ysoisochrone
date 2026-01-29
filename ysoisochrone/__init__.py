"""
 ysoisochrone v1.1.1
 Dingshan Deng, Sep 2024 - Jan 2026
"""

# from . import constants
# from . import wrapper_model_parameters
# from . import wrapper_disk_density

from . import bayesian
from . import utils
from . import plotting
from . import isochrone
from . import registry

# __version__ = "1.1.1"
# the new version is now in pyproject.toml and automatically handled by setuptools
try:
    from importlib.metadata import version as _version
    __version__ = _version("ysoisochrone")
except Exception:
    __version__ = "unknown"

__author__ = "Dingshan Deng"
__copyright__ = "Copyright (C) 2024 Dingshan Deng"
__all__ = ["isochrone", "bayesian", "plotting", "utils", "registry"]
