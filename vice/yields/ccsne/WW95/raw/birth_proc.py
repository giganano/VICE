"""
WW95 Initial Abundances
"""
from vice._globals import _RECOGNIZED_ISOTOPES_
import glob
from os.path import basename

# VICE info
outfile = '../'
out_feh = ['FeH-inf', 'FeH-4', 'FeH-2', 'FeH-1', 'FeH0']

eles = glob.glob("../%s/v0/explosive/*.dat" % (out_feh[0]))
eles = [basename(ele).replace(".dat", "") for ele in eles]

for feh in out_feh:
	with open(outfile+feh+'/birth_composition.dat', 'w') as f:
		for iso in _RECOGNIZED_ISOTOPES_:
			ele = "".join([c for c in iso if not c.isdigit()])
			if ele in eles:
				f.write('%s \t %1.3e \n' % (iso.lower(), 0))
	f.close()
