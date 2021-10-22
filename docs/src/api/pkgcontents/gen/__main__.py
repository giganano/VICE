"""
This file creates the rst files required to generate VICE's documentation
"""

import sys
if sys.version_info[:2] < (3, 6):
	raise RuntimeError("Python >= 3.6 required to compile VICE documentation.")
else: pass

import vice
from doctree import doctree

if __name__ == "__main__":
	doctree(vice).save()

