/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * This script contains the extern declarations of the MODEL, ELEMENT, and 
 * INTEGRATION structs. 
 */

#ifndef SPECS_H
#define SPECS_H

/* Include the stdio.h file because FILE objects are declared here */ 
#include <stdio.h>

/* 
 * The fields of the MODEL struct contain user-specified model parameters that 
 * are either model-dependent or specific to the galaxy that they are 
 * simulating. 
 * 
 * Fields:
 * =======
 * imf:				The IMF to assume 
 *						VICE currently recognizes only Kroupa and Salpeter 
 * dtd:				The SNe Ia delay-time distribution to adopt 
 * mdf:				The stellar metallicity distribution function for each 
 * 						element 
 * bins:			The bins in which to sort the stellar MDF 
 * num_bins:		The number of bins in the array bins
 *						This is equal to the length of the bins array + 1 
 * eta:				The mass loading parameter at each timestep 
 * enh:				The outflow enhancement factor at each timestep 
 * Zin:				The inflow metallicity of each element at each timestep 
 * R: 				The cumulative return fraction at all timesteps 
 * H:				The hydrogen burning mass fraction at all timesteps 
 * tau_star:		The depletion time at all timesteps 
 * schmidt_index: 	The power law index on Kennicutt-Schmidt star formation 
 * 						efficiency 
 * mgschmidt: 		The normalization of the Kennicutt-Schmidt law 
 * t_d:				The minimum delay time for SNe Ia from a single stellar 
 * 						population 
 * tau_ia:			The e-folding timescale of SNe Ia 
 *  					Only relevant when the user is adopting the built-in 
 * 						exponential DTD 
 * ria: 			The SNe Ia DTD iself, normalized, and evaluated at all 
 * 						timesteps 
 * smoothing_time:	The outflow smoothing timescale in Gyr 
 * m_upper: 		The upper mass limit on star formation in Msun
 * m_lower:			The lower mass limit on star formation in Msun 
 * R0:				The recycling parameter, if continuous recycling is not 
 * 						implemented 
 * continuous: 		Whether or not to implement continuous recycling 
 * 						(1 for yes; 0 for no) 
 * schmidt: 		Whether or not to implement the Kennicutt-Schmidt law 
 * 						(1 for yes; 0 for no)
 * Z_solar:			The metallicity of the sun to adopt 
 * 						Default and recommended: 0.014 (Asplund et al. 2009) 
 */ 
typedef struct model {

	char *imf;
	char *dtd;
	double **mdf;
	double *bins;
	long num_bins;
	double *eta;
	double *enh;
	double **Zin;
	double *R;
	double *H;
	double *tau_star;
	double schmidt_index;
	double mgschmidt;
	double t_d;
	double tau_ia;
	double *ria;
	double smoothing_time;
	double m_upper;
	double m_lower;
	double R0;
	int continuous;
	int schmidt;
	double Z_solar;

} MODEL;

/* 
 * The fields of the ELEMENT struct contain parameters that are specific to 
 * a given element that the simulation is tracking. 
 * 
 * symbol: 			The elemental symbol from the periodic table 
 * ccsne_yields:	The yield from core-collapse supernovae at every 10^-5 step 
 * 						in Z from 0 to 0.5. 
 * sneia_yield: 	The yield of the element from SNe Ia 
 * agb_grid: 		The mass-metallicity grid of yields from AGB stars 
 * agb_m:			The masses on which the AGB yield grid is sampled 
 * agb_z: 			The metallicities on which the AGB yield grid is sampled 
 * num_agb_m: 		The number of masses on which the AGB yield grid is sampled 
 * num_agb_z:		The number of metallicities on which the AGB yield grid 
 * 						is sampled 
 * m_tot: 			The total mass of the element at the given timestep 
 * solar: 			The solar abundance of the element. This is not 
 * 						user-specifiable, and the values are defined in the 
 * 						_globals.py file. They are taken from Asplund et al. 
 * 						(2009), ARA&A, 47, 481 
 */ 
typedef struct element {

	char *symbol; 
	double *ccsne_yield; 
	double sneia_yield;
	double **agb_grid;
	double *agb_m;
	double *agb_z;
	long num_agb_m;
	long num_agb_z;
	double m_tot;
	double solar;

} ELEMENT;


/* 
 * The fields of the INTEGRATION struct contain parameters that are intrinsic 
 * to a timestep-integration of GCE parameters using Euler's method, as 
 * implemented in VICE. 
 * 
 * out1:			The output struct for the history.out output file 
 * out2: 			The output struct for the mdf.out output file 
 * mode: 			'ifr', 'sfr', or 'gas' based on what spec represents 
 * MG:				The gas mass in Msun at the current timestep 
 * SFR:				The star formation rate in Msun Gyr^-1 at any given timestep 
 * 					This value is specified in Msun yr^-1 in Python 
 * IFR: 			The inflow rate in Msun Gyr^-1 at any given timestep 
 * 					This value is specified in Msun yr^-1 in Python 
 * num_elements:	The number of elements being tracked by the integration 
 * mdotstar: 		The star formation rate at all timesteps 
 * Zall: 			The mass abundance of each element at all timesteps 
 * dt: 				The timestep size in Gyr 
 * current_time: 	The current time in the simulation in Gyr 
 * timestep: 		The timestep number 
 * elements: 		A pointer to all of the element structs 
 */ 
typedef struct integration {

	FILE *out1;
	FILE *out2;
	char *mode;
	double *spec;
	double MG;
	double SFR;
	double IFR;
	int num_elements;
	double *mdotstar;
	double **Zall;
	double dt;
	double current_time;
	long timestep;
	ELEMENT *elements;

} INTEGRATION;



#endif /* SPECS_H */

