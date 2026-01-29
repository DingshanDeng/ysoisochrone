# The available stellar evolutionary models

The young stellar objects (pre-main-sequence) evolutionary tracks mainly include the ones from the following works.
The code can download and format the stellar evolutionary tracks from public repositories and websites. 
Customized stellar evolutionary tracks can also be used, but they need to be formatted to the required matrix format by the user (see [use your own isochrone](./notebooks/ysoisochrone_customize_isochrone.ipynb) for more details).

For the moment being, this package is meant to be used to study young stellar objects. In other words, it only utilizes the stellar evolutionary tracks for pre-main-sequence stars, avoiding the problem of dealing with main-sequence and post-main-sequence targets (whose luminosity rises again and will overlay on the pre-main-sequence phase). 
This method could also be expanded to use on the main-sequence stars (e.g., [Fernandes et al. 2023](https://ui.adsabs.harvard.edu/abs/2023AJ....166..175F/abstract)), but user-specified customized stellar evolutionary tracks are needed for now, and this function will be included in the future releases.

**To call the models, use the keyword defined here in the `ysoisochrone` package**

## Baraffe et al. (2015)

keyword: `baraffe2015`

Models from Baraffe, Homeier, Allard, Chabrier 2015, A&A,577, 42 *New evolutionary models for pre-main sequence and main sequence low-mass stars down to the hydrogen-burning limit*.

ADS webpage: https://ui.adsabs.harvard.edu/abs/2015A%26A...577A..42B/abstract

Data are downloaded from http://perso.ens-lyon.fr/isabelle.baraffe/BHAC15dir/

## Feiden (2016)

keyword: `feiden2016` or `feiden2016_nonmagnetic` for non-magnetic tracks; `feiden2016_magnetic` for magnetic tracks.

Models from Feiden 2016, Astronomy & Astrophysics, Volume 593, id.A99, 11 pp. *Magnetic inhibition of convection and the fundamental properties of low-mass stars. III. A consistent 10 Myr age for the Upper Scorpius OB association*.

ADS webpage: https://ui.adsabs.harvard.edu/abs/2016A%26A...593A..99F/abstract

Data are downloaded from https://github.com/gfeiden/MagneticUpperSco/?tab=readme-ov-file

By default, we use the **nonmagnetic** tracks that are in the public repo from here: https://github.com/gfeiden/MagneticUpperSco/tree/master/models/trk/std

**NOTE**: in the updated version (v1.1+), the magnetic tracks are also added.  

**Caution**: There are known issues with model isochrones at very young ages (below 10 Myr). Proceed with caution. Updated models that rectify known issues are available from the author. 

See the GitHub page from the author: https://github.com/gfeiden/MagneticUpperSco/?tab=readme-ov-file

## PARSEC

keyword: `parsec` or `parsec_v2p0` for PARSEC v2.0; `parsec_v1p2` for PARSEC v1.2.

The **PA**dova T**R**ieste **S**tellar **E**volutionary **C**ode. 
See their website for details and references: http://stev.oapd.inaf.it/PARSEC/index.html

We provide the option to use their newest version 2.0, and legacy version 1.2 tracks. 
By default, we adopt the tracks with solar metallicity, and do not include rotations.

## MIST

keyword: `mist` or `mist_v1p2` for MIST v1.2.

**NOTE** The `MIST` model feature is still under development.

**M**ESA **I**sochrones & **S**tellar **T**racks.
The MIST stellar evolutionary tracks are computed with the [Modules for Experiments in Stellar Astrophysics (MESA)](http://mesa.sourceforge.net/index.html).

See their website for details and references: https://waps.cfa.harvard.edu/MIST/.

## Siess et al. (2000)

keyword: `siess2000`

A classical pre-main sequence tracks for low- and intermediate-mass stars presented in [Siess et al. (2000)](https://ui.adsabs.harvard.edu/abs/2000A%26A...358..593S/abstract).

## SPOTS

keyword: `spots0169`, `spots0339`, `spots0508`, and `spots0847` for SPOTS model with different spot coverages (16.9%, 33.9%, 50.8%, 84.7%).

SPOTS Tracks with different cold photospheric spot coverages [(Somers et al. 2020)](https://ui.adsabs.harvard.edu/abs/2020ApJ...891...29S/abstract).

## Pisa

keyword: `pisa`

See the paper on ads [Tognelli et al. 2011](https://scixplorer.org/abs/2011A%26A...533A.109T/abstract).

## Useful Links

> There is also another Python package [isochrones](https://github.com/timothydmorton/isochrones/tree/master), that is capable of handling all the MIST isochrones.
> 
> We also refer the users to the Python package [`MADYS`](https://madys.readthedocs.io/en/latest/), which can handle MIST, PARSEC (1.2 and 2.0), Feiden, Baraffe and many other models for pre-MS or MS stars, and can be used to derive stellar age and mass using multi-wavelengths photometric data with extinction corrected according to extinction maps and laws.
