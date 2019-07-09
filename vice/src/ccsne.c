
#include <stdlib.h> 
#include <string.h> 
#include "ccsne.h" 
#include "io.h" 
#include "imf.h" 
#include "utils.h" 
#include "quadrature.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double interpolate_yield(double m); 
static double yield_weighted_kroupa01(double m); 
static double yield_weighted_salpeter55(double m); 
static double mass_weighted_kroupa01(double m); 
static double mass_weighted_salpeter55(double m); 

/* 
 * These variables are declared globally in this file because it is easier for 
 * quadrature functions to be able to access them while still only taking one 
 * parameter. 
 * 
 * GRID: 		The stellar mass - element yield itself 
 * GRIDSIZE:	The number of stellar masses on which the yield grid is sampled 
 */
static double **GRID; 
static int GRIDSIZE = 0; 

/* 
 * Allocate memory for and return a pointer to a CCSNE_YIELD_SPECS struct. 
 * This also allocates memory for the grid of metallicities and automatically 
 * fills it with the grid defined by CC_YIELD_GRID_MIN, CC_YIELD_GRID_MAX, 
 * and CC_YIELD_STEP as defined in ccsne.h. Initializes the yield_ value to 
 * NULL. 
 * 
 * header: ccsne.h 
 */ 
extern CCSNE_YIELD_SPECS *ccsne_yield_initialize(void) {

	CCSNE_YIELD_SPECS *ccsne_yield = (CCSNE_YIELD_SPECS *) malloc (sizeof(
		CCSNE_YIELD_SPECS)); 

	ccsne_yield -> yield_ = NULL; 

	/* 
	 * The number of elements on the yield grid between CC_YIELD_GRID_MIN and 
	 * CC_YIELD_GRID_MAX in steps of CC_YIELD_STEP (inclusive). 
	 */ 
	long num_grid_elements = (long) (
		(CC_YIELD_GRID_MAX - CC_YIELD_GRID_MIN) / CC_YIELD_STEP
	) + 1l; 

	/* Fill the grid starting at CC_YIELD_GRID_MIN in steps of CC_YIELD_STEP */ 
	long i; 
	ccsne_yield -> grid = (double *) malloc (num_grid_elements * sizeof(double)); 
	for (i = 0l; i < num_grid_elements; i++) {
		ccsne_yield -> grid[i] = CC_YIELD_GRID_MIN + i * CC_YIELD_STEP; 
	} 

	return ccsne_yield; 

} 

/* 
 * Free up the memory stored in a CCSNE_YIELD_SPECS struct 
 * 
 * header: ccsne.h 
 */ 
extern void ccsne_yield_free(CCSNE_YIELD_SPECS *ccsne_yield) {

	if ((*ccsne_yield).yield_ != NULL) free(ccsne_yield -> yield_); 
	free(ccsne_yield -> grid); 
	free(ccsne_yield); 

} 

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
 * header: ccsne.h 
 */ 
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e) {

	double Z = scale_metallicity(sz, sz.timestep); 
	double yield = get_cc_yield(e, Z); 
	return yield * (*sz.ism).star_formation_rate; 

	// return (get_cc_yield(e, scale_metallicity(sz, sz.timestep)) * 
	// 	(*sz.ism).star_formation_rate); 

}

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
 * The interpolated yield off of the stored yield grid within the ELEMENT struct. 
 * 
 * header: ccsne.h 
 */ 
extern double get_cc_yield(ELEMENT e, double Z) { 

	return interpolate(
		(long) (Z / CC_YIELD_STEP) * CC_YIELD_STEP, 
		(long) (Z / CC_YIELD_STEP) * CC_YIELD_STEP + CC_YIELD_STEP, 
		(*e.ccsne_yields).yield_[(long) (Z / CC_YIELD_STEP)], 
		(*e.ccsne_yields).yield_[(long) (Z / CC_YIELD_STEP + 1l)], 
		Z 
	); 

} 

/* 
 * Determine the value of the integrated IMF weighted by the mass yield of a 
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
 * header: ccsne.h 
 */ 
extern double *IMFintegrated_fractional_yield_numerator(char *file, char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, 
	long Nmax, long Nmin) {

	/* 
	 * Initialize these variables globally. This is such that the functions 
	 * which execute numerical quadrature can accept only one parameter - the 
	 * stellar mass. 
	 */ 

	GRIDSIZE = line_count(file) - header_length(file); 
	GRID = cc_yield_grid(file); 

	double *numerator; 
	if (!strcmp(IMF, "kroupa")) {
		numerator = quad(yield_weighted_kroupa01, m_lower, m_upper, tolerance, 
			method, Nmax, Nmin); 
	} else if (!strcmp(IMF, "salpeter")) {
		numerator = quad(yield_weighted_salpeter55, m_lower, m_upper, tolerance, 
			method, Nmax, Nmin); 
	} else { 
		/* Would be caught by python anyway, included as failsafe */ 
		return NULL; /* Error: unrecognized IMF */ 
	} 

	free(GRID); 
	GRIDSIZE = 0; 
	return numerator; 

} 

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
 * header: ccsne.h 
 */ 
extern double *IMFintegrated_fractional_yield_denominator(char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, long Nmax, 
	long Nmin) { 

	if (!strcmp(IMF, "kroupa")) {
		return quad(mass_weighted_kroupa01, m_lower, m_upper, tolerance, 
			method, Nmax, Nmin); 
	} else if (!strcmp(IMF, "salpeter")) {
		return quad(mass_weighted_salpeter55, m_lower, m_upper, tolerance, 
			method, Nmax, Nmin); 
	} else {
		/* Would be caught by python anyway, included as failsafe */ 
		return NULL; /* Error: unrecognized IMF */ 
	} 

}

/* 
 * Interpolates the mass yield of a given element from core-collapse supernovae 
 * between masses sampled on the grid 
 * 
 * Parameters 
 * ========== 
 * m: 		The mass of a star whose yield is to be interpolated 
 * 
 * Returns 
 * ======= 
 * The interpolated yield in Msun 
 */ 
static double interpolate_yield(double m) {

	if (m < CC_MIN_STELLAR_MASS) {
		return 0; 
	} else {
		int i; 
		for (i = 0; i < GRIDSIZE; i++) {
			/* if the mass itself is on the grid, just return that yield */ 
			if (m == GRID[i][0]) {
				return GRID[i][1]; 
			} else {
				continue; 
			} 
		} 

		/* 
		 * Can't simply call get_bin_number because GRID is 2-dimensional 
		 */
		for (i = 0; i < GRIDSIZE - 1; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return interpolate(GRID[i][0], GRID[i + 1][0], GRID[i][1], 
					GRID[i + 1][1], m); 
			} else {
				continue; 
			} 
		} 

		/* 
		 * If the code gets to this point, the mass is above the grid. In that 
		 * case, python will raise a warning, and we automatically extrapolate 
		 * yield linearly from the bottom two elements on the grid. 
		 */ 
		return interpolate(GRID[GRIDSIZE - 2][0], GRID[GRIDSIZE - 1][0], 
			GRID[GRIDSIZE - 2][1], GRID[GRIDSIZE - 1][1], m); 
	}

} 

/* 
 * The Kroupa IMF weighted by the mass yield of a given element from the CCSN 
 * of a star of mass m. 
 * 
 * Parameters 
 * ========== 
 * m: 		The mass of the exploding star in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the yield weighted Kroupa IMF up to its normalization. 
 * 
 * References 
 * ========== 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double yield_weighted_kroupa01(double m) {

	return interpolate_yield(m) * kroupa01(m); 

} 

/* 
 * The Salpeter IMF weighted by the mass yield of a given element from the CCSN 
 * of a star of mass m. 
 * 
 * Parameters 
 * ========== 
 * m: 		The mass of the exploding star in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the yield weighted Salpeter IMF up to its normalization 
 * 
 * References 
 * ========== 
 * Salpeter (1955), ApJ, 121, 161 
 */ 
static double yield_weighted_salpeter55(double m) {

	return interpolate_yield(m) * salpeter55(m); 

}

/* 
 * The Kroupa IMF weighted by stellar mass. 
 * 
 * Parameters 
 * ========== 
 * m: 		The stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the mass weighted Kroupa IMF up to its normalization. 
 * 
 * References 
 * ========== 
 * Kroupa (2001), MNRAS, 322, 231 
 */ 
static double mass_weighted_kroupa01(double m) {

	return m * kroupa01(m); 

} 

/* 
 * The Salpeter IMF weighted by stellar mass. 
 * 
 * Parameters 
 * ========== 
 * m: 		The stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the mass weighted Salpeter IMF up to its normalization. 
 * 
 * References 
 * ========== 
 * Salpeter (1955), ApJ, 121, 161 
 */ 
static double mass_weighted_salpeter55(double m) {

	return m * salpeter55(m); 

}


