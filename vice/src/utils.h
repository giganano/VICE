
#ifndef UTILS_H
#define UTILS_H

/*
 * Sets the array in the MODEL struct containing the inflow metallicity at each 
 * timestep for a given element. The array is set up in the wrapper. 
 * 
 * Args:
 * =====
 * m:				The MODEL struct for this simulation
 * arr:				The array of inflowing metallicities
 * num_times:		The number of times at which the simulation will evaluate 
 * index: 			The index of the element 
 * 
 * source: utils.c 
 */
extern int setup_Zin(MODEL *m, double *arr, long num_times, int index);

/* 
 * Allocates memory for the array containing the inflow metallicity of each 
 * element at each timestep. 
 * 
 * Args:
 * =====
 * run: 			The INTEGRATION struct for this simulation
 * m: 				The MODEL struct for this simulation 
 * 
 * source: utils.c 
 */ 
extern int malloc_Zin(INTEGRATION run, MODEL *m); 

/* 
 * Sets up each ELEMENT struct with the symbol of the element and its solar 
 * abundance. 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for this simulation
 * symbols:			A pointer to the elemental symbols as char* arrays
 * solars:			A pointer to the solar abundances of each element 
 * 
 * source: utils.c 
 */
extern int setup_elements(INTEGRATION *run, char **symbols, double *solars);

/* 
 * Sets up a dummy element so that the single_stellar_population function can 
 * run faster. 
 * 
 * Args:
 * =====
 * run:		The dummy INTEGRATION struct from the single_stellar_population 
 * 			function  
 * 
 * source: utils.c 
 */
extern int setup_dummy_element(INTEGRATION *run);

/* 
 * Frees the memory allocated by C subroutines in the simulation 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for this simulation
 * m:			The MODEL struct for this simulation 
 * 
 * source: utils.c
 */
extern void clean_structs(INTEGRATION *run, MODEL *m);

/*
 * Sets up the Zall array for the INTEGRATION struct. 
 * 
 * Args:
 * =====
 * run:				A pointer to the INTEGRATION struct
 * num_times:		The number of times that the iteration will evaluate at 
 * 
 * source: utils.c  
 */
extern void setup_Zall(INTEGRATION *run, long num_times); 

#endif /* UTILS_H */

