
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
 * The rate of mass enrichment in Msun/Gyr. -1 if index is not between 0 
 * and the number of elements tracked by the simulation (i.e. if it would 
 * cause a segmentation fault). 
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
 * Returns value of the integrated IMF weighted by the mass yield of a 
 * given element, up to the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * file:		The nme of the data file containing the grid
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * m_lower:		The lower mass limit on star formation in units of Msun
 * m_upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins 
 * 
 * Returns 
 * ======= 
 * The mass yield from all CCSNe in a stellar population as predicted by the 
 * built-in yields, up to the normalization of the IMF. 
 * 
 * source: ccsne.c 
 */ 
extern double *IMFintegrated_fractional_yield_numerator(char *file, char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, 
	long Nmax, long Nmin); 

	/* 
 * Determine the value of the integrated IMF weighted by stellar mass, up to 
 * the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * m_lower:		The lower mass limit on star formation in units of Msun
 * m_upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins 
 * 
 * Returns 
 * ======= 
 * The total mass of a stellar population in Msun, up to the normalization of 
 * the IMF. 
 * 
 * source: ccsne.c 
 */ 
extern double *IMFintegrated_fractional_yield_denominator(char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, long Nmax, 
	long Nmin); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* CCSNE_H */ 

