/* 
 * This file implements the calculations of IMF-averaged yields from core 
 * collapse supernovae (CCSNe). 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include "../callback.h" 
#include "../yields.h" 
#include "../io.h" 
#include "../imf.h" 
#include "../utils.h" 
#include "../ccsne.h" 
#include "ccsne.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static double interpolate_yield(double m); 
static double y_cc_numerator(double m); 
static double y_cc_denominator(double m); 


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
static IMF_ *IMF = NULL; 
static CALLBACK_1ARG *EXPLODABILITY = NULL; 


/* 
 * Determine the value of the integrated IMF weighted by the mass yield of a 
 * given element, up to the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 			The integral object for the numerator of the yield 
 * imf:				The associated IMF object
 * explodability: 	Stellar explodability as a function of mass 
 * file:			The nme of the data file containing the grid 
 * 
 * Returns 
 * ======= 
 * 3 on an unrecognized IMF, otherwise the value returned by quad (see 
 * quadrature.h). 
 * 
 * header: ccsne.h 
 */ 
extern unsigned short IMFintegrated_fractional_yield_numerator(
	INTEGRAL *intgrl, IMF_ *imf, CALLBACK_1ARG *explodability, 
	char *file) { 

	/* 
	 * Initialize these variables globally. This is such that the function 
	 * which execute numerical quadrature can accept only one parameter - the 
	 * stellar mass. 
	 */ 
	GRIDSIZE = line_count(file) - header_length(file); 
	GRID = cc_yield_grid(file); 
	IMF = imf; 
	EXPLODABILITY = explodability; 

	intgrl -> func = &y_cc_numerator; 
	int x = quad(intgrl); 
	free(GRID); 
	intgrl -> func = NULL; 
	GRIDSIZE = 0; 
	IMF = NULL; 
	EXPLODABILITY = NULL; 
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
 * header: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_denominator(
	INTEGRAL *intgrl, IMF_ *imf) { 

	IMF = imf; 
	intgrl -> func = &y_cc_denominator; 
	int x = quad(intgrl); 
	intgrl -> func = NULL; 
	IMF = NULL; 
	return x; 

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
		// double explosion_fraction = get_explodability_fraction(m); 
		for (i = 0; i < GRIDSIZE; i++) {
			/* if the mass itself is on the grid, just return that yield */ 
			if (m == GRID[i][0]) {
				return callback_1arg_evaluate(*EXPLODABILITY, m) * GRID[i][1]; 
			} else { 
				continue; 
			} 
		} 

		/* 
		 * Can't simply call get_bin_number because GRID is 2-dimensional 
		 */
		for (i = 0; i < GRIDSIZE - 1; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return callback_1arg_evaluate(*EXPLODABILITY, m) * 
					interpolate(GRID[i][0], 
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
		return callback_1arg_evaluate(*EXPLODABILITY, m) * interpolate(
			GRID[GRIDSIZE - 2][0], 
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

	return interpolate_yield(m) * imf_evaluate(*IMF, m); 

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

	return m * imf_evaluate(*IMF, m); 

} 

