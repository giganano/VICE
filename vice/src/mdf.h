
#ifndef MDF_H 
#define MDF_H 

#ifdef __cplusplus 
extern "C" {
#endif 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to an MDF struct. Initializes all 
 * fields to NULL. 
 * 
 * source: mdf.c 
 */ 
extern MDF *mdf_initialize(void); 

/* 
 * Free up the memory stored in an MDF struct. 
 * 
 * source: mdf.c 
 */ 
extern void mdf_free(MDF *mdf); 

/* 
 * Setup the metallicity distribution functions. This does nothing more and 
 * nothing less than give each abundance and ratio distribution an array of 
 * zeroes representing the value in each bin. These arrays will be modified 
 * at each timestep as the simulation evolves. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object for the current simulation 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: mdf.c 
 */ 
extern int setup_MDF(SINGLEZONE *sz); 

/* 
 * Update the metallicity distribution function. This simply determines the bin 
 * number for each [X/H] abundance and [X/Y] abundance ratio in the specified 
 * binspace and increments it by the star formation rate. The prefactors are 
 * ignored because they cancel in normalization at the end of the simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object to update the MDF for 
 * 
 * source: mdf.c 
 */ 
extern void update_MDF(SINGLEZONE *sz); 

/* 
 * Normalize the metallicity distribution functions stored within a singlezone 
 * object in prep for write-out at the end of a simulation. This converts each 
 * distribution into a probability distribution function where the integral 
 * over the extent of the user-specified binspace is equal to 1. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object whose simulation just finished 
 * 
 * header: mdf.h 
 */ 
extern void normalize_MDF(SINGLEZONE *sz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MDF_H */ 



