
|logo| 

Versatile Integrator for Chemical Evolution
+++++++++++++++++++++++++++++++++++++++++++

|version| |MIT Licensed| |travis| |docs| |issues| |paper1| 

..	|version| image:: https://img.shields.io/badge/PyPI-1.2.0-blue.svg
	:target: https://pypi.org/project/vice/ 
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

.. 	|docs| image:: https://readthedocs.org/projects/vice-astro/badge/?version=latest
	:target: https://vice-astro.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

..	|paper1| image:: https://img.shields.io/badge/NASA%20ADS-Johnson%20%26%20Weinberg%20(2020)-red
	:target: https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.1364J/abstract 
	:alt: JW20 

..	|logo| image:: logo/logo.png 

VICE is a user-friendly python_ package designed to model chemical enrichment 
in galaxies. 

* 77 elements on the periodic table 
* Fast integration of one-zone models 
* Enrichment from single stellar populations 
* Highly flexible nucleosynthetic yield calculations 
* User-defined mathematical forms describing: 
	- Nucleosynthetic yields in simulations 
	- Mixing processes in multi-zone models 
	- Infall and star formation histories 
	- The stellar initial mass function 
	- The star formation law 
	- Element-by-element infall metallicities 
	- Type Ia supernova delay-time distributions 

.. _python: https://www.python.org/ 

Quick Links
===========

* `Install VICE`__ 
	- `Dependencies`__ 
	- `Installing from Source`__ 
	- `Troubleshoot Your Build`__ 
* `Usage`__ 
	- `Tutorial`__ 
	- `Example Code`__ 
	- `From the Command Line`__ 
* `Documentation`__ 
* `Submit a Bug Report`__ 
* `Cite VICE`__ 
* `Acknowledgements`__ 
* `License`__ 

__ install_ 
__ dependencies_ 
__ sourceinstall_  
__ troubleshoot_ 
.. _install: https://vice-astro.readthedocs.io/en/latest/install.html 
.. _dependencies: https://vice-astro.readthedocs.io/en/latest/install.html#dependencies 
.. _sourceinstall: https://vice-astro.readthedocs.io/en/latest/install.html#installing-from-source
.. _troubleshoot: https://vice-astro.readthedocs.io/en/latest/install.html#troubleshooting-your-build

__ usage_ 
__ tutorial_ 
__ example_ 
__ fromcmdline_ 
.. _usage: https://vice-astro.readthedocs.io/en/latest/getting_started.html
.. _tutorial: https://github.com/giganano/VICE/blob/master/examples/QuickStartTutorial.ipynb
.. _example: https://github.com/giganano/VICE/tree/master/examples
.. _fromcmdline: https://vice-astro.readthedocs.io/en/latest/users_guide/command_line.html

__ docs_ 
.. _docs: https://vice-astro.readthedocs.io/en/latest/

__ issues_ 
.. _issues: https://github.com/giganano/VICE/issues

__ citing_ 
.. _citing: https://vice-astro.readthedocs.io/en/latest/developers/citing.html

__ acknowledgements_ 
.. _acknowledgements: https://vice-astro.readthedocs.io/en/latest/developers/acknowledgements.html

__ license_ 
.. _license: https://vice-astro.readthedocs.io/en/latest/developers/license.html

Journal Related Features 
========================
We provide `here`__ the python_ code which runs the simulations and produces 
the figures in `Johnson & Weinberg (2020)`__. After running ``make starburst`` 
in this directory, the figures will be located here under starbursts_.  

__ starbursts_ 
__ jw20_ 
.. _starbursts: https://github.com/giganano/VICE/tree/master/starbursts 
.. _jw20: https://ui.adsabs.harvard.edu/abs/2020MNRAS.498.1364J/abstract 

