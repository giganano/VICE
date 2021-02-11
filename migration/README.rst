
Johnson et al. (2021) Models
++++++++++++++++++++++++++++

|feuillet2018| |feuillet2019| |ahumada2020| |vincenzo2021| 

Here we provide instructions for running the Johnson et al. (2021) chemical 
evolution models for the Milky Way disk, producing the figures which appear in 
the corresponding paper, and accessing the observational sample used in the 
comparison. 

.. 	|feuillet2018| image:: https://img.shields.io/badge/NASA%20ADS-Feuillet%20et%20al.%20(2018)-red 
	:target: feuillet2018_ 
	:alt: feuillet2018 

.. 	|feuillet2019| image:: https://img.shields.io/badge/NASA%20ADS-Feuillet%20et%20al.%20(2019)-red 
	:target: feuillet2019_ 
	:alt: feuillet2019 

.. 	|ahumada2020| image:: https://img.shields.io/badge/NASA%20ADS-Ahumada%20et%20al.%20(2020)-red 
	:target: ahumada2020_ 
	:alt: ahumada2020 

.. 	|vincenzo2021| image:: https://img.shields.io/badge/NASA%20ADS-Vincenzo%20et%20al.%20(2021)-red 
	:target: vincenzo2021_ 
	:alt: vincenzo2021 

.. _feuillet2018: https://ui.adsabs.harvard.edu/abs/2018MNRAS.477.2326F/abstract 
.. _feuillet2019: https://ui.adsabs.harvard.edu/abs/2019MNRAS.489.1742F/abstract 
.. _ahumada2020: https://ui.adsabs.harvard.edu/abs/2020ApJS..249....3A/abstract 
.. _vincenzo2021: https://ui.adsabs.harvard.edu/abs/2021arXiv210104488V/abstract 

.. Contents:: 

Requirements 
============
To run these models, you must first `install the latest version of VICE`__, 
1.2.0. Unless you wish to modify VICE's source code to run some alternate 
version of these models, you can achieve this with a simple ``pip install vice`` 
command in a ``Unix`` terminal. VICE 1.2.0 is the earliest version that 
includes the necessary functionality with which to handle stellar migration. 
In turn, VICE 1.2.0 requires Python >= 3.5.0. 

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

Although VICE itself has no runtime dependencies, producing any of the 
figures included in Johnson et al. (2021) requires ``matplotlib >= 2.0.0`` and 
``numpy >= 1.17.0``. This is only relevant if you plan on making use of the 
``figures.py`` script. 

Maximum Number of Open File Descriptors 
---------------------------------------
Computers enforce a limit on the number of open file descriptors at a given 
time by a single application. VICE will open two file descriptors per annulus. 
With sufficiently narrow annuli, the user may exceed their system's limit for 
the number of simultaneously open files. To view the current limit of your 
system, run the following line in your ``Unix`` terminal: 

:: 

	$ ulimit -n 

The default number varies from system to system; on Mac OS X, it is 256, and on 
a computer running CentOS 7.4 (a Linux operating system), it is 1024. With a 
limit of ``n``, the user can run a model with only ``n/2`` annuli without 
producing a system error. If necessary, you can modify these limits using 
``launchctl`` on Mac OS X and ``sysctl`` on Linux operating systems. These 
commands are used to configure kernel parameters at runtime, and must be ran as 
``root``; as such, doing so requires ``admin`` privileges over your computer. 
If you do not have such capabilities and need to increase this limit for your 
research, you'll need to speak with your administrator about increasing the 
maximum number of open file descriptors on your system. 

To increase the maximum number of open file descriptors on Mac OS X, run the 
following set of lines: 

:: 
	
	$ sudo launchctl limit maxfiles <N> 
	$ ulimit -n <N> 

where ``<N>`` should be replaced with a number at least twice as large as the 
number of annuli you intend on using in the model. If your administrator has 
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

where ``<N>`` should again be replaced with a number at least twice as large 
as the number of annuli you intend on using in the model. 

Recommended: Screen Sessions 
----------------------------
If you haven't used the ``screen`` command before, it is a utility which allows 
you to create a new terminal session within your current one, then subsequently 
detach from it while some process with a long CPU-time may be running.  Many 
systems now come with ``screen`` pre-installed; 
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

To start a screen session, run ``screen -S [name]``; to then detach from the 
session, simply press ``Ctrl+A`` followed by ``Ctrl+D``. To reattach to a 
previous session, run ``screen -r [name]``. Terminating a ``screen`` session 
can be done by simply running ``exit`` from within the session. 

Runnings the Models 
===================
Before running the Johnson et al. (2021) models, you should ensure that you've 
satisfied all `Requirements`_, particularly the 
`Maximum Number of Open File Descriptors`_. 

All of the models can be ran via the ``simulations.py`` script in this 
directory. Running ``python simulations.py --help`` produces the following 
help message regarding the parameters which can be specified at runtime: 

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
|                            | "outer-burst"              | 
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

For a mathematical definition of the allowed strings for the ``migration`` and 
``evolution`` parameters, see the Johnson et al. (2021) paper. The Johnson et 
al. (2021) models as they appear in the associated paper should be ran with the 
following set of commands: 

:: 

	$ mkdir outputs 
	$ mkdir outputs/diffusion 
	$ mkdir outputs/linear 
	$ mkdir outputs/sudden 
	$ mkdir outputs/post-processing 
	$ python simulations.py -f --nstars=9 --name=./outputs/diffusion/insideout 
	$ python simulations.py -f --nstars=9 --evolution=static --name=./outputs/diffusion/static 
	$ python simulations.py -f --nstars=9 --evolution=lateburst --name=./outputs/diffusion/lateburst 
	$ python simulations.py -f --nstars=9 --evolution=outerburst --name=./outputs/diffusion/outerburst 
	$ python simulations.py -f --nstars=9 --migration=linear --name=./outputs/linear/insideout 
	$ python simulations.py -f --nstars=9 --migration=sudden --name=./outputs/sudden/insideout 
	$ python simulations.py -f --nstars=9 --migration=post-process --name=./outputs/post-process/insideout 

If desired, each individual call to ``simulations.py`` can be ran separately in 
a ``screen`` session following a single run of each of the ``mkdir`` commands 
above. 


Producing the Figures 
=====================
All of the figures in Johnson et al. (2021) can be produces via the 
``figures.py`` script. Running ``python figures.py --help`` produces the 
following help message: 

:: 

	$ python figures.py --help 

	usage: figures.py [-h] [--fig1] [--fig2] [--fig3] [--fig4] [--fig5] [--fig6]
	                  [--fig7] [--fig8] [--fig9] [--fig10] [--fig11] [--fig12]
	                  [--fig13a] [--fig13b] [--fig14] [--fig15] [--fig16]
	                  [--fig17]

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

These parameters simply tell the script which figure(s) you'd like produced. 
For example, ``python figures.py --fig9`` will produce only Fig. 9 of 
Johnson et al. (2021), where as ``python figures.py --fig9 --fig10`` will 
produces Figs. 9 and 10. 

.. warning:: In order for this script to work properly, the outputs of each of 
	the Johnson et al. (2021) models need to be at the following locations: 

	| ``./outputs/diffusion/static`` 
	| ``./outputs/diffusion/insideout`` 
	| ``./outputs/diffusion/lateburst`` 
	| ``./outputs/diffusion/outerburst`` 
	| ``./outputs/linear/insideout`` 
	| ``./outputs/sudden/insideout`` 
	| ``./outputs/post-process/insideout`` 

	where the directory names simply specify the stellar migration and star 
	formation history of the model, respectively. If the outputs are not in 
	these locations, it's likely the ``figures.py`` script will produce an 
	error message stating that an output is not found. 


Accessing the Observational Sample 
==================================
Johnson et al. (2021) made use of observational data from 
`Feuillet et al. (2018)`__, `Feuillet et al. (2019)`__, and 
`Vincenzo et al. (2021)`__ as well as the 16th data release of the Apache 
Point Observatory Galaxy Evolution Experiment (APOGEE; `Ahumada et al. 2020`__). 

__ feuillet2018_ 
__ feuillet2019_ 
__ vincenzo2021_ 
__ ahumada2020_ 

Feuillet et al. (2018) 
----------------------

|feuillet2018| 

The `Feuillet et al. (2018)`__ sample can be found at ``./data/feuillet2018``. 
In this directory are three files: ``age_alpha.dat``, ``age_mh.dat``, and 
``age_oh.dat``, corresponding to the age-[:math:`\alpha`/Fe] relation, the 
age-[M/H] relation, and the age-[O/H] relation. Each of these files contains 
four columns, the first two of which are the minimum and maximum of a bin in 
[:math:`\alpha`/Fe], [O/H], or [M/H], depending on the file. The third and 
fourth are the mean and standard deviation of a gaussian in log-age fit to the 
data in each abundance bin. 

__ feuillet2018_ 

Feuillet et al. (2019) 
----------------------

|feuillet2019| 

The `Feuillet et al. (2019)`__ sample can be found at ``./data/age_alpha``, 
``./data/age_mh``, and ``./data/age_oh``, each directory containing the 
reported age-[:math:`\alpha`/Fe], age-[M/H], and age-[O/H] relations, 
respectively. The file names in each directory are of the format 
``ELEM_GAUSS_AGE_A_B_C_D_X.fits``, where ``A`` and ``B`` denote the minimum 
and maximum galactocentric radius in kpc, and ``C`` and ``D`` the minimum and 
maximum heights above/below the galaxy disk midplane :math:`\left|z\right|` of 
the sample. In each of the fits files, the following columns are used in the 
Johnson et al. (2021) comparison: 

	- ``BIN_AB`` : The minimum of the bin in abundance 
	- ``BIN_AB_MAX`` : The maximum of the bin in abundance 
	- ``MEAN_AGE`` : The mean log-age determined via their fit 
	- ``AGE_DISP`` : The dispersion in log-age determined via their fit 
	- ``NSTARS`` : The number of stars in the bin 

__ feuillet2019_ 

Although there are other quantities stored in these files, only these columns 
are relevant to Johnson et al. (2021). 


Ahumada et al. (2020) 
---------------------

|ahumada2020| 

The sample of stars from APOGEE DR16 employed in the Johnson et al. (2021) 
comparison can be found at ``./data/dr16stars.dat``. This is a plain ascii 
text file containing APOGEE IDs, an identifier tagging stars as either high- or 
low-alpha sequence, [Mg/H], [O/H], [Fe/H], [Mg/Fe], effective temperatures, 
surface gravities, galactocentric radii in kpc, height above the disk midplane 
in kpc, and signal-to-noise ratios for each stars that passes the following 
cuts: 

	- 4000 K :math:`\leq T_\text{eff} \leq` 4600 K 
	- 1.0 :math:`\leq \log g \leq` 2.5 
	- SNR :math:`\geq` 100 

These cuts ensure that the sample consists of stars on the upper red giant 
branch, safely excluding red clump stars to avoid obvious systematics in the 
abundance distributions. 

The rest of the APOGEE DR16 data can be accessed through the 
`Sloan Digital Sky Survey`__. 

__ sdss_ 
.. _sdss: https://www.sdss.org/dr16/

Vincenzo et al. (2021) 
----------------------

|vincenzo2021| 

The `Vincenzo et al. (2021)`__ sample is located at ``./data/ofe_mdfs``. The 
files names in this directory are of the format 
``RminA_hminB_FeHminC.dat``. ``A`` denotes the minimum galactocentric radius in 
kpc of the correspond 2-kpc wide bin. ``B`` denotes the minimum height 
above/below the disk midplane in kpc of the corresponding region (either 
0 - 0.5 kpc, 0.5 - 1 kpc, or 1 - 2 kpc). ``C`` denotes the minimum [Fe/H] of 
the metallicity bin with width :math:`\Delta` [Fe/H] = 0.2. These are plain 
ascii text files, where the final two columns contain the value of [O/Fe] and 
the value of the distribution, respectively. 

__ vincenzo2021_ 

