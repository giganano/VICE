
VICE Documentation
++++++++++++++++++
Welcome to VICE's documentation! 

Prerequisites
=============
Rebuilding VICE's documetation requires the following 

1. Sphinx_ >= 2.0.0 

2. Make_ >= 3.81 

.. _Sphinx: https://www.sphinx-doc.org/en/master/ 
.. _Make: https://www.gnu.org/software/make/ 

Recompile 
=========
To recompile the documentation, first install VICE. Most of the user's guide 
is generated from docstrings embedded in the code, which must be compiled 
before python can import it. Then run either ``make`` within this directory or 
``make docs`` in VICE's source directory immediately after running the 
setup.py file. 

This will automatically produce both the html and the PDF forms of the 
documentation. The PDF form will be located here under the name vice.pdf, and 
the root html document at src/_build/html/index.html. Running ``make open`` 
within this directory will open the html documentation in the default web 
browser. 

When finished, running ``make clean`` in this directory will remove all of the 
output files. 

