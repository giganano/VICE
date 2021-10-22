# Configuration file for the Sphinx documentation builder.

import sys
if sys.version_info[:2] < (3, 5):
	raise RuntimeError("Python >= 3.5 required to compile VICE documentation.")
else: pass

try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import sphinx
except (ModuleNotFoundError, ImportError):
	raise RuntimeError("""Sphinx >= 2.0.0 is required to compile VICE's \
documentation.""")
version_info_from_string = lambda s: tuple([int(i) for i in s.split('.')])
if version_info_from_string(sphinx.__version__)[:2] < (2, 0):
	raise RuntimeError("Must have Sphinx version >= 2.0.0. Current: %s" % (
		sphinx.__version__))
else: pass
try:
	import vice
except (ModuleNotFoundError, ImportError):
	raise RuntimeError("""VICE not found. VICE must be installed before the \
documentation can be compiled.""")
import warnings
warnings.filterwarnings("ignore")
import os
# Generates the comprehensive API reference
os.system("make -C %s/api" % (
	os.path.dirname(os.path.abspath(__file__))))




# -- Project information -----------------------------------------------------

project = 'VICE'
copyright = '2020-2021, James W. Johnson'
author = vice.__author__
release = vice.__version__


# -- General configuration ---------------------------------------------------
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
html_theme = "nature"
html_logo = "../../logo/logo_transparent.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

latex_elements = {
	"maketitle": "\\input{%s/cover.tex}" % (
		os.path.dirname(os.path.abspath(__file__))
	)
}

