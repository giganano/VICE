
#ifndef SSP_H 
#define SSP_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

/* main sequence lifetime ~ M^-MASS_LIFETIME_PLAW_INDEX */ 
#ifndef MASS_LIFETIME_PLAW_INDEX 
#define MASS_LIFETIME_PLAW_INDEX 3.5 
#endif /* MASS_LIFETIME_PLAW_INDEX */ 

/* The lifetime of the sun in Gyr */ 
#ifndef SOLAR_LIFETIME 
#define SOLAR_LIFETIME 10 
#endif /* SOLAR_LIFETIME */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to an SSP struct. Automatically 
 * sets both crf and msmf to NULL. Allocates memory for a 100-element char * 
 * IMF specifier. 
 * 
 * source: ssp.c 
 */ 
extern SSP *ssp_initialize(void); 

/*
 * Free up the memory stored in an SSP struct. 
 * 
 * source: ssp.c 
 */ 
extern void ssp_free(SSP *ssp); 

/* 
 * Determine the main sequence turnoff mass in solar masses of a single 
 * stellar population at a time t in Gyr following their formation. 
 * 
 * Parameters 
 * ========== 
 * t: 		Time in Gyr 
 * 
 * Returns 
 * ======= 
 * Main sequence turnoff mass in solar masses via (t / 10 Gyr)^(-1/3.5) 
 * 
 * Notes 
 * ===== 
 * 10 Gyr and 3.5 are values that can be changed in ssp.h 
 * 
 * source: ssp.c 
 */ 
extern double main_sequence_turnoff_mass(double t); 

/* 
 * Run a simulation of elemental production for a single element produced by a 
 * single stellar population. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		A pointer to an SSP object 
 * e: 			A pointer to an element to run the simulation for 
 * Z: 			The metallicity by mass of the stellar population 
 * times: 		The times at which the simulation will evaluate 
 * n_times: 	The number of elements in the times array 
 * mstar: 		The mass of the stellar population in Msun 
 * 
 * Returns 
 * ======= 
 * An array of the same length as times, where each element is the mass of the 
 * given chemical element at the corresponding time. NULL on failure to 
 * allocate memory. 
 * 
 * header: ssp.h 
 */ 
extern double *single_population_enrichment(SSP *ssp, ELEMENT *e, 
	double Z, double *times, long n_times, double mstar); 

/* 
 * Determine the mass recycled from all previous generations of stars for 
 * either a given element or the gas supply. For details, see section 3.3 of 
 * VICE's science documentation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * e: 		A pointer to the element to find the recycled mass. NULL to find 
 * 			it for the total ISM gas. 
 * 
 * Returns 
 * ======= 
 * The recycled mass in Msun 
 * 
 * source: ssp.c 
 */ 
extern double mass_recycled(SINGLEZONE sz, ELEMENT *e); 

/* 
 * Evaluate the cumulative return fraction across all timesteps in preparation 
 * of a singlezone simulation. This will store the CRF in the SSP struct 
 * within the singlezone object. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A singlezone object to setup the CRF within 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: ssp.c  
 */ 
extern int setup_CRF(SINGLEZONE *sz); 

/* 
 * Determine the cumulative return fraction from a single stellar population 
 * a given time in Gyr after its formation. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		An SSP struct containing information on the stallar IMF and 
 * 				the mass range of star formation 
 * time: 		The age of the stellar population in Gyr 
 * 
 * Returns 
 * ======= 
 * The value of the CRF at that time for the IMF assumptions encoded into the 
 * SSP struct 
 * 
 * source: ssp.c  
 */ 
extern double CRF(SSP spp, double time); 

/* 
 * Evaluate the main sequence mass fraction across all timesteps in preparation 
 * of a singlezone simulation. This will store the MSMF in the SSP struct 
 * within the singlezone object. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A singlezone object to setup the MSMF within 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: ssp.c  
 */ 
extern int setup_MSMF(SINGLEZONE *sz); 

/* 
 * Determine the main sequence mass fraction of a stellar population a some 
 * time following its formation. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		A SSP struct containing information on the stellar IMF and 
 * 				the mass range of star formation 
 * time: 		The age of the stellar population in Gyr 
 * 
 * Returns 
 * ======= 
 * The value of the main sequence mass fraction at the specified age. -1 in 
 * the case of an unrecognized IMF. 
 * 
 * source: ssp.c  
 */ 
extern double MSMF(SSP ssp, double time); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_H */ 

