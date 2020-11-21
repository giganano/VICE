
import numpy as np 
import math as m 
RADII = np.linspace(0, 15.5, 1000) 


def thin_disk(radius): 
	sigma_0 = 1311e6 
	rs = 2.5 
	return sigma_0 * m.exp(-radius / rs) 


def thick_disk(radius): 
	sigma_0 = 353e6 
	rs = 2.0 
	return sigma_0 * m.exp(-radius / rs) 


def total_disk(radius): 
	return thin_disk(radius) + thick_disk(radius) 


def total_disk_mass(stop = RADII[-1]): 
	total = i = 0 
	while RADII[i] < stop and i < len(RADII): 
		total += total_disk((RADII[i + 1] + RADII[i]) / 2) * m.pi * (
			RADII[i + 1]**2 - RADII[i]**2 
		) 
		i += 1 
	return total 


def half_disk_radius(): 
	mass = i = 0 
	while mass < 0.5 * total_disk_mass(): 
		mass += total_disk((RADII[i + 1] + RADII[i]) / 2) * m.pi * (
			RADII[i + 1]**2 - RADII[i]**2 
		) 
		i += 1 
	return RADII[i] 


if __name__ == "__main__": 
	print("Total disk mass: %e Msun" % (total_disk_mass())) 
	print("Half mass radius: %.2f kpc" % (half_disk_radius())) 
	print("Mass ratio enclosed at %.2f kpc: %.2f" % (half_disk_radius(), 
		total_disk_mass(stop = half_disk_radius()) / total_disk_mass())) 

