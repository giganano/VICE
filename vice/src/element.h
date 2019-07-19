/* 
 * This header file defines the ELEMENT struct, an object to hold all of the 
 * parameters specific to individual elements on the periodic table. 
 */ 

#ifndef ELEMENT_H 
#define ELEMENT_H 

#ifdef __cplusplus 
extern "C" {
#endif 

#include "objects.h" 

/* 
 * Allocate memory for an return a pointer to an ELEMENT struct. This also 
 * allocates memory for the AGB_YIELD_GRID, CCSNE_YIELD_SPECS, and 
 * SNEIA_YIELD_SPECS stored in the ELEMENT struct. Allocates memory for a 
 * 5-element string for each element's symbol. 
 * 
 * source: element.c 
 */ 
extern ELEMENT *element_initialize(void); 

/*
 * Free up the memory stored in an ELEMENT struct 
 * 
 * source: element.c 
 */ 
extern void element_free(ELEMENT *e); 

/* 
 * Allocates memory for bookkeeping each elements previous ISM metallicity 
 * and sets each element to zero. 
 * 
 * Parameters 
 * ========== 
 * e: 				A pointer to the element to setup the Z array for 
 * n_timesteps: 	The number of elements in this array (i.e. the total 
 * 					number of timesteps in the simulation) 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: element.c 
 */ 
extern int malloc_Z(ELEMENT *e, long n_timesteps); 

/* 
 * Updates the mass of a single element at the current timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object currently being simulated 
 * e: 		A pointer to the element to update 
 * 
 * source: element.c 
 */ 
extern void update_element_mass(SINGLEZONE sz, ELEMENT *e); 

/* 
 * Updates the mass of each element in each zone to the proper value at the 
 * next timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * source: element.c 
 */ 
extern void update_elements(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif 
#endif /* ELEMENT_H */ 


