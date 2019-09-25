/* 
 * This file implements the enrichment of arbitrary elements from core 
 * collapse supernovae (CCSNe). 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include "ccsne.h" 
#include "io.h" 
#include "imf.h" 
#include "utils.h" 
#include "quadrature.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double y_cc_numerator(double m); 
static double y_cc_denominator(double m); 
static double interpolate_yield(double m); 
static double get_explodability_fraction(double m); 
#if 0 
static double yield_weighted_kroupa01(double m); 
static double yield_weighted_salpeter55(double m); 
static double mass_weighted_kroupa01(double m); 
static double mass_weighted_salpeter55(double m); 
#endif 

/* 
 * These variables are declared globally in this file because it is easier for 
 * quadrature functions to be able to access them while still only taking one 
 * parameter. 
 * 
 * GRID: 			The stellar mass - element yield itself 
 * GRIDSIZE:		The number of stellar masses on which the yield grid is 
 * 					sampled 
 * MASS_RANGES: 	Stellar initial mass ranges passed from the user for 
 * 					stellar explodability prescription 
 * EXPLODABILITY: 	The fractions of stars that explode in those mass ranges 
 */
static double **GRID; 
static unsigned int GRIDSIZE = 0; 
static unsigned int N_MASSES = 0; 
static double *MASSES; 
static double *EXPLODABILITY; 
static IMF_ *adopted_imf = NULL; 

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
	unsigned long num_grid_elements = (long) (
		(CC_YIELD_GRID_MAX - CC_YIELD_GRID_MIN) / CC_YIELD_STEP
	) + 1l; 

	/* Fill the grid starting at CC_YIELD_GRID_MIN in steps of CC_YIELD_STEP */ 
	unsigned long i; 
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

	if (ccsne_yield != NULL) {

		if ((*ccsne_yield).yield_ != NULL) {
			free(ccsne_yield -> yield_); 
			ccsne_yield -> yield_ = NULL; 
		} else {} 

		if ((*ccsne_yield).grid != NULL) {
			free(ccsne_yield -> grid); 
			ccsne_yield -> grid = NULL; 
		} else {} 

		free(ccsne_yield); 
		ccsne_yield = NULL; 

	} else {} 

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
 * The rate of mass enrichment in Msun/Gyr. 
 * 
 * header: ccsne.h 
 */ 
extern double mdot_ccsne(SINGLEZONE sz, ELEMENT e) {
	
	return (get_cc_yield(e, scale_metallicity(sz, sz.timestep)) * 
		(*sz.ism).star_formation_rate); 

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
 * The interpolated yield off of the stored yield grid within the ELEMENT 
 * struct. 
 * 
 * header: ccsne.h 
 */ 
extern double get_cc_yield(ELEMENT e, double Z) { 

	long lower_bound_idx; 
	if (Z < CC_YIELD_GRID_MIN) {
		/* 
		 * Metallicity below the yield grid. Unless the user changes 
		 * CC_YIELD_GRID_MIN in ccsne.h to something other than zero, this 
		 * would be unphysical. Included as a failsafe for users modifying 
		 * VICE. Interpolate off bottom two elements of yield grid. 
		 */ 
		lower_bound_idx = 0l; 
	} else if (CC_YIELD_GRID_MIN <= Z && Z <= CC_YIELD_GRID_MAX) { 
		/* 
		 * Metallicity on the grid. This will always be true for simulations 
		 * even remotely realistic without modified grid parameters. 
		 * Interpolate off neighbroding elements of yield grid. 
		 */ 
		lower_bound_idx = (long) (Z / CC_YIELD_STEP); 
	} else { 
		/* 
		 * Metallicity above the grid. Without modified grid parameters, this 
		 * is unrealistically high, but included as a failsafe against 
		 * segmentation faults. Interpolate off top two elements of yield 
		 * grid. 
		 */ 
		lower_bound_idx = (long) (CC_YIELD_GRID_MAX / CC_YIELD_STEP) - 1l; 
	} 

	return interpolate(
		lower_bound_idx * CC_YIELD_STEP, 
		lower_bound_idx * CC_YIELD_STEP + CC_YIELD_STEP, 
		(*e.ccsne_yields).yield_[lower_bound_idx], 
		(*e.ccsne_yields).yield_[lower_bound_idx + 1l], 
		Z
	); 

} 

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
 * header: ccsne.h 
 */ 
extern void set_explodability_criteria(double *masses, unsigned int n_masses, 
	double *explodability) {

	/* Allocate memory, copy the number of masses on the grid */ 
	N_MASSES = n_masses; 
	MASSES = (double *) malloc (n_masses * sizeof(double)); 
	EXPLODABILITY = (double *) malloc ((n_masses - 1) * sizeof(double)); 

	/* 
	 * Copy over each mass range, and set the explodability equal to 1 in 
	 * ranges where the user didn't specify an explodability fraction. 
	 */ 
	unsigned int i; 
	for (i = 0; i < n_masses; i++) { 
		MASSES[i] = masses[i]; 
	} 
	for (i = 0; i < n_masses - 1; i++) { /* n_masses always divisible by 2 */ 
		if (i % 2) { 
			EXPLODABILITY[i] = 1; 
		} else { 
			EXPLODABILITY[i] = explodability[i / 2]; 
		} 
	} 

	#if 0
	printf("Testing\n"); 
	printf("========================================\n"); 
	for (i = 0; i < n_masses; i++) {
		printf("MASSES[%d] = %g\n", i, MASSES[i]); 
	} 
	for (i = 0; i < n_masses - 1; i++) {
		printf("EXPLODABILITY[%d] = %g\n", i, EXPLODABILITY[i]); 
	}
	#endif 

} 

/* 
 * Determines the fraction of stars at the stellar mass m in Msun that explode 
 * according to the user's explodability criteria. 
 * 
 * Parameters 
 * ========== 
 * m: 		The stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The specified fraction of stars that explode. 
 */ 
static double get_explodability_fraction(double m) {

	long bin = get_bin_number(MASSES, N_MASSES, m); 
	if (bin != -1l) {
		return EXPLODABILITY[bin]; 
	} else {
		return 1; 
	}

} 

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
 * 3 on an unrecognized IMF, otherwise the value returned by quad (see 
 * quadrature.h). 
 * 
 * header: ccsne.h 
 */ 
extern unsigned short IMFintegrated_fractional_yield_numerator(
	INTEGRAL *intgrl, IMF_ *imf, char *file) {

	/* 
	 * Initialize these variables globally. This is such that the functions 
	 * which execute numerical quadrature can accept only one parameter - the 
	 * stellar mass. 
	 */ 
	GRIDSIZE = line_count(file) - header_length(file); 
	GRID = cc_yield_grid(file); 
	adopted_imf = imf; 

	#if 0 
	printf("intgrl: %p\n", (void *) intgrl); 
	printf("imf: %p\n", (void *) imf); 
	printf("imf.spec (%p): %s\n", (void *) (*imf).spec, (*imf).spec); 
	printf("imf.mass_distribution: %p\n", (void *) (*imf).mass_distribution); 
	printf("file (%p): %s\n", (void *) file, file); 
	#endif 

	#if 0
	switch (checksum(IMF)) {

		case KROUPA: 
			intgrl -> func = &yield_weighted_kroupa01; 
			break; 

		case SALPETER: 
			intgrl -> func = &yield_weighted_salpeter55; 
			break; 

		default: 
			free(MASSES); 
			free(EXPLODABILITY); 
			free(GRID); 
			GRIDSIZE = 0; 
			N_MASSES = 0; 
			return 3; 

	} 
	#endif 

	intgrl -> func = &y_cc_numerator; 
	int x = quad(intgrl); 
	free(MASSES); 
	free(EXPLODABILITY); 
	free(GRID); 
	intgrl -> func = NULL; 
	adopted_imf = NULL; 
	GRIDSIZE = 0; 
	N_MASSES = 0; 
	return x; 

}

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
 * header: ccsne.h 
 */ 
extern unsigned short IMFintegrated_fractional_yield_denominator(
	INTEGRAL *intgrl, IMF_ *imf) {

	#if 0 
	switch (checksum(IMF)) {

		case KROUPA: 
			intgrl -> func = &mass_weighted_kroupa01; 
			break; 

		case SALPETER: 
			intgrl -> func = &mass_weighted_salpeter55; 
			break; 

		default: 
			/* would be caught by python anyway, included as failsafe */ 
			return 3; 

	} 
	#endif 
	
	adopted_imf = imf; 
	intgrl -> func = &y_cc_denominator; 
	int x = quad(intgrl); 
	intgrl -> func = NULL; 
	adopted_imf = NULL; 
	return x; 
	// return quad(intgrl); 

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
		unsigned int i; 
		double explosion_fraction = get_explodability_fraction(m); 
		for (i = 0; i < GRIDSIZE; i++) {
			/* if the mass itself is on the grid, just return that yield */ 
			if (m == GRID[i][0]) {
				return explosion_fraction * GRID[i][1]; 
			} else {
				continue; 
			} 
		} 

		/* 
		 * Can't simply call get_bin_number because GRID is 2-dimensional 
		 */
		for (i = 0; i < GRIDSIZE - 1; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return explosion_fraction * interpolate(GRID[i][0], 
					GRID[i + 1][0], GRID[i][1], GRID[i + 1][1], m); 
			} else {
				continue; 
			} 
		} 

		/* 
		 * If the code gets to this point, the mass is above the grid. In that 
		 * case, python will raise a warning, and we automatically extrapolate 
		 * yield linearly from the bottom two elements on the grid. 
		 */ 
		return explosion_fraction * interpolate(GRID[GRIDSIZE - 2][0], 
			GRID[GRIDSIZE - 1][0], GRID[GRIDSIZE - 2][1], 
			GRID[GRIDSIZE - 1][1], m); 
	}

} 

/*
 * The integrand of the numerator of the IMF integrated fractional yield. 
 * 
 * Paremeters 
 * ========== 
 * m: 		A stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of y(x) * dN/dm 
 */ 
static double y_cc_numerator(double m) { 

	return interpolate_yield(m) * imf_evaluate(*adopted_imf, m); 

} 

/* 
 * The integrand of the denominator of the IMF integrated fractional yield 
 * 
 * Parameters 
 * ========== 
 * m: 		A stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of m * dN/dm 
 */ 
static double y_cc_denominator(double m) {

	return m * imf_evaluate(*adopted_imf, m); 

}

#if 0
extern double *IMFintegrated_fractional_yield_numerator(char *file, char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, 
	unsigned long Nmax, unsigned long Nmin) {

	/* 
	 * Initialize these variables globally. This is such that the functions 
	 * which execute numerical quadrature can accept only one parameter - the 
	 * stellar mass. 
	 */ 

	GRIDSIZE = line_count(file) - header_length(file); 
	GRID = cc_yield_grid(file); 
	double (*yield_weighted_IMF) (double); 

	switch (checksum(IMF)) {

		case KROUPA: 
			yield_weighted_IMF = &yield_weighted_kroupa01; 
			break; 

		case SALPETER: 
			yield_weighted_IMF = &yield_weighted_salpeter55; 
			break; 

		default: 
			free(GRID); 
			GRIDSIZE = 0; 
			return NULL; 

	} 

	double *numerator = quad(yield_weighted_IMF, m_lower, m_upper, tolerance, 
		method, Nmax, Nmin); 
	free(GRID); 
	GRIDSIZE = 0; 
	return numerator; 

	#if 0
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
	#endif 

} 

extern double *IMFintegrated_fractional_yield_denominator(char *IMF, 
	double m_lower, double m_upper, double tolerance, char *method, 
	unsigned long Nmax, unsigned long Nmin) { 

	double (*mass_weighted_IMF) (double); 

	switch (checksum(IMF)) { 

		case KROUPA: 
			mass_weighted_IMF = &mass_weighted_kroupa01; 
			break; 

		case SALPETER: 
			mass_weighted_IMF = &mass_weighted_salpeter55; 
			break; 

		default: 
			/* would be caught by python anyway, included as failsafe */ 
			return NULL; 	/* Error: unrecognized IMF */ 

	} 

	return quad(mass_weighted_IMF, m_lower, m_upper, tolerance, 
		method, Nmax, Nmin); 

	#if 0
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
	#endif 

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
#endif 


