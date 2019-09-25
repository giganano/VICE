
#ifndef CCSNE_H 
#define CCSNE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#ifndef CC_YIELD_STEP 
#define CC_YIELD_STEP 1e-5 
#endif /* CC_YIELD_STEP */ 

#ifndef CC_YIELD_GRID_MIN 
#define CC_YIELD_GRID_MIN 0 
#endif /* CC_YIELD_GRID_MIN */ 

#ifndef CC_YIELD_GRID_MAX 
#define CC_YIELD_GRID_MAX 0.5 
#endif /* CC_YIELD_GRID_MAX */ 

/* minimum mass of a star for a CCSN in VICE */ 
#ifndef CC_MIN_STELLAR_MASS 
#define CC_MIN_STELLAR_MASS 8 
#endif /* CC_MIN_STELLAR_MASS */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a CCSNE_YIELD_SPECS struct. 
 * This also allocates memory for the grid of metallicities and automatically 
 * fills it with the grid defined by CC_YIELD_GRID_MIN, CC_YIELD_GRID_MAX, 
 * and CC_YIELD_STEP as defined in ccsne.h. Initializes the yield_ value to 
 * NULL. 
 * 
 * source: ccsne.c 
 */ 
extern CCSNE_YIELD_SPECS *ccsne_yield_initialize(void); 

/* 
 * Free up the memory stored in a CCSNE_YIELD_SPECS struct 
 * 
 * source: ccsne.c 
 */ 
extern void ccsne_yield_free(CCSNE_YIELD_SPECS *ccsne_yield); 

/* 
 * Determine the rate of mass enrichment of an element X from core-collapse 
 * supernovae at the current timestep. This is implemented acording to the 
 * following formulation (see section 4.2 of VICE's science documentation): 
 * 
 * Mdot_x_CC = y_x_CC * SFR 
 * 
 * Parameters 
 * ========== 
 * sz: 			The SINGLEZONE object for the current integration 
 * e: 			The ELEMENT struct corresponding to the element to find the 
 * 				mass enrichment rate for  
 * 
 * Returns 
 * ======= 
 * The rate of mass enrichment in Msun/Gyr. 
 * 
 * source: ccsne.c 
 */ 
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e); 

/* 
 * Obtain the IMF-integrated fractional mass yield of a given element from its 
 * internal yield table.  
 * 
 * Parameters 
 * ========== 
 * e: 				The element to find the yield for 
 * Z: 				The metallicity to look up on the grid 
 * 
 * Returns 
 * ======= 
 * The interpolated yield off of the stored yield grid within the ELEMENT 
 * struct. 
 * 
 * source: ccsne.c 
 */ 
extern double get_cc_yield(ELEMENT e, double Z); 

/* 
 * Copy the explodability criteria that the user passed to 
 * yields.ccsne.fractional. 
 * 
 * Parameters 
 * ========== 
 * masses: 			The masses themselves. Python will ensure that this is 
 * 					always divisible by two 
 * n_masses: 		The number of masses in the mass binspace 
 * explodability: 	The explosion fractions 
 * 
 * source: ccsne.c 
 */ 
extern void set_explodability_criteria(double *masses, unsigned int n_masses, 
	double *explodability); 

/* 
 * Determine the value of the integrated IMF weighted by the mass yield of a 
 * given element, up to the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 		The integral object for the numerator of the yield 
 * imf:			The associated IMF object 
 * file:		The nme of the data file containing the grid
 * 
 * Returns 
 * ======= 
 * The mass yield from all CCSNe in a stellar population as predicted by the 
 * built-in yields, up to the normalization of the IMF. 
 * 
 * source: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_numerator(
	INTEGRAL *intgrl, IMF_ *imf, char *file); 

/* 
 * Determine the value of the integrated IMF weighted by stellar mass, up to 
 * the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 		The integral object for the denominator of the yield 
 * imf:			The associated IMF object 
 * 
 * Returns 
 * ======= 
 * 3 on an unrecognized IMF, otherwise the value returned by quad (see 
 * quadrature.h) 
 * 
 * source: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_denominator(
	INTEGRAL *intgrl, IMF_ *imf); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* CCSNE_H */ 

