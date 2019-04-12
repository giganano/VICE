/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "specs.h"
#include "utils.h"

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
extern int setup_Zin(MODEL *m, double *arr, long num_times, int index) {

	/* Allocate memory for this element's inflow metallicity */ 
	m -> Zin[index] = (double *) malloc (num_times * sizeof(double)); 

	/* Now just copy over the array */ 
	long i;
	for (i = 0l; i < num_times; i++) {
		m -> Zin[index][i] = arr[i]; 
	}
	return 1; 

}



/* 
 * Allocates memory for the array containing the inflow metallicity of each 
 * element at each timestep. 
 * 
 * Args:
 * =====
 * run: 			The INTEGRATION struct for this simulation
 * m: 				The MODEL struct for this simulation 
 * 
 * header: utils.h 
 */ 
extern int malloc_Zin(INTEGRATION run, MODEL *m) {

	/* Allocate memory to a pointer based onthe number of elements */ 
	m -> Zin = (double **) malloc (run.num_elements * sizeof(double *)); 
	return 1; 

}

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
 * header: utils.h
 */
extern int setup_elements(INTEGRATION *run, char **symbols, double *solars) {

	int i;
	/* 
	 * Python has already told the INTEGRATION object how many elements it is 
	 * going to track in the wrapper.  
	 */ 
	run -> elements = (ELEMENT *) malloc ((*run).num_elements * sizeof(
		ELEMENT));
	for (i = 0; i < (*run).num_elements; i++) {
		ELEMENT *e = &((*run).elements[i]);
		e -> symbol = symbols[i];
		e -> solar = solars[i];
	}
	return 0;

}

/* 
 * Sets up a dummy element so that the single_stellar_population function can 
 * run both faster and in fewer lines. 
 * 
 * Args:
 * =====
 * run:		The dummy INTEGRATION struct from the single_stellar_population 
 * 			function 
 * 
 * header: utils.h 
 */
extern int setup_dummy_element(INTEGRATION *run) {

	run -> elements = (ELEMENT *) malloc (sizeof(ELEMENT));
	return 1;

}

/* 
 * Frees the memory allocated by C subroutines in the simulation 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for this simulation
 * m:			The MODEL struct for this simulation 
 * 
 * header: utils.h
 */
extern void clean_structs(INTEGRATION *run, MODEL *m) {

	/* Free the model parameters setup during integration */
	free(m -> mdf);
	free(m -> R);
	free(m -> H);

	free(m -> Zin);

	if (strcmp((*m).dtd, "custom")) {
		free(m -> ria);
	} else {}

	/* Free the integration parameters setup during integration. */
	free(run -> Zall);

	/* Free individual element parameters setup during integration. */
	int i;
	for (i = 0; i < (*run).num_elements; i++) {
		ELEMENT *e = &((*run).elements[i]);
		free(e -> agb_grid);
		free(e -> agb_m);
		free(e -> agb_z);
	}

}

/*
 * Sets up the Zall array for the INTEGRATION struct. 
 * 
 * Args:
 * =====
 * run:		A pointer to the INTEGRATION struct
 * num_times:	The number of times that the iteration will evaluate at 
 * 
 * header: utils.h 
 */
extern void setup_Zall(INTEGRATION *run, long num_times) {

	int i;
	/* Allocate memory and fill it with zeroes */  
	run -> Zall = (double **) malloc ((*run).num_elements * sizeof(double *));
	for (i = 0; i < (*run).num_elements; i++) {
		run -> Zall[i] = (double *) malloc (num_times * sizeof(double));
		run -> Zall[i][0] = 0; 
	}

}




