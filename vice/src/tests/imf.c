/* 
 * This file implements tests of the core routines of the IMF object. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "../imf.h" 
#include "../utils.h" 
#include "imf.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double test_imf(double m); 
static IMF_ *get_test_imf(void); 

/* 
 * TEST_IMF_MAX_MASS:	The maximum stellar mass of the test case IMF 
 * TEST_IMF_MIN_MASS: 	The minimum stellar mass of the test case IMF 
 */ 
static double TEST_IMF_MAX_MASS = 100; 
static double TEST_IMF_MIN_MASS = 0.08; 


/* 
 * Test the function which sets the mass distribution 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: imf.h 
 */ 
extern unsigned short test_imf_set_mass_distribution(void) {

	/* Set the mass distribution according to custom test case ... */ 
	IMF_ *test = get_test_imf(); 
	if (set_test_custom_mass_distribution(test)) {
		imf_free(test); 
		return 0u; 
	} else {} 

	/* 
	 * ... and ensure that it matches the value of the function at each sampled 
	 * stellar mass 
	 */ 
	unsigned long i; 
	for (i = 0ul; i < n_mass_bins(*test); i++) {
		if ((*test).mass_distribution[i] != test_imf(TEST_IMF_MIN_MASS + 
			IMF_STEPSIZE * i)) { 
			imf_free(test); 
			return 0u; 
		} else {} 
	} 
	imf_free(test); 
	return 1u; 

}


/* 
 * Test the function which determines the number of mass bins in an IMF object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: imf.h  
 */ 
extern unsigned short test_n_mass_bins(void) { 

	IMF_ *test = get_test_imf(); 
	unsigned short result = ( 
		/* right-hand side is return statement of function w/known values */ 
		n_mass_bins(*test) == 1l + ((TEST_IMF_MAX_MASS - TEST_IMF_MIN_MASS) / 
			IMF_STEPSIZE) 
	); 
	imf_free(test); 
	return result; 

} 


/* 
 * Test the function which evaluates an IMF object at a given mass 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: imf.h 
 */ 
extern unsigned short test_imf_evaluate(void) {

	IMF_ *test = get_test_imf(); 
	strcpy(test -> spec, "kroupa"); 
	if (imf_evaluate(*test, 1) != kroupa01(1)) {
		imf_free(test); 
		return 0u; 
	} else {} 
	strcpy(test -> spec, "salpeter"); 
	if (imf_evaluate(*test, 1) != salpeter55(1)) {
		imf_free(test); 
		return 0u; 
	} else {} 
	strcpy(test -> spec, "custom"); 


	if (set_test_custom_mass_distribution(test)) { 
		imf_free(test); 
		return 0u; 
	} else {} 

	/* 
	 * Ensure that it evaluates to the right values, and interpolates properly 
	 * between elements of the grid, also returning 0 outside the grid 
	 */ 
	unsigned long i; 
	for (i = 0ul; i < n_mass_bins(*test); i++) { 
		if (absval(
			imf_evaluate(*test, TEST_IMF_MIN_MASS + IMF_STEPSIZE * i) / 
			(*test).mass_distribution[i] - 1)) { 
			imf_free(test); 
			return 0u; 

		} else {} 
	} 

	if (imf_evaluate(*test, TEST_IMF_MIN_MASS + 0.5 * IMF_STEPSIZE) != 
		interpolate(TEST_IMF_MIN_MASS, TEST_IMF_MIN_MASS + IMF_STEPSIZE, 
			(*test).mass_distribution[0], (*test).mass_distribution[1], 
			TEST_IMF_MIN_MASS + 0.5 * IMF_STEPSIZE)) { 
		imf_free(test); 
		return 0u; 
	} else {
		imf_free(test); 
		return 1u; 
	}

} 


/* 
 * Test the built-in Salpeter (1955) IMF 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * References 
 * ========== 
 * Salpeter (1955), ApJ, 121, 161 
 * 
 * header: imf.h 
 */ 
extern unsigned short test_salpeter55(void) {

	return (
		salpeter55(1) == 1 && 
		salpeter55(2) == pow(2, -2.35) && 
		salpeter55(-1) == -1 
	); 

} 


/* 
 * Test the built-in Kroupa (2001) IMF 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * References 
 * ========== 
 * Kroupa (2001), MNRAS, 322, 231 
 * 
 * header: imf.h 
 */ 
extern unsigned short test_kroupa01(void) { 

	return ( 
		/* normalization factors appear due to piece-wise nature */
		kroupa01(0.05) == pow(0.05, -0.3) && 
		kroupa01(0.1) == 0.08 * pow(0.1, -1.3) && 
		kroupa01(1) == 0.04 
	); 

} 


/* 
 * Sets a custom mass distribution according to test_imf 
 * 
 * Returns 
 * ======= 
 * The value of imf_set_mass_distribution at vice/src/imf.h 
 * 
 * header: imf.h 
 */ 
extern unsigned short set_test_custom_mass_distribution(IMF_ *test) {

	unsigned long i; 
	double *mass_dist = (double *) malloc (n_mass_bins(*test) * 
		sizeof(double)); 
	for (i = 0ul; i < n_mass_bins(*test); i++) {
		mass_dist[i] = test_imf(TEST_IMF_MIN_MASS + IMF_STEPSIZE * i); 
	} 
	return imf_set_mass_distribution(test, mass_dist); 

} 


/* 
 * A test custom IMF with slope -2 
 */ 
static double test_imf(double m) {

	/* A top-heavy power-law IMF */ 
	return pow(m, -2); 

} 


/* 
 * Get the test IMF object 
 */ 
static IMF_ *get_test_imf(void) { 

	return imf_initialize(TEST_IMF_MIN_MASS, TEST_IMF_MAX_MASS); 

}

