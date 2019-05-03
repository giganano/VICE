
|version| |MIT Licensed| |Authors| |userguide| |scidocs| 

``VICE: Versatile Integrator for Chemical Evolution``
=====================================================

Overview
--------

``VICE`` is a user-friendly library designed to model the chemical enrichment 
of galaxies. It is capable of calculating nucleosynethetic yields of various 
elements, running simulations of enrichment under the single-zone, 
instantaneous mixing approximation, as well as simulating the enrichment of 
a given element from a single star cluster of given mass and metallicity. It 
is designed to model enrichment via core-collapse supernovae, type Ia 
supernovae, and asymptotic giant branch stars. 

Why You Should Use It
---------------------
``VICE`` is designed to recognize infall histories, gas histories, star 
formation histories, galactic outflows, outflow metallicities, inflow 
metallicities, and star formation efficiencies as arbitrary, callable functions 
of time in ``python``. It also allows the user to pass a function of time to 
specify their own supernovae Ia delay-time distribution, and supports 
user-specified fractional yields for both core-collapse and type Ia 
supernovae. In the case of core-collapse supernovae, ``VICE`` allows users to 
construct their own arbitrary, callable functions of metallicity. This wide 
range of customizability allows ``VICE`` to simulate galactic chemical 
enrichment for highly complex parameter spaces in nearly full generality. 
Furthermore, ``VICE`` recognizes all astrophysically produced elements between 
carbon and bismuth: a total of 76 elements on the periodic table. 

Furthermore, ``VICE`` achieves powerful computing speeds. On a system with a 
2.7 GHz Intal Core i5 processor with 8 GB of DDR3 RAM (e.g. a base-model 
2015 Macbook Pro), a simulation over the default parameter space with 
typical timesteps (e.g. 10 Myr) finishes in 82 milliseconds per simulated 
element. With finer timestepping (e.g. 1 Myr), the simulation finishes in ~6.0 
seconds per simulated element. These simulations require only ~3 and ~25 MB of 
RAM per simulated element, respectively, and are thus not memory-limited. 

Installation
============

System Requirements
-------------------

Installing ``VICE`` requires 60 MB of disk space. The source code stored 
in this repository is 45 MB, with 15 being copied to the desired install 
directory. If there is not adequate disk space, it is likely that the 
installation process will fail. 

``VICE`` supports linux and Mac OS X. Because ``VICE`` is implemented using 
only ``C`` and ``python`` standard libraries, it is technically entirely 
cross-platform. However, ``VICE`` is currently not packaged for installation 
on ``Windows``. Users can open a request at 
<https://github.com/giganano/VICE/issues> for ``Windows`` compatibility, and 
it will be fulfilled if there is sufficient demand. 

The following system requirements must be satisfied for ``VICE`` to install 
properly: 

1) ``Cython version >= 0.25.2``

2) ``Python version 2.7, or >= 3.5``

3) ``Make version >= 3.80``

4) ``Clang >= 4.2.0 or gcc >= 4.6``

**NOTE**: It is strongly recommended that users install ``dill`` along with 
``VICE`` if they have not already. This can be achieved via ``pip install 
dill``. ``VICE`` will run independently of ``dill``, but certain useful 
features are made possible with ``dill``. As such, ``VICE`` is not dependent 
on ``dill``, but users will miss out on certain features if they do not have 
it. 

``VICE``'s tutorial is dependent on ``numpy`` only weakly in that it 
uses ``numpy``'s ``linspace`` function. However, ``VICE`` is also independent 
of ``numpy``, and users may replace these lines in the tutorial if they so 
choose. 

Preferred Install Method
------------------------

We recommend users install ``VICE`` from a terminal using the following 
sequence of commands:

:: 
	
	$ git clone https://github.com/giganano/VICE.git 
	$ cd VICE
	$ make 
	$ python setup.py install [--user]
	$ [python2 setup.py install [--user]]
	$ [python3 setup.py install [--user]]
	$ make clean 
	$ make tests
	$ [make tests2] 
	$ [make tests3]

Optional elements of the installation process are bound in brackets. The 
option ``[--user]`` should be invoked when the user wishes to install to 
their ``~/.local/`` ``python`` library. If users are installing to multiple 
versions of ``python``, they should not run the setup file in separate 
terminals simultaneously. It is likely that this will cause at least one of 
the installations to fail. In this case, tests over a specific version can be 
ran from the ``Makefile`` as indicated above. 

Users should **NOT** install ``VICE`` in a ``conda`` environment. In this case, 
the installation process will run smoothly, but the compiled extensions will 
not be placed in the correct install directory, and ``VICE`` will not run. 
``VICE`` is implemented in ``C`` and wrapped for calling from python using 
only the standard library ``ctypes`` module, making it entirely ``anaconda`` 
independent. For this reason, it does not make sense to install in a ``conda`` 
environment anyway. ``VICE`` may be ran in whatever ``conda`` environments 
users desire, but the installation process must not be ran in such a manner. 

If the user is installing to their ``~/.local/`` directory, then 
``~/.local/bin/`` must be on their ``PATH`` for ``VICE`` to run from the 
command-line. ``VICE`` will permanently add this to the user's ``PATH`` along 
with the installation process if it is not already there. This may require 
running ``source ~/.bash_profile`` after installation or restarting the 
``linux`` shell before properly working.

This is the only install method for ``VICE``. It is currently not 
installable via ``pip``, but will be uploaded to ``PyPI`` in the coming weeks. 

Usage 
=====
All of ``VICE``'s documentation is stored here under ``docs/``. 
We recommend that users retain copies of ``VICE``'s `user's guide`__ and 
`science documentation`__ for reference. These are PDFs with embedded 
hyperlinks for ease of use. If installed via ``git``, the contents of this 
directory will download automatically with the source code. Users who install 
via ``pip`` will need to either clone this repository via ``git`` anyway or 
download the documentation separately in order to obtain copies. 

Tutorial
--------
Under ``docs/``, we provide `QuickStartTutorial.ipynb`__, a 
``jupyter notebook`` intended to provide first-time users with a primer on how 
to use all of ``VICE``'s features. If installed via ``git``, users can launch 
the tutorial immediately via ``make tutorial``. If installed via ``pip``, users 
must either clone this repository via ``git`` anyway or download the notebook 
separately in order to obtain a copy. 

From the Command Line 
---------------------
After installation, users can run simple simulations using ``VICE`` from the 
command line. Run ``vice --help`` in a terminal from any directory for 
instructions on how to use this functionality. We however caution users that 
``VICE``'s functionality is severely limited when ran from the command line in 
comparison to its full ``python`` capabilities. 

If users have installed to their ``~/.local/`` library and ``VICE`` does not 
run properly from the command line, they may need to restart their ``linux`` 
shell (or, alternatively, run ``source ~/.bash_profile`` in a terminal from any 
directory). If this also does not work, it is likely that the user needs to add 
``~/.local/bin/`` to their ``PATH``. 

Example Code: A Simulation of a Galaxy with Known Star Formation History   
------------------------------------------------------------------------
.. code:: python 

	import matplotlib.pyplot as plt 
	import numpy as np 
	import vice 

	def f(t): 
		"""
		The galaxy's star formation rate in Msun/yr as a function of 
		cosmic time in Gyr. 
		""" 
		return 8.7 * np.exp( -t / 5.2 ) 

	# Give a singlezone object the star formation history, some elements, and 
	# an array of output times in Gyr. 
	sz = vice.singlezone() 
	sz.name = "known_sfh" 
	sz.mode = "sfr" # f now represents star formation rate 
	sz.func = f 
	sz.tau_star = 1.7 # star formation per unit gas supply in yr^-1
	sz.elements = ["mg", "fe", "c", "n", "o", "s", "sr"] 
	sz.run(np.linspace(0, 10, 1001)) 

	# Read in the output holding the time-evolution of the ISM metallicity  
	hist = vice.history("known_sfh") 

	# plot the track in the [Mg/Fe]-[Fe/H] plane 
	plt.plot(hist["[fe/h]"], hist["[mg/fe]"], c = 'k') 
	plt.show() 
	plt.clf() 

	# plot the track in the [N/Mg]-[Mg/H] plane 
	plt.plot(hist["[mg/h]"], hist["[n/mg]"], c = 'k') 
	plt.show()
	plt.clf() 

	# Read in the output holding the stellar metallicity distribution 
	zdist = vice.mdf("known_sfh") 

	# Plot the [O/Fe] stellar probability density 
	bin_centers = [np.mean(i) for i in zip(zdist["bin_edge_left"], 
		zdist["bin_edge_right"])] 
	plt.plot(bin_centers, zdist["dn/d[o/fe]"], c = 'k') 
	plt.show() 
	plt.clf() 

Journal-Related Features
========================
We provide here the ``python`` code which produces all of the figures in 
Johnson & Weinberg (2019). From ``VICE``'s root directory, users can run 
``make jw19plots`` in a terminal, which will automatically run the simulations 
and produce the figures exactly as they appear in that paper. Users may also 
use these scrips as example code if they so choose. 

Submit a Bug Report 
===================
To submit a bug report, please open an issue at 
<https://github.com/giganano/VICE/issues>. 

Authors & Maintainers
=====================
The current version of ``VICE`` was written by James W. Johnson at The Ohio 
State University. See authors_ for details. 

Implementation
==============
``VICE`` is implemented entirely in ``ANSI/ISO C`` and standard library 
``python`` and ``Cython``. It is therefore entirely cross-platform. It is 
NumPy- and Pandas-compatible, but neither NumPy- nor Pandas-dependent. That is, 
it will recognize user input from NumPy and Pandas data types but will run 
independently of these software packages. All internal data is stored and 
handled using ``C`` and ``python`` standard libraries. It is thus independent 
of the user's version of Anaconda, or lackthereof. 

The only feature in this software requiring the user of Anaconda is the 
``show`` function assocaited with the ``output`` class, which requires 
``matplotlib >= 2``. This function is however not a part of the integration 
features associated with chemical evolution modeling, and is purely intended 
so that the user may inspect the results of their integrations visually in 
``ipython``, a ``jupyter notebook``, or similar without having to plot it 
themselves. This functionality is not intended to produce publication-quality 
figures, and is included purely for user convenience. 

We recommend that users install dill_ if they have not already. This package 
is required for encoding functional attributes in ``VICE`` outputs. ``VICE`` 
will run independetly of this package, but functional attributes are not able 
to be saved without it.  

Citing
======
Usage of ``VICE`` leading to a publication should cite Johnson & Weinberg 
(2019, in prep). A ``BibTex`` entry will be added here once the paper is 
announced. 

LICENSE
=======

``VICE`` is open source software released under the MIT License. We invite 
researchers and developers to use, modify, and redistribute how they see fit 
under the terms of the associated LICENSE_. 

..	|version| image:: https://img.shields.io/badge/version-1.0.0-blue.svg
	:target: https://img.shields.io/badge/version-1.0.0-blue.svg
	:alt: version
..	|MIT Licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
	:target: https://raw.githubusercontent.com/giganano/VICE/master/LICENSE
	:alt: MIT License

..	|docs| image:: https://img.shields.io/badge/-docs-brightgreen.svg
	:target: https://github.com/giganano/VICE/tree/master/docs
	:alt: docs

..	|authors| image:: https://img.shields.io/badge/-Authors-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/AUTHORS.rst
	:alt: authors 

..	|userguide| image:: https://img.shields.io/badge/-User's%20Guide-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/users_guide.pdf 
	:alt: userguide

..	|scidocs| image:: https://img.shields.io/badge/-Science%20Documentation-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/science_documentation.pdf
	:alt: scidocs


..	_authors: https://github.com/giganano/VICE/blob/master/AUTHORS.rst

.. _dill: https://pypi.org/project/dill/

.. _LICENSE: https://raw.githubusercontent.com/giganano/VICE/master/LICENSE

.. _userguide: https://github.com/giganano/VICE/blob/master/docs/users_guide.pdf 
.. _scidocs: https://github.com/giganano/VICE/blob/master/docs/science_documentation.pdf

.. _tutorial: https://github.com/giganano/VICE/blob/master/docs/QuickStartTutorial.ipynb

__ userguide_
__ scidocs_
__ tutorial_ 
