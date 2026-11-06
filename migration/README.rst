
Johnson et al. (2021) Models
++++++++++++++++++++++++++++

|johnson2021| |apogeedr16| |feuillet2018| |feuillet2019| |vincenzo2021|

Here we provide instructions for running the Johnson et al. (2021) chemical
evolution models for the Milky Way disk, producing the figures which appear in
the corresponding paper, and accessing the observational sample used in the
comparison. The instructions herein assume that you as the user are already
familiar with the nature of the Johnson et al. (2021) models; this information
can be found in the associated journal publication.

.. 	|johnson2021| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20et%20al.%20(2021)-red
	:target: https://ui.adsabs.harvard.edu/abs/2021arXiv210309838J/abstract
	:alt: Johnson et al. (2021)

.. 	|apogeedr16| image:: https://img.shields.io/badge/NASA%20ADS-APOGEE%20DR16-red
	:target: apogeedr16_
	:alt: Ahumada et al. (2020)

.. 	|feuillet2018| image:: https://img.shields.io/badge/NASA%20ADS-Feuillet%20et%20al.%20(2018)-red
	:target: feuillet2018_
	:alt: Feuillet et al. (2018)

.. 	|feuillet2019| image:: https://img.shields.io/badge/NASA%20ADS-Feuillet%20et%20al.%20(2019)-red
	:target: feuillet2019_
	:alt: Feuillet et al. (2019)

.. 	|vincenzo2021| image:: https://img.shields.io/badge/NASA%20ADS-Vincenzo%20et%20al.%20(2021)-red
	:target: vincenzo2021_
	:alt: Vincenzo et al. (2021)

.. _feuillet2018: https://ui.adsabs.harvard.edu/abs/2018MNRAS.477.2326F/abstract
.. _feuillet2019: https://ui.adsabs.harvard.edu/abs/2019MNRAS.489.1742F/abstract
.. _apogeedr16: https://ui.adsabs.harvard.edu/abs/2020ApJS..249....3A/abstract
.. _vincenzo2021: https://ui.adsabs.harvard.edu/abs/2021arXiv210104488V/abstract

.. Contents::


Requirements
============
To run these models, you must first `install VICE`__ version 1.2.0 or greater.
Unless you wish to modify VICE's source code to run some alternate
version of these models, you can achieve this with a simple ``pip install vice``
command in a ``Unix`` terminal. VICE 1.2.0 is the earliest version that
includes the necessary functionality with which to handle stellar migration.
In turn, VICE 1.2.0 requires Python >= 3.6.0, but subsequent versions require
later versions of Python.

__ install_
.. _install: https://vice-astro.readthedocs.io/en/latest/install.html

Once these requirements are satisfied, even if you installed VICE via ``pip``,
you'll need a local copy of the code base for the Johnson et al. (2021) models.
If you haven't done so already, using a ``Unix`` terminal, navigate to the
directory you'd like the code to live, and run the following set of commands:

::

	$ git clone https://github.com/giganano/VICE.git
	$ cd VICE/migration/

Unless you'd like to modify the parameters of the models, you can run them from
this directory in your terminal on your personal computer without modifying
the source code. No cluster computing necessary!

Although VICE itself has no runtime dependencies, the code base for the
Johnson et al. (2021) models requires matplotlib_ >= 2.0.0 and
NumPy_ >= 1.17.0.

.. _matplotlib: https://pypi.org/project/matplotlib/
.. _NumPy: https://pypi.org/project/numpy/


Maximum Number of Open File Descriptors
---------------------------------------
Computers enforce a limit on the number of open file descriptors at one
time by a single application; VICE will open two file descriptors per ring in
the Johnson et al. (2021) models, plus one for the abundances of individual
stellar populations.
With sufficiently narrow rings, the user may exceed their system's limit for
the number of simultaneously open files. To view the current limit of your
system, run the following line in your ``Unix`` terminal:

::

	$ ulimit -n

The default number varies from system to system; on Mac OS X, it is 256, and
it's 1024 on some Linux distributions.
With a limit of ``n``, the user can run a model with at most ``n/2 - 1`` annuli
without producing a system error. If necessary, you can modify these limits
using ``launchctl`` on Mac OS X and ``sysctl`` on Linux operating systems.
These commands are used to configure kernel parameters at runtime, and must be
ran as ``root``; as such, doing so requires ``admin`` privileges over your
computer.
If you do not have such capabilities and need to increase this limit for your
research, you'll need to speak with your administrator about increasing the
maximum number of open file descriptors on your system.

To increase the maximum number of open file descriptors on Mac OS X, run the
following set of lines:

::
	
	$ sudo launchctl limit maxfiles <N>
	$ ulimit -n <N>

where ``<N>`` should be replaced with a number more than twice as large as the
number of rings you intend on using in the model. If your administrator has
increased your limit, you should only run the second line; the presence of a
``sudo`` command will produce a ``permission denied`` error if you do. If you
are the administrator, however, the first line is necessary for the second to
work, and you'll need to enter your password if you haven't ran a ``sudo``
command in your current terminal session yet. Lastly, double check that this
procedure ran properly by re-running ``ulimit -n``, and now your terminal
should display the updated maximum.

To increase the maximum number of open file descriptors on Linux, the same
concepts as the Mac OS X procedure apply, but with slightly different syntax:

::

	$ sudo sysctl -w fs.file-max=<N>
	$ ulimit -n <N>

where ``<N>`` should again be replaced with a number more than twice as large
as the number of annuli you intend on using in the model.

Recommended: Screen Sessions
----------------------------
If you haven't used the ``screen`` command before, it is a utility which allows
you to create a new terminal session from within your current one, then
subsequently detach from it while some process with a long CPU-time may be
running.  Many systems now come with ``screen`` pre-installed;
to check if it is, simply run ``screen --help``. On Mac OS X, ``screen`` can be
installed easily with Homebrew_ via ``brew install screen``. On Linux, ``admin``
privileges are necessary. If you are not the administrator of your system, you
should speak with them about installing ``screen``. If you are the
administrator, it can be installed with one of the following lines, depending
on which distribution you're using:

::

	$ sudo yum install screen # CentOS
	$ sudo apt-get install screen # Ubuntu
	$ sudo pacman -Sy screen # Manjaro
	$ sudo dnf install screen # Fedora

.. _Homebrew: https://brew.sh/

To start a ``screen`` session, run ``screen -S [name]``, and give your new
session some name descriptive of its purpose; to then detach from the
session, simply press ``Ctrl+A`` followed by ``Ctrl+D``. To reattach to a
previous session, run ``screen -r [name]``. Terminating a ``screen`` session
can be done by simply running ``exit`` from within the session, or killing the
process using the ``screen`` session's ``pid``.

Runnings the Models
===================
Before running the Johnson et al. (2021) models, you should ensure that you've
satisfied all `Requirements`_, particularly the
`Maximum Number of Open File Descriptors`_.

Unless you'd like to modify the source code for the models, they can all
be ran via the ``simulations.py`` script in this directory.
Running ``python simulations.py --help`` produces the following help message
regarding the parameters which can be specified at runtime:

::

	$ python simulations.py --help

	usage: simulations.py [-h] [-f] [--migration MIGRATION]
	                      [--evolution EVOLUTION] [--dt DT] [--nstars NSTARS]
	                      [--name NAME] [--elements ELEMENTS]
	                      [--zonewidth ZONEWIDTH]

	The parameters of the Milky Way models to run.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f, --force           Force overwrite existing VICE outputs of the same
	                        name.
	  --migration MIGRATION
	                        The migration model to assume. (Default: diffusion)
	  --evolution EVOLUTION
	                        The evolutionary history to assume (Default:
	                        insideout)
	  --dt DT               Timestep size in Gyr. (Default: 0.01)
	  --nstars NSTARS       Number of stellar populations per zone per timestep.
	                        (Default: 2)
	  --name NAME           The name of the output simulations (Default:
	                        'milkway')
	  --elements ELEMENTS   Elements to simulation the enrichment for separated
	                        by underscores. (Default: "fe_o")
	  --zonewidth ZONEWIDTH
	                        The width of each annulus in kpc. (Default: 0.1)

If you're rerunning a number of models whose outputs have already been
produced, you should use the ``-f`` or ``--force`` commands so that VICE
doesn't stop and ask you for permission to overwrite your files. Below is a
table of the allowed values for each parameter:

+----------------------------+----------------------------+
| Parameter                  | Allowed Values             |
+============================+============================+
| migration                  | Must be a string.          |
|                            | "diffusion",               |
|                            | "linear", "sudden", or     |
|                            | "post-process"             |
+----------------------------+----------------------------+
| evolution                  | Must be a string.          |
|                            | "static", "insideout",     |
|                            | "lateburst", or            |
|                            | "outerburst". "static"     |
|                            | corresponds to a constant  |
|                            | star formation rate.       |
+----------------------------+----------------------------+
| dt                         | Must be a float. Must be   |
|                            | positive.                  |
+----------------------------+----------------------------+
| nstars                     | Must be an integer. Must   |
|                            | be positive.               |
+----------------------------+----------------------------+
| name                       | Must be a string. Must be  |
|                            | a valid relative or        |
|                            | absolute path              |
|                            | (e.g. "./outputs/mymodel") |
+----------------------------+----------------------------+
| elements                   | Must be a string. Must be  |
|                            | the one or two character   |
|                            | symbols of chemical        |
|                            | elements as they appear on |
|                            | the periodic table         |
|                            | separated by underscores   |
|                            | (e.g. "c_n_o", "fe_mg_n")  |
+----------------------------+----------------------------+
| zone_width                 | Must be a float. Must be   |
|                            | positive.                  |
+----------------------------+----------------------------+

Mathematical definitions of the recognized models for the ``migration`` and
``evolution`` parameters can be found in the Johnson et al. (2021) paper. The
Johnson et al. (2021) models as they appear in the paper should be ran with the
following set of commands:

::

	$ mkdir outputs
	$ mkdir outputs/diffusion
	$ mkdir outputs/linear
	$ mkdir outputs/sudden
	$ mkdir outputs/post-processing
	$ python simulations.py -f --nstars=8 --name=./outputs/diffusion/insideout
	$ python simulations.py -f --nstars=8 --evolution=static --name=./outputs/diffusion/static
	$ python simulations.py -f --nstars=8 --evolution=lateburst --name=./outputs/diffusion/lateburst
	$ python simulations.py -f --nstars=8 --evolution=outerburst --name=./outputs/diffusion/outerburst
	$ python simulations.py -f --nstars=8 --migration=linear --name=./outputs/linear/insideout
	$ python simulations.py -f --nstars=8 --migration=sudden --name=./outputs/sudden/insideout
	$ python simulations.py -f --nstars=8 --migration=post-process --name=./outputs/post-process/insideout

**Note**: These models are computationally expensive. At any given moment
during the integration, they can require up to ~3 GB of RAM each.
Users running these models on systems which would be strained by such demand
should therefore run lower resolution versions by specifying lower numbers to
``nstars`` and larger numbers to ``zonewidth``.

If your system has adequate space to do so, each individual call to
``simulations.py`` can be ran separately in a ``screen`` session following a
single run of each of the ``mkdir`` commands above.


Producing the Figures
=====================
All of the figures in Johnson et al. (2021) can be produced via the
``figures.py`` script. Running ``python figures.py --help`` produces the
following help message:

::

	$ python figures.py --help

	usage: figures.py [-h] [--fig1] [--fig2] [--fig3] [--fig4] [--fig5] [--fig6]
	                  [--fig7] [--fig8] [--fig9] [--fig10] [--fig11] [--fig12]
	                  [--fig13a] [--fig13b] [--fig14] [--fig15] [--fig16]
	                  [--fig17] [--fig18]

	Produce the figures in Johnson et al. (2021).

	optional arguments:
	  -h, --help  show this help message and exit
	  --fig1      Produce Fig. 1.
	  --fig2      Produce Fig. 2.
	  --fig3      Produce Fig. 3.
	  --fig4      Produce Fig. 4.
	  --fig5      Produce Fig. 5.
	  --fig6      Produce Fig. 6.
	  --fig7      Produce Fig. 7.
	  --fig8      Produce Fig. 8.
	  --fig9      Produce Fig. 9.
	  --fig10     Produce Fig. 10.
	  --fig11     Produce Fig. 11.
	  --fig12     Produce Fig. 12.
	  --fig13a    Produce Fig. 13a.
	  --fig13b    Produce Fig. 13b.
	  --fig14     Produce Fig. 14.
	  --fig15     Produce Fig. 15.
	  --fig16     Produce Fig. 16.
	  --fig17     Produce Fig. 17.
	  --fig18     Produce Fig. 18.

These parameters simply tell the script which figure(s) you'd like produced.
For example, ``python figures.py --fig9`` will produce only Fig. 9 of
Johnson et al. (2021), where as ``python figures.py --fig9 --fig10`` will
produces Figs. 9 and 10.
This script saves figures here under a directory named ``figures``; users
should therefore be careful to run ``mkdir figures`` prior to running
the ``figures.py`` script.

**WARNING**: In order for this script to work properly, the outputs of each of
the Johnson et al. (2021) models need to be at the following locations:

| ``./outputs/diffusion/static``
| ``./outputs/diffusion/insideout``
| ``./outputs/diffusion/lateburst``
| ``./outputs/diffusion/outerburst``
| ``./outputs/linear/insideout``
| ``./outputs/sudden/insideout``
| ``./outputs/post-process/insideout``

where the directory names simply specify the stellar migration and star
formation history of the model, respectively. If the outputs are not in these
locations, it's likely the ``figures.py`` script will produce an error message
stating that an output is not found.


Accessing the Observational Sample
==================================
Johnson et al. (2021) made use of observational data from
`Feuillet et al. (2018)`__, `Feuillet et al. (2019)`__, and
`Vincenzo et al. (2021)`__ as well as the 16th data release of the Apache
Point Observatory Galaxy Evolution Experiment (APOGEE; `Ahumada et al. 2020`__).

__ feuillet2018_
__ feuillet2019_
__ vincenzo2021_
__ apogeedr16_

APOGEE DR16
-----------

|apogeedr16|

The sample of stars from APOGEE DR16 employed in the Johnson et al. (2021)
comparison can be found at ``./data/dr16stars.dat``. This is a plain ascii
text file containing APOGEE IDs, an identifier tagging stars as either high- or
low-alpha sequence, [Mg/H], [O/H], [Fe/H], [Mg/Fe], effective temperatures,
surface gravities, galactocentric radii in kpc, height above the disk midplane
in kpc, and signal-to-noise ratios for each star that passes the following
cuts:

	- Effective temperatures between 4000 and 4600 K
	- Surface gravities (log g) between 1.0 and 2.5
	- Signal-to-Noise ratios larger than 100

These cuts ensure that the sample consists of stars on the upper red giant
branch, which are luminous enough to sample a wide range of galactocentric
radius.
This also safely excludes red clump stars to avoid potential systematic
differences in the abundances between the two spectral classes.

The rest of the APOGEE DR16 data can be accessed through the
`Sloan Digital Sky Survey`__.

__ sdss_
.. _sdss: https://www.sdss.org/dr16/

Feuillet et al. (2018)
----------------------

|feuillet2018|

The `Feuillet et al. (2018)`__ sample can be found at ``./data/feuillet2018``.
In this directory are three files: ``age_alpha.dat``, ``age_mh.dat``, and
``age_oh.dat``, corresponding to the age-[alpha/Fe] relation, the
age-[M/H] relation, and the age-[O/H] relation, respectively.
Each of these files stores ascii text containing four columns, the first two of
which are the minimum and maximum of a bin in [alpha/Fe], [O/H], or
[M/H], depending on the file.
The third and fourth are the mean and standard deviation of a gaussian in
log age fit to the data in each abundance bin.

__ feuillet2018_

Feuillet et al. (2019)
----------------------

|feuillet2019|

The `Feuillet et al. (2019)`__ sample can be found at ``./data/age_alpha``,
``./data/age_mh``, and ``./data/age_oh``, each directory containing the
reported age-[alpha/Fe], age-[M/H], and age-[O/H] relations,
respectively. The file names in each directory are of the format
``ELEM_GAUSS_AGE_A_B_C_D_X.fits``, where ``A`` and ``B`` denote the minimum
and maximum galactocentric radius in kpc, and ``C`` and ``D`` the minimum and
maximum disk midplane distances |z| of the sample.
In each of the fits files, the following columns are used in the
Johnson et al. (2021) comparison:

	- ``BIN_AB`` : The minimum of the bin in abundance
	- ``BIN_AB_MAX`` : The maximum of the bin in abundance
	- ``MEAN_AGE`` : The mean log-age determined via their fit
	- ``AGE_DISP`` : The dispersion in log-age determined via their fit
	- ``NSTARS`` : The number of stars in the bin

__ feuillet2019_

Although there are other quantities stored in these files, only these columns
are relevant to Johnson et al. (2021).


Vincenzo et al. (2021)
----------------------

|vincenzo2021|

The `Vincenzo et al. (2021)`__ sample is located at ``./data/ofe_mdfs``. The
files names in this directory are of the format
``RminA_hminB_FeHminC.dat``. ``A`` denotes the minimum galactocentric radius in
kpc of the corresponding 2-kpc wide bin. ``B`` denotes the minimum disk
midplane distance in kpc of the corresponding region (either
0 - 0.5 kpc, 0.5 - 1 kpc, or 1 - 2 kpc). ``C`` denotes the minimum [Fe/H] of
the metallicity bin with width [Fe/H] = 0.2. These are plain
ascii text files, where the final two columns contain the value of [O/Fe] and
the value of the distribution, respectively.

__ vincenzo2021_

