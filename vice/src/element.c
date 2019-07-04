
#include <stdlib.h> 
#include "element.h" 
#include "agb.h" 
#include "ccsne.h" 
#include "sneia.h" 

/* 
 * Allocate memory for an return a pointer to an ELEMENT struct. This also 
 * allocates memory for the AGB_YIELD_GRID, CCSNE_YIELD_SPECS, and 
 * SNEIA_YIELD_SPECS stored in the ELEMENT struct. Allocates memory for a 
 * 5-element string for each element's symbol. 
 * 
 * header: element.h 
 */ 
extern ELEMENT *element_initialize(void) {

	ELEMENT *e = (ELEMENT *) malloc (sizeof(ELEMENT)); 
	e -> symbol = (char *) malloc (5 * sizeof(char)); 
	e -> agb_grid = agb_yield_grid_initialize(); 
	e -> ccsne_yields = ccsne_yield_initialize(); 
	e -> sneia_yields = sneia_yield_initialize(); 
	return e; 

} 

/*
 * Free up the memory stored in an ELEMENT struct 
 * 
 * header: element.h 
 */ 
extern void element_free(ELEMENT *e) {

	agb_yield_grid_free(e -> agb_grid); 
	ccsne_yield_free(e -> ccsne_yields); 
	sneia_yield_free(e -> sneia_yields); 
	free(e -> symbol); 
	free(e); 

} 

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
 * header: element.h 
 */ 
extern int malloc_Z(ELEMENT *e, long n_timesteps) {

	long i; 
	e -> Z = (double *) malloc (n_timesteps * sizeof(double)); 
	if ((*e).Z == NULL) {
		return 1; 
	} else {
		for (i = 0l; i < n_timesteps; i++) {
			e -> Z[i] = 0; 
		} 
		return 0; 
	}

}

