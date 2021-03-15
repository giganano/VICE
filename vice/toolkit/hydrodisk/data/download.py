
import urllib 
import sys 
import os 
PATH = os.path.dirname(os.path.abspath(__file__)) 
NSUBS = int(30) 


def download(verbose = True): 
	r""" 
	Downloads the h277 supplementary data from VICE's source tree on GitHub
	""" 
	cwd = os.getcwd() 
	os.chdir(PATH) 
	if not os.path.exists("./h277"): os.mkdir("./h277") 
	# for sub in H277_IDS.keys(): 
	for sub in range(NSUBS): 
		# url = "https://drive.google.com/uc?export=download&id=%s" % (
		# 	H277_IDS[sub]) 
		url = "https://raw.githubusercontent.com/giganano/VICE/v1.2.x/vice/" 
		url += "toolkit/hydrodisk/data/h277/sub%d.dat" % (sub) 
		urllib.request.urlretrieve(url, "./h277/sub%d.dat" % (sub)) 
		if verbose: sys.stdout.write("\rDownloading subsample: %d of %d" % (
			sub + 1, NSUBS)) 
	if verbose: sys.stdout.write("\n") 
	os.chdir(cwd) 


def _h277_exists(): 
	r""" 
	Determines if the h277 supplementary data has been downloaded. 
	""" 
	status = True 
	# for sub in H277_IDS.keys(): 
	for sub in range(NSUBS): 
		status &= os.path.exists("%s/h277/sub%d.dat" % (PATH, sub)) 
		if not status: break 
	return status 


def _h277_remove(): 
	r""" 
	Removes the h277 supplementary data. 
	""" 
	try: 
		os.rmdir("%s/h277" % (PATH)) 
	except (FileNotFoundError, OSError): 
		raise FileNotFoundError("Supplementary data not found.") 

