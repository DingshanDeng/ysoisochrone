from setuptools import setup, find_packages

setup(
    name='ysoisochrone',
    version='0.4.1.beta',
    description='Python package handles the young-stellar-objects isochrones, and one primary goal is to derive the stellar mass and ages from the isochrones.',
    author='Dingshan Deng',
    author_email='dingshandeng@arizona.edu',
    url="https://github.com/DingshanDeng/ysoisochrone",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'numpy',
        'pandas',
        "matplotlib>=3.3.4",
        'scipy',
        'requests',
        'tqdm',
        'jupyter',
        'pytest',
    ],
)
