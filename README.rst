
VICE: Versatile Integrator for Chemical Evolution
+++++++++++++++++++++++++++++++++++++++++++++++++

| |version| |MIT Licensed| |travis| |issues| |paper1| 
| |Authors| |userguide| |scidocs| 

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

..	|authors| image:: https://img.shields.io/badge/-Authors-blue.svg
	:target: https://github.com/giganano/VICE/blob/master/AUTHORS.rst
	:alt: authors 

..	|userguide| image:: https://img.shields.io/badge/-User's%20Guide-blue.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/users_guide.pdf 
	:alt: userguide 

..	|scidocs| image:: https://img.shields.io/badge/-Science%20Documentation-blue.svg
	:target: https://github.com/giganano/VICE/blob/master/docs/science_documentation.pdf
	:alt: scidocs 

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 
	:alt: paper1 

Overview
========

VICE is a user-friendly library designed to model the chemical enrichment 
of galaxies. It is capable of calculating nucleosynethetic yields of various 
elements, running simulations of enrichment under the single-zone, 
instantaneous mixing approximation, as well as simulating the enrichment of 
a given element from a single star cluster of given mass and metallicity. It 
is designed to model enrichment via core-collapse supernovae, type Ia 
supernovae, and asymptotic giant branch stars. 

Why You Should Use It
=====================
VICE is designed to recognize infall histories, gas histories, star 
formation histories, galactic outflows, outflow metallicities, inflow 
metallicities, and star formation efficiencies as arbitrary, callable functions 
of time in Python_. It also allows the user to pass a function of time to 
specify their own supernovae Ia delay-time distribution, and supports 
user-specified fractional yields for both core-collapse and type Ia 
supernovae. In the case of core-collapse supernovae, VICE allows users to 
construct their own arbitrary, callable functions of metallicity. This wide 
range of customizability allows VICE to simulate galactic chemical 
enrichment for highly complex parameter spaces in nearly full generality. 
Furthermore, VICE recognizes all astrophysically produced elements between 
carbon and bismuth: a total of 76 elements on the periodic table. 

Furthermore, VICE achieves powerful computing speeds. On a system with a 
2.7 GHz Intel Core i5 processor with 8 GB of DDR3 RAM (e.g. a base-model 
2015 Macbook Pro), a simulation over the default parameter space with 
typical timesteps (e.g. 10 Myr) finishes in 82 milliseconds per simulated 
element. With finer timestepping (e.g. 1 Myr), the simulation finishes in ~6.0 
seconds per simulated element. These simulations require only ~3 and ~25 MB of 
RAM per simulated element, respectively, and are thus not memory-limited. 

.. _Python: https://www.python.org/ 

Links
=====

* `Install VICE`__ 
	- `Dependencies`__ 
	- `Installation`__ 
	- `Troubleshoot Your Build`__ 
* `Usage`__ 
	- `Tutorial`__ 
	- `Example Code`__ 
	- `Accessing Documentation`__ 
	- `From the Command Line`__ 
* `Submit a Bug Report`__ 
* `Cite VICE`__ 
* `Acknowledgements`__ 
* `License`__ 

__ install_ 
__ dependencies_ 
__ installation_ 
__ troubleshoot_ 
.. _install: https://github.com/astrobeard/VICEdev/blob/master/INSTALL.rst.txt
.. _dependencies: https://github.com/astrobeard/VICEdev/blob/master/INSTALL.rst.txt#dependencies
.. _installation: https://github.com/astrobeard/VICEdev/blob/master/INSTALL.rst.txt#installation
.. _troubleshoot: https://github.com/astrobeard/VICEdev/blob/master/INSTALL.rst.txt#troubleshooting-your-build

__ usage_ 
__ tutorial_ 
__ example_ 
__ accessdocs_ 
__ fromcmdline_ 
.. _usage: https://github.com/astrobeard/VICEdev/blob/master/USAGE.rst.txt
.. _tutorial: https://github.com/astrobeard/VICEdev/blob/master/USAGE.rst.txt#tutorial
.. _example: https://github.com/astrobeard/VICEdev/tree/master/examples
.. _accessdocs: https://github.com/astrobeard/VICEdev/blob/master/USAGE.rst.txt#accessing-documentation
.. _fromcmdline: https://github.com/astrobeard/VICEdev/blob/master/USAGE.rst.txt#from-the-command-line 

__ issues_ 
.. _issues: https://github.com/giganano/VICE/issues

__ citing_ 
.. _citing: https://github.com/astrobeard/VICEdev/blob/master/CITING.rst.txt

__ acknowledgements_ 
.. _acknowledgements: https://github.com/astrobeard/VICEdev/blob/master/THANKS.rst.txt

__ license_ 
.. _license: https://github.com/giganano/VICE/blob/master/LICENSE

Journal Related Features 
========================
We provide `here`__ the Python_ code which runs the simulations and produces 
the figures in `Johnson & Weinberg (2020)`__. After running ``make starburst`` 
in this directory, the figures will be located here under starbursts_.  

__ starbursts_ 
__ jw20_ 
.. _starbursts: https://github.com/giganano/VICE/tree/master/starbursts 
.. _jw20: https://ui.adsabs.harvard.edu/abs/2019arXiv191102598J/abstract 


