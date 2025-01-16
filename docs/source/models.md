# The available stellar evolutionary models

The young stellar objects (pre-main-sequence) evolutionary tracks mainly include the ones from the following works.
The code can download and format the stellar evolutionary tracks from public repositories and websites. 
Customized stellar evolutionary tracks can also be used, but they need to be formatted to the required matrix format by the user (see [use your own isochrone](./notebooks/ysoisochrone_customize_isochrone.ipynb) for more details).

For the moment being, this package is meant to be used to study young stellar objects. In other words, it only utilizes the stellar evolutionary tracks for pre-main-sequence stars, avoiding the problem of dealing with main-sequence and post-main-sequence targets (whose luminosity rises again and will overlay on the pre-main-sequence phase). 
This method could also be expanded to use on the main-sequence stars (e.g., [Fernandes et al. 2023](https://ui.adsabs.harvard.edu/abs/2023AJ....166..175F/abstract)), but user-specified customized stellar evolutionary tracks are needed for now, and this function will be included in the future releases.

## Baraffe et al. (2015)
Models from Baraffe, Homeier, Allard, Chabrier 2015, A&A,577, 42 *New evolutionary models for pre-main sequence and main sequence low-mass stars down to the hydrogen-burning limit*.

ADS webpage: https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract

Data are downloaded from http://perso.ens-lyon.fr/isabelle.baraffe/BHAC15dir/

## Feiden (2016)
Models from Feiden 2016, Astronomy & Astrophysics, Volume 593, id.A99, 11 pp. *Magnetic inhibition of convection and the fundamental properties of low-mass stars. III. A consistent 10 Myr age for the Upper Scorpius OB association*.

ADS webpage: https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract

Data are downloaded from https://github.com/gfeiden/MagneticUpperSco/?tab=readme-ov-file

By default, we use the standard nonmagnetic tracks that are in the public repo from here: https://github.com/gfeiden/MagneticUpperSco/tree/master/models/trk/std

**Caution**: There are known issues with model isochrones at very young ages (below 10 Myr). Proceed with caution. Updated models that rectify known issues are available from the author. 

See the GitHub page from the author: https://github.com/gfeiden/MagneticUpperSco/?tab=readme-ov-file

## PARSEC
The **PA**dova T**R**ieste **S**tellar **E**volutionary **C**ode. 
See their website for details and references: http://stev.oapd.inaf.it/PARSEC/index.html

We provide the option to use their newest version 2.0, and legacy version 1.2 tracks. 
By default, we adopt the tracks with solar metallicity, and do not include rotations.

## MIST

**NOTE** The `MIST` model feature is still under development.

**M**ESA **I**sochrones & **S**tellar **T**racks.
The MIST stellar evolutionary tracks are computed with the [Modules for Experiments in Stellar Astrophysics (MESA)](http://mesa.sourceforge.net/index.html).

See their website for details and references: https://waps.cfa.harvard.edu/MIST/.

> There is also another Python package [isochrones](https://github.com/timothydmorton/isochrones/tree/master), that is capable of handling all the MIST isochrones.
> 
> We also refer the users to the Python package [`MADYS`](https://madys.readthedocs.io/en/latest/), which can handle MIST, PARSEC (1.2 and 2.0), Feiden, Baraffe and many other models for pre-MS or MS stars, and can be used to derive stellar age and mass using extinction corrected multi-wavelengths photometric data.
