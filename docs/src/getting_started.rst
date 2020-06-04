
Getting Started 
===============
Any questions regarding usage of VICE or its implementation can be directed 
to the primary author (James W. Johnson: giganano9@gmail.com). 

Tutorial 
--------
Under ``examples`` in VICE's source directory is the `quick start tutorial`__, 
a notebook intended to provide first-time users with a primar on how to use 
all of VICE's features. After installation, users can launch the tutorial 
immediately via ``make tutorial``. 

__ tutorial_ 
.. _tutorial: https://github.com/giganano/VICE/blob/master/examples/QuickStartTutorial.ipynb


Example Code
------------
We provide example scripts in VICE's source tree under examples_. 

.. _examples: https://github.com/giganano/VICE/tree/master/examples


Accessing Documentation 
-----------------------
After installing VICE, the documentation can be launched in a browser window 
via the ``vice-docs`` command line entry. If this feature does not work after 
installing VICE, troubleshooting can be found `here`__. Documentation can also 
be found in the docstrings embedded in the code, and in the 
`git repository`__. 

__ troubleshooting_ 
__ repo_ 
.. _troubleshooting: https://github.com/giganano/VICE/blob/master/INSTALL.rst.txt#vice-isn-t-running-from-the-command-line
.. _repo: https://github.com/giganano/VICE.git 


From the Command Line 
---------------------
VICE allows simple simulations to be ran directly from the command line. 
For instructions on how to use this functionality, run ``vice --help`` in a 
terminal from any directory (with the exception of VICE's source directory). 

If this feature does not work after installing VICE, troubleshooting can be 
found `here`__. 

**Note**: VICE's functionality is severely limited when ran from the command 
line in comparison to its full Python_ capabilities. 

__ troubleshooting_
.. _Python: https://www.python.org/ 
