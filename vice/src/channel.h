/* 
 * This is the header file for the arbitrary enrichment channel functions. 
 */ 

#ifndef CHANNEL_H 
#define CHANNEL_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cpluslus */ 

#include "objects.h" 

#ifndef CHANNEL_YIELD_GRID_STEP 
#define CHANNEL_YIELD_GRID_STEP 1e-5 
#endif /* CHANNEL_YIELD_STEP */ 

#ifndef CHANNEL_YIELD_GRID_MIN 
#define CHANNEL_YIELD_GRID_MIN 0 
#endif /* CHANNEL_YIELD_GRID_MIN */ 

#ifndef CHANNEL_YIELD_GRID_MAX 
#define CHANNEL_YIELD_GRID_MAX 0.5 
#endif /* CHANNEL_YIELD_GRID_MAX */ 

/* 
 * Allocate memory for and return a pointer to a CHANNEL object. 
 * Automatically initializes yield_ and rate to NULL. Allocates memory for and 
 * fills the grid_. 
 * 
 * source: channel.c 
 */ 
extern CHANNEL *channel_initialize(void); 

/* 
 * Free up the memory in a CHANNEL object. 
 * 
 * source: channel.c 
 */ 
extern void channel_free(CHANNEL *ch); 

/* 
 * Determine the rate of mass enrichment of a given element at the current 
 * timestep from all arbitrary enrichment channels. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * e: 		The element to find the rate of mass enrichment for 
 * 
 * Returns 
 * ======= 
 * The time-derivative of the arbitrary enrichment channels mass enrichment 
 * term 
 * 
 * source: channel.c 
 */ 
extern double mdot(SINGLEZONE sz, ELEMENT e); 

/* 
 * Obtain the IMF-integrated fractional mass yield of a given element from 
 * its internal yield table. 
 * 
 * Parameters 
 * ========== 
 * e: 		The element to find the yield for 
 * Z: 		The metallicity to look up on the grid 
 * 
 * Returns 
 * ======= 
 * The interpolated yield off of the stored yield grid within the CHANNEL 
 * struct. 
 * 
 * source: channel.c 
 */ 
extern double get_yield(CHANNEL ch, double Z); 

/* 
 * Enrichh all elements in a multizone simulation from all custom enrichment 
 * channels from all tracer particles in the simulation. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * channel.c 
 */ 
extern void from_tracers(MULTIZONE *mz); 

/* 
 * Normalize the rate once it is set according to an arbitrary normalization 
 * by the user in python. 
 * 
 * Parameters 
 * ========== 
 * e: 			The ELEMENT struct to normalize the rate for. 
 * length: 		The length of the e -> channels[i] -> rate array 
 * 
 * source: channel.c 
 */ 
extern void normalize_rates(ELEMENT *e, unsigned long length); 

#ifdef __cpluslus 
} 
#endif /* __cplusplus */ 

#endif /* CHANNEL_H */ 



