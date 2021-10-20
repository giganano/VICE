
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
To recompile the documentation, first `install VICE from source`__. Most of
the user's guide is generated from docstrings embedded in the code, which must
be compiled and installed before they can be imported into Python. Then run
either ``make`` within this directory or ``make docs`` in the parent
directory immediately after running the ``setup.py`` file.

__ install_
.. _install: https://github.com/giganano/VICE/blob/master/docs/src/install.rst#installing-from-source

This will automatically produce both the HTML and the PDF forms of the
documentation. The PDF form will be located here under the name vice.pdf, and
the root HTML document at src/_build/html/index.html. Running ``make open``
within this directory will open the HTML documentation in the default web
browser once this process is finished.

When finished, running ``make clean`` in this directory will remove all of the
output files. Unless modifications are made to the ``.gitignore`` file in the
parent directory, all documentation output will be ignored by version control.

