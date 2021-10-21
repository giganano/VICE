
import urllib.request
import sys
import os
PATH = os.path.dirname(os.path.abspath(__file__))
NSUBS = int(30) # hard coded into VICE


def download(verbose = True):
	r"""
	Downloads the h277 supplementary data from VICE's source tree on GitHub
	"""
	if not os.path.exists("%s/h277" % (PATH)): os.mkdir("%s/h277" % (PATH))
	for sub in range(NSUBS):
		url = "https://raw.githubusercontent.com/giganano/VICE/v1.3.x/vice/"
		url += "toolkit/hydrodisk/data/h277/sub%d.dat" % (sub)
		urllib.request.urlretrieve(url, "%s/h277/sub%d.dat" % (PATH, sub))
		if verbose: sys.stdout.write("\rDownloading subsample: %d of %d" % (
			sub + 1, NSUBS))
	if verbose: sys.stdout.write("\n")


def _h277_exists():
	r"""
	Determines if the h277 supplementary data has been downloaded.
	"""
	status = True
	for sub in range(NSUBS):
		status &= os.path.exists("%s/h277/sub%d.dat" % (PATH, sub))
		if not status: break
	return status


def _h277_remove():
	r"""
	Removes the h277 supplementary data.
	"""
	try:
		for sub in range(NSUBS):
			filename = "%s/h277/sub%d.dat" % (PATH, sub)
			if os.path.exists(filename): os.remove(filename)
		os.rmdir("%s/h277" % (PATH))
	except (FileNotFoundError, OSError):
		raise FileNotFoundError("Supplementary data not found.")

