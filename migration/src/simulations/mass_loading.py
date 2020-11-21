
from vice import solar_z 

def strong_mass_loading(rgal): 
	return 0.015 / solar_z['o'] * (10**(0.08 * (rgal - 4) - 0.3)) - 0.6 
