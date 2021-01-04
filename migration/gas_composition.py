r""" 
ARGV 
====
1) 		The name of the output 
""" 

import vice 
import sys 


def composition(name, helium = 0.27): 
	output = vice.output(name) 
	hi = 0 
	h2 = 0 
	zones = range(200) 
	for zone in zones: 
		key = "zone%d" % (zone) 
		sfr = output.zones[key].history["sfr"][-1] 
		mgas = output.zones[key].history["mgas"][-1] 
		tau_star = 1.e-9 * mgas / sfr 
		fmol = 2.0 / tau_star 
		hi += (1 - fmol) * mgas 
		if zone >= 60: h2 += fmol * mgas 
		# h2 += fmol * mgas 
	hi *= (1 - helium) 
	h2 *= (1 - helium) 
	return [hi, h2, h2 / (hi + h2)] 


def sfr(name): 
	output = vice.output(name) 
	sfr = 0 
	zones = ["zone%d" % (_) for _ in range(60, 200)] 
	for zone in zones: 
		sfr += output.zones[zone].history["sfr"][-1] 
	return sfr 


if __name__ == "__main__": 
	hi, h2, fmol = composition(sys.argv[1]) 
	print("HI mass: %.5e Msun" % (hi)) 
	print("H2 mass: %.5e Msun" % (h2)) 
	print("Total H mass: %.5e Musn" % ((hi + h2))) 
	print("Total ISM mass: %.5e Msun" % ((hi + h2) / (1 - 0.27))) 
	print("fmol: %.5f" % (fmol)) 
	print("Present day SFR: %.5f" % (sfr(sys.argv[1]))) 

