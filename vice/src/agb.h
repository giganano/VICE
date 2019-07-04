
#ifndef AGB_H 
#define AGB_H 

#ifdef __cplusplus 
extern "C" {
#endif 

/* The maximum mass of a star in Msun that undergoes an AGB phase in VICE */ 
#ifndef MAX_AGB_MASS 
#define MAX_AGB_MASS 8 
#endif /* MAX_AGB_MASS */ 

/* The minimum mass of a star in Msun that undergoes an AGB phase in VICE */ 
#ifndef MIN_AGB_MASS 
#define MIN_AGB_MASS 0 
#endif /* MIN_AGB_MASS */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to an AGB_YIELD_GRID struct and 
 * initialize all fields to NULL. 
 * 
 * source: agb.c 
 */ 
extern AGB_YIELD_GRID *agb_yield_grid_initialize(void); 

/* 
 * Free up the memory stored in an AGB_YIELD_GRID struct 
 * 
 * source: agb.c 
 */ 
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid); 

/* 
 * Determine the mass of a given element produced by AGB stars at the current 
 * timestep of a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 			The SINGLEZONE struct associated with the current simulation 
 * e: 			The ELEMENT struct to find the total mass yield for 
 * 
 * Returns 
 * ======= 
 * The mass of the given element in solar masses produced by AGB stars in one 
 * timestep from all previous generations of stars. 
 * 
 * header: agb.h 
 */ 
extern double m_AGB(SINGLEZONE sz, ELEMENT e); 

/* 
 * Determine the fractional yield of a given element from AGB stars at a 
 * given mass and metallicity. 
 * 
 * Parameters 
 * ========== 
 * e: 				The element struct containing AGB yield information 
 * Z_stars: 		The metallicity by mass Z of the AGB stars 
 * turnoff_mass:	The mass of the AGB stars 
 * 
 * Returns
 * ======= 
 * The fraction of each AGB star's mass that is converted into the element e 
 * under the current yield settings. 
 * 
 * source: agb.c 
 */ 
extern double get_AGB_yield(ELEMENT e, double Z_stars, double turnoff_mass); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* AGB_H */ 

