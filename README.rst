
| |version| |MIT Licensed| |travis| |issues| |paper1| 
| |Authors| |userguide| |scidocs| 


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
2.7 GHz Intel Core i5 processor with 8 GB of DDR3 RAM (e.g. a base-model 
2015 Macbook Pro), a simulation over the default parameter space with 
typical timesteps (e.g. 10 Myr) finishes in 82 milliseconds per simulated 
element. With finer timestepping (e.g. 1 Myr), the simulation finishes in ~6.0 
seconds per simulated element. These simulations require only ~3 and ~25 MB of 
RAM per simulated element, respectively, and are thus not memory-limited. 

Dependencies 
============

Primary 
-------
The following dependencies must be satisfied for ``VICE`` to install properly: 

1) ``Cython >= 0.28.0``

2) ``Python >= 3.5``

3) ``Make >= 3.81``

4) ``Clang >= 3.6.0 or gcc >= 4.6`` 

Secondary
---------
``VICE`` will run independently of the following, but either enable extra 
features or make it easier to use ``VICE``. 

1) ``dill >= 0.2.0`` is required for saving functional attributes within 
``VICE`` outputs. Without ``dill``, these attributes are simply not saved with 
outputs. It can be installed via ``pip install dill [--user]``. 

2) ``matplotlib >= 2.0.0`` is necessary for ``VICE``'s ``show`` function, 
intended to allow users to visually inspect their integrations visually in 
``ipython``, a ``jupyter notebook``, or similar without having to plot it 
themselves. This functionality is not intended to produce publication-quality 
figures, and is included purely for convenience. This function does not 
contribute to the scientific features of ``VICE`` and for that reason is not 
listed as a primary dependency. 

3) ``numpy`` is used in ``VICE``'s tutorial, which makes use of the 
``linspace`` function. 

A Note on Implementation 
------------------------
``VICE`` is implemented in ``ANSI/ISO C`` and is wrapped using only standard 
library ``python`` and ``Cython``. It is thus independent of the user's 
version of Anaconda, or lackthereof. It is NumPy- and Pandas-compatible, but 
neither NumPy- nor Pandas-dependent. That is, it will recognize user input 
from NumPy and Pandas data types, but is designed to run independently of 
them. 

Installation
============
``VICE`` must be installed from a terminal using the following sequence of 
commands:

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
option ``--user`` should be invoked when users wish to install to their 
``~/.local/`` library. Users installing to multiple version of ``python`` may 
run the tests over a specific version from the ``Makefile`` as indicated 
above. We caution users that running the tests for multiple versions of 
``python`` simultaneously may cause a ``segmentation fault``. 

If the user is installing to their ``~/.local/`` directory, then 
``~/.local/bin/`` must be on their ``PATH`` for ``VICE`` to run from the 
command-line. ``VICE`` will permanently add this to the user's ``PATH`` along 
with the installation process if it is not already there. This may require 
running ``source ~/.bash_profile`` after installation or restarting the 
``linux`` shell before running properly.

This is currently the only installation method for ``VICE``. It is currently 
not installable via ``pip``. 

Installation Methods to Avoid 
-----------------------------

**1) Parallel Installations**: Users installing to multiple version of 
``python`` should not run the ``setup.py`` file in separate terminals 
simultaneously. It is likely that this will cause at least one of the 
installations to fail. 

**2) conda Environments**: ``VICE`` should **never** be installed from within 
a ``conda`` environment. In this case, the installation process will run 
smoothly, but the compiled extensions will not be placed in the correct 
directory, preventing ``VICE`` from running properly. This however does not 
include the ``base`` default environment associated with later versions of 
``python`` and ``anaconda``. 

``VICE`` will *run* within whatever ``conda`` environments users create; it 
is only the installation process that this applies to. ``VICE`` is implemented 
independently of ``anaconda``, and for this reason, it does not make sense to 
install it in a ``conda`` environment anyway.

Usage 
=====
All of ``VICE``'s documentation is stored here under ``docs/``. 
We recommend that users retain copies of ``VICE``'s `user's guide`__ and 
`science documentation`__ for reference. These are PDFs with embedded 
hyperlinks for ease of use; the contents of this directory will download 
automatically with the source code. 

If users find ``VICE`` useful, we kindly request that they star this 
repository. This also helps us keep track of an approximate number of users. 

Tutorial
--------
Under ``docs/``, we provide `QuickStartTutorial.ipynb`__, a 
``jupyter notebook`` intended to provide first-time users with a primer on how 
to use all of ``VICE``'s features. After installation, users can launch the 
tutorial immediately via ``make tutorial``. 

From the Command Line 
---------------------
After installation, users can run simple simulations using ``VICE`` from the 
command line. Run ``vice --help`` in a terminal from any directory (with the 
exception of ``VICE``'s root directory) for instructions on how to use this 
functionality. We however caution users that ``VICE``'s functionality is 
severely limited when ran from the command line in comparison to its full 
``python`` capabilities. 

If users have installed ``VICE`` to their ``~/.local/`` library and ``VICE`` 
does not run properly from the command line, they may need to restart their 
linux shell (or, alternatively, run ``source ~/.bash_profile`` in a terminal 
from any directory). If this also does not work, it is likely that 
``~/.local/bin`` needs to be permanently added to their ``PATH``. 

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
`Johnson & Weinberg (2019)`__. From ``VICE``'s root directory, users can run 
``make jw19plots`` in a terminal, which will automatically run the simulations 
and produce the figures exactly as they appear in that paper. Users may also 
use these scripts as example code if they so choose. 

Submit a Bug Report 
===================
To submit a bug report, please open an issue `here`__. 

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

The only feature in this software requiring the use of Anaconda is the 
``show`` function associated with the ``output`` class, which requires 
``matplotlib >= 2``. This function is however not a part of the integration 
features associated with chemical evolution modeling, and is purely intended 
so that the user may inspect the results of their integrations visually in 
``ipython``, a ``jupyter notebook``, or similar without having to plot it 
themselves. This functionality is not intended to produce publication-quality 
figures, and is included purely for user convenience. 

Acknowledgements 
================
J.W.J. is grateful to David H. Weinberg and Jennifer A. Johnson at The Ohio 
State University for continual guidance in galactic chemical evolution 
modeling. J.W.J. also aknowledges valuable discussion on the implementation of 
the cumulative return fraction contributed by Jenna Freudenburg at The Ohio 
State University. Construction of this software was supported in part by an 
Ohio State University graduate fellowship. 

Citing
======
Usage of ``VICE`` leading to a publication should cite 
`Johnson & Weinberg (2019)`__. 

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

..	|issues| image:: https://img.shields.io/github/issues/giganano/VICE.svg
	:target: https://github.com/giganano/VICE/issues 
	:alt: issues 

..	|travis| image:: https://travis-ci.com/giganano/VICE.svg?branch=master 
	:target: https://travis-ci.com/giganano/VICE 
	:alt: travis 

..	|authors| image:: https://img.shields.io/badge/-Authors-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/AUTHORS.rst
	:alt: authors 

..	|userguide| image:: https://img.shields.io/badge/-User's%20Guide-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/users_guide.pdf 
	:alt: userguide 

..	|scidocs| image:: https://img.shields.io/badge/-Science%20Documentation-brightgreen.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/science_documentation.pdf
	:alt: scidocs 

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 
	:alt: paper1 


..	_authors: https://github.com/giganano/VICE/blob/master/AUTHORS.rst

.. _dill: https://pypi.org/project/dill/

.. _LICENSE: https://raw.githubusercontent.com/giganano/VICE/master/LICENSE

.. _userguide: https://github.com/giganano/VICE/blob/master/docs/users_guide.pdf 
.. _scidocs: https://github.com/giganano/VICE/blob/master/docs/science_documentation.pdf

.. _tutorial: https://github.com/giganano/VICE/blob/master/docs/QuickStartTutorial.ipynb

.. _citelink: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 

.. _issues: https://github.com/giganano/VICE/issues 

__ userguide_
__ scidocs_
__ tutorial_ 
__ citelink_ 
__ issues_ 
__ citelink_ 
