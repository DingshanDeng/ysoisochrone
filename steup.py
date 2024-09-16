from setuptools import setup, find_packages

setup(
    name='ysoisochrone',
    version='0.1.0.alpha',
    description='Python package for Bayesian inference of stellar ages and masses from evolutionary tracks',
    author='Dingshan Deng',
    author_email='dingshandeng@arizona.edu',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'astropy',
        'requests',
        'tarfile',
        'zipfile',
        're',
        'tqdm',
    ],
)
