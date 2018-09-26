"""
Initializes the mass-metallicity grid of AGB yield parameters.
"""

import inspect
import sys
import os
from ...core._globals import DIRECTORY
PATH = "%sdata/_agb_yields/" % (DIRECTORY)

def _column(mat, ind):
	return [row[ind] for row in mat]

def _sort(arr):
	copy = arr[:]
	new = len(arr) * [0.]
	for i in range(len(copy)):
		new[i] = min(copy)
		copy[copy.index(min(copy))] = max(copy)
	return new

def read_grid(filename):
	grid = []
	with open(filename, 'r') as f:
		line = f.readline()
		while line != "":
			grid.append([float(i) for i in line.split()])
			line = f.readline()
		f.close()
	return grid

def yield_grid(element):
	"""
	Returns the mass-metallicity yield grid for the element.

	Args:
	=====
	element:				An elemental symbol (case-insensitive)

	Returns:
	========
	A 3-element array
		returned[0]:		The 2D grid itself, which can be accessed by giving 
					indexing in the following manner:
					yield = returned[2][mass_index][z_index]
		returned[1]:		The masses on the grid sorted least to greatest
		returned[2]:		The metallicities on the grid sorted least to greatest
	"""
	grid = read_grid("%s%s.dat" % (PATH, element.lower()))
	m = list(set(_column(grid, 0)))
	z = list(set(_column(grid, 1)))
	y = len(m) * [None]
	for i in range(len(m)):
		arr = len(z) * [0.]
		for j in range(len(z)):
			# y[i][j] = grid[len(m) * i + j][2]
			arr[j] = grid[len(z) * i + j][2]
		y[i] = arr
	return [y, _sort(m), _sort(z)]

