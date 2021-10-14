
.. _getting_started: 

Getting Started 
===============
VICE's developers are happy to consult with scientists looking to 
incorporate it into their research. 
Email one of our :ref:`contributors <contributors>` or `join us on Slack`__ 
and start collaborating now! 

Users should also be aware of our :ref:`comprehensive API reference <apiref>`, 
where they can find instructions on how to use all of the functions and 
objects that VICE provides. 
Details on VICE's implementation and justification thereof can be found in 
our :ref:`science documentation <scidocs>`. 

__ slack_ 
.. _slack: https://join.slack.com/t/vice-astro/shared_invite/zt-tqwa1syp-faiQu0P9oe83cazb0q9tJA

Tutorial 
--------
Under ``examples`` in VICE's `GitHub repository`__ is the `tutorial`__, 
a ``jupyter notebook`` intended to provide first-time users with a primer on 
how to use all of VICE's features. After installation, this jupyter notebook 
can be viewed in the web browser by running ``vice --tutorial`` from the 
command line. Alternatively, if installing from source, it can be launched via 
``make tutorial`` in the root directory. To download this jupyter notebook, 
simply clone the git repository if you haven't already, and it will be under 
the ``examples`` directory. 

__ repo_ 
__ tutorial_ 
.. _repo: https://github.com/giganano/VICE.git 
.. _tutorial: https://github.com/giganano/VICE/blob/master/examples/QuickStartTutorial.ipynb


Example Code
------------
We provide `example scripts`__ in VICE's GitHub repository under ``examples``, 
alongside the `tutorial`__. 

__ examples_ 
__ tutorial_ 
.. _examples: https://github.com/giganano/VICE/tree/master/examples


Accessing Documentation 
-----------------------
After installing VICE, the documentation can be launched in a browser window 
via the ``vice --docs`` command line entry. If this feature does not work 
after installing VICE, troubleshooting can be found `here`__. Documentation 
can also be found in the docstrings embedded in the code, and in the 
`GitHub repository`__. 

__ troubleshooting_ 
__ repo_ 
.. _troubleshooting: https://github.com/giganano/VICE/blob/master/docs/src/install.rst#troubleshooting-your-build


From the Command Line 
---------------------
VICE allows simple one-zone models to be ran directly from the command line. 
For instructions on how to use this functionality, run ``vice --help`` in a 
terminal from any directory (with the exception of VICE's source directory). 
If the ``vice`` command-line entry isn't working, it's possible the variant 
``python3 -m vice`` is required. Further troubleshooting can be found `here`__. 

**Note**: VICE's functionality is severely limited when ran from the command 
line in comparison to its full python_ capabilities. 

__ troubleshooting_
.. _python: https://www.python.org/ 
