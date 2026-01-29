from setuptools import setup, find_packages

setup()

# # the new setup and metadata are now in pyproject.toml and automatically handled by setuptools
# # Previous setup.py content (now commented out)
# setup(
#     name='ysoisochrone',
#     version='1.1.1',
#     description='Python package handles the young-stellar-objects isochrones, and one primary goal is to derive the stellar mass and ages from the isochrones.',
#     author='Dingshan Deng',
#     author_email='dingshandeng@arizona.edu',
#     url="https://github.com/DingshanDeng/ysoisochrone",
#     packages=find_packages(),
#     # >>> NEW: include data files inside the package <<<
#     include_package_data=True,
#     package_data={
#         # This assumes ysoisochrone/data/*.mat
#         "ysoisochrone": ["data/*.mat"],
#     },
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#     ],
#     install_requires=[
#         'numpy',
#         'pandas',
#         "matplotlib>=3.3.4",
#         'scipy',
#         'requests',
#         'tqdm',
#         'jupyter',
#         'pytest',
#     ],
# )
