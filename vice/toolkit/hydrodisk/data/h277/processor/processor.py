r"""
This script reads in the fits file containing the h277 star particle data for
stars that are <150 Myr old at first snapshot, and places them in a given
number of subsamples in the appropriate directory for use within VICE.

ARGV
====
1) 		The integer random number seed to use in assigning star particles
		random sub-files, if desired.

.. note:: Running this script makes use of the astropy.io.fits functionality

.. seealso:: Johnson et al. (2021) [1]_

.. [1] J.W. Johnson et al. (2021, in prep)
"""

from astropy.io import fits
import random
import sys
import os

# Name of the input file in this directory
INPUT_FILE = "h277_star_particles_150Myr.fits"

# maximum age at first snapshot in Myr; cannot get larger than 150 Myr, as the
# source file does not include those at >150 Myr anyway.
MAX_AGE_AT_FIRST_SNAPSHOT = 150

# Number of subset files to use; hard-coded in VICE at
# vice/src/toolkit/hydrodiskstars.c as static unsigned short NSUBS = 30u
N_OUTFILES = 30

# Source file has kinematic decomposition tags as integers. Halo stars are
# omitted here, so reassign them a number a little more intuitive.
# (These will be reflected in the documentation.)
DECOMP_REASSIGN = {
	1: 1, # thin disk
	4: 2, # thick disk
	3: 3, # bulge
	5: 4, # pseudobulge
	2: 5  # halo
}

# The amount of time subtracted from ages. Hydrodisk models place the onset of
# star formation some time following T = 0 in h277.
AGE_SHIFT = 0.5

#####################


def main(seed = 0):
	r"""
	Divide the h277 star particles across their respective subfiles in the
	appropriate directory.

	Parameters
	----------
	seed : int [default : 0]
		The random number seed to adopt in assigned star particles to
		sub-files.

	.. note:: The output files with *always* be placed in this script's
		parent directory.
	"""
	# Change into this file's directory
	src_path = os.path.dirname(os.path.abspath(__file__))
	old_path = os.getcwd()
	os.chdir(src_path)

	# Open all output files and write a brief header
	header = "# id Tform Rform Rfinal Zform Zfinal v_r v_phi v_z decomp"
	outfiles = N_OUTFILES * [None]
	for i in range(N_OUTFILES):
		outfiles[i] = open("../sub%d.dat" % (i), 'w')
		outfiles[i].write("%s\n" % (header))

	# Parse the individual star particles from h277
	with fits.open(INPUT_FILE) as h277:
		n = 0
		random.seed(a = seed)
		for i in range(len(h277[1].data["tform"])):
			which_outfile = int(N_OUTFILES * random.random())
			write_star(outfiles[which_outfile], h277, i)
			n += 1
			sys.stdout.write("\r%d star particles" % (n))
			sys.stdout.flush()
		sys.stdout.write("\n")
		h277.close()

	for i in range(N_OUTFILES): outfiles[i].close()

	# Change back to original directory
	os.chdir(old_path)


def write_star(outfile, h277, index):
	r"""
	Writes a star particlefrom h277  to one of the output files if it passes
	the imposed cuts.

	Parameters
	----------
	outfile : file
		The file object obtained from calling python's ``open`` function.
	h277 : astropy.io.fits.hdu.hdulist.HUDList
		The fits file object opened by calling astropy.io.fits with the input
		file name.
	index : int
		The list index of the star particle in ``h277[1].data``.
	"""
	if all_cuts(h277, index):
		outfile.write("%d " % (h277[1].data["iord"][index]))
		outfile.write("%.4f " % (h277[1].data["tform"][index] - AGE_SHIFT))
		outfile.write("%.4f " % (h277[1].data["Rform"][index]))
		outfile.write("%.4f " % (h277[1].data["Rfinal"][index]))
		outfile.write("%.4f " % (h277[1].data["Zform"][index]))
		outfile.write("%.4f " % (h277[1].data["Zfinal"][index]))
		outfile.write("%.4f " % (h277[1].data["vrxy"][index]))
		outfile.write("%.4f " % (h277[1].data["vcxy"][index]))
		outfile.write("%.4f " % (h277[1].data["vz"][index]))
		outfile.write("%d \n" % (
			DECOMP_REASSIGN[h277[1].data["decomp"][index]]
		))
	else: pass


def all_cuts(h277, index):
	r"""
	Determines if a star passes the quality cuts imposed by this processor.

	Parameters
	----------
	h277 : astropy.io.fits.hdu.hdulist.HDUList
		The fits file object opened by calling astropy.io.fits with the input
		file name.
	index : int
		The list index of the star particle in ``h277[1].data``.

	Returns
	-------
	test : bool
		True if the star particle passes all quality cuts.

	Notes
	-----
	This function simply ensures that all cuts are passed via the python
	``all`` function, equivalent to a logical ``and`` operator.

	.. seealso::

		ageform_cut
		tform_cut
		disk_cut
		kinematic_cut
	"""
	# cuts = [ageform_cut, tform_cut, disk_cut, kinematic_cut]
	cuts = [ageform_cut, tform_cut, disk_cut]
	return all([cut(h277, index) for cut in cuts])


def ageform_cut(h277, index):
	r"""
	Determines if a star has an age at first snapshot adequately low to be
	included in the final sample.

	Parameters
	----------
	h277 : astropy.io.fits.hdu.hdulist.HDUList
		The fits file object opened by calling astropy.io.fits with the
		input file name.
	index : int
		The list index of the star particle in ``h277[1].data``.

	Returns
	-------
	test : bool
		True if the star particle was born <= 150 Myr before the first
		snapshot in which it appeared. False otherwise.

	Notes
	-----
	This is a quality cut to ensure that the birth radius of a given star
	particle is known to adequate accuracy for use in simulations such as
	VICE's ``milkyway`` object.
	"""
	# 1.e3 converts from Gyr to Myr
	return h277[1].data["ageform"][index] * 1.e3 <= MAX_AGE_AT_FIRST_SNAPSHOT


def tform_cut(h277, index):
	r"""
	Determines if a star has the minimum age required to be included in the
	final subsample.

	Parameters
	----------
	h277 : astropy.io.fits.hdu.hdulist.HDUList
		The fits file object opened by calling astropy.io.fits with the
		input file name.
	index : int
		The list index of the star particle in ``h277[1].data``.

	Returns
	-------
	test : bool
		True if the star particle was born at a simulation time >= 0.5 Gyr.
		False otherwise.

	Notes
	-----
	Star particles born prior to 0.5 Gyr into the h277 are not included in the
	final sample. This is a much better estimate of the onset of star
	formation in this galaxy than the beginning of that simulation.

	The exact time value can be adjusted via the AGE_SHIFT global variable in
	this file.
	"""
	return h277[1].data["tform"][index] >= AGE_SHIFT


def disk_cut(h277, index):
	r"""
	Determines if a star was born in a spatial region reasonably defining the
	disk of the simulated galaxy.
	
	Parameters
	----------
	h277 : astropy.io.fits.hdu.hdulist.HDUList
		The fits file object opened by calling astropy.io.fits with the input
		file name.
	index : int
		The list index of the star particle in ``h277[1].data``.

	Returns
	-------
	test : bool
		True if the star particle passes the spatial cut. False otherwise.

	Notes
	-----
	This cut is in place to ensure that the star particles used in the
	``milkyway`` object all formed close enough to the disk midplane to be
	considered "in-situ" stars.
	"""
	return (0 <= h277[1].data["Rform"][index] <= 20 and
		0 <= h277[1].data["Rfinal"][index] <= 20 and
		-3 <= h277[1].data["Zform"][index] <= 3)


def kinematic_cut(h277, index):
	r"""
	Determines if a star passes the kinematic cut of excluding halo stars
	based on the kinematic decomposition performed on the input file.

	Parameters
	----------
	h277 : astropy.io.fits.hdu.hdulist.HDUList
		The fits file object opened by calling astropy.io.fits with the input
		file name.
	index : int
		The list index of the star particle in ``h277[1].data``.

	Returns
	-------
	test : bool
		True if the star particle is not a halo star. False otherwise.

	Notes
	-----
	Many halo stars are believed to be accreted populations. For this reason,
	they should not be included in models of the in-situ chemical evolution of
	disk galaxies, as the ``milkyway`` object is intended.
	"""
	# halo stars have a decomp index of 2
	return h277[1].data["decomp"][index] in [1, 3, 4, 5]


if __name__ == "__main__":
	if len(sys.argv) > 1: # specified seed
		main(seed = int(sys.argv[1]))
	else:
		main()

