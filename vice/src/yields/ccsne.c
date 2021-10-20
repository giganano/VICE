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
#include "../stats.h"
#include "ccsne.h"

/* ---------- static function comment headers not duplicated here ---------- */
static void setup_calculation(IMF_ *imf, CALLBACK_1ARG *explodability,
	char *path, const unsigned short wind, char *element);
static void zero_wind_yield_grid(void);
static double interpolate_yield(double m);
static double y_cc_numerator(double m);
static double y_cc_denominator(double m);


/*
 * These variables are declared globally in this file because it is easier for
 * quadrature functions to be able to access them while still only taking one
 * parameter.
 *
 * GRID: 			The stellar mass - element yield from the explosion
 * WIND: 			The stellar mass - element yield from the wind
 * GRIDSIZE:		The number of stellar masses on which the yield grid is
 * 					sampled
 * IMF: 			The assumed stellar IMF's corresponding object
 * EXPLODABILITY: 	The fractions of stars that explode in those mass ranges
 * Z_PROGENITOR: 	Z_x of the progenitor stars for the element x.
 * WEIGHT_INITIAL: 	A boolean int describing whether or not to weight the
 * 					initial composition by explodability
 * TESTING: 		A global testing status: 1 if testing, 0 if not.
 */
static double **GRID;
static double **WIND;
static unsigned int GRIDSIZE = 0;
static IMF_ *IMF = NULL;
static CALLBACK_1ARG *EXPLODABILITY = NULL;
static double Z_PROGENITOR;
static unsigned short WEIGHT_INITIAL;


/*
 * Weight the initial composition of each star by explodability. This ensures
 * that net yields are not reported as negative when the study did not
 * separate wind and explosive yields.
 *
 * Parameters
 * ==========
 * 1 to weight the initial composition by explodability, 0 to not.
 *
 * header: ccsne.h
 */
extern void weight_initial_by_explodability(unsigned short weight) {

	WEIGHT_INITIAL = weight;

}


/*
 * Set the value of the progenitor stars abundance by mass Z_x for the element
 * x whose net yield is being calculated.
 *
 * Parameters
 * ==========
 * Z: 		The initial abundance Z_x itself
 *
 * header: ccsne.h
 */
extern void set_Z_progenitor(double Z) {

	Z_PROGENITOR = Z;

}


/*
 * Determine the value of the integrated IMF weighted by the mass yield of a
 * given element, up to the normalization of the IMF.
 *
 * Parameters
 * ==========
 * intgrl: 			The integral object for the numerator of the yield
 * imf:				The associated IMF object
 * explodability: 	Stellar explodability as a function of mass
 * path:			The nme of the data file containing the grid
 * wind: 			Boolean int describing whether or not to include winds
 * element: 		The symbol of the element
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
	char *path, const unsigned short wind, char *element) {

	setup_calculation(imf, explodability, path, wind, element);
	intgrl -> func = &y_cc_numerator;
	int x = quad(intgrl);
	free(GRID);
	free(WIND);
	intgrl -> func = NULL;
	GRIDSIZE = 0;
	IMF = NULL;
	return x;

}


/*
 * Setup the yield calculation by initializing all of the necessary global
 * variables.
 *
 * Parameters
 * ==========
 * imf:				The associated IMF object
 * explodability: 	Stellar explodability as a function of mass
 * path:			The nme of the data file containing the grid
 * wind: 			Boolean int describing whether or not to include winds
 * element: 		The symbol of the element
 */
static void setup_calculation(IMF_ *imf, CALLBACK_1ARG *explodability,
	char *path, const unsigned short wind, char *element) {

	/*
	 * Initialize these variables globally. This is such that the function
	 * which executes numerical quadrature can accept only one parameter - the
	 * ZAMS mass of the progenitor.
	 */
	char *file = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char));
	strcpy(file, path);
	strcat(file, "explosive/");
	strcat(file, element);
	strcat(file, ".dat");

	GRIDSIZE = line_count(file) - header_length(file);
	GRID = cc_yield_grid(file);

	if (wind) {
		char *wind = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char));
		strcpy(wind, path);
		strcat(wind, "wind/");
		strcat(wind, element);
		strcat(wind, ".dat");
		WIND = cc_yield_grid(wind);
		free(wind);
	} else {
		zero_wind_yield_grid();
	}

	IMF = imf;
	EXPLODABILITY = explodability;

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
 * Initialize the wind yield to a grid of zeroes in the event that the user
 * is neglecting the wind yields in this calculation.
 */
static void zero_wind_yield_grid(void) {

	unsigned int i;
	WIND = (double **) malloc (GRIDSIZE * sizeof(double *));
	for (i = 0u; i < GRIDSIZE; i++) {
		WIND[i] = (double *) malloc (2 * sizeof(double));
		WIND[i][0] = GRID[i][0];
		WIND[i][1] = 0.0;
	}

}


/*
 * Interpolates the mass yield of a given element from core-collapse supernovae
 * between masses sampled on the grid, taking into account both explosive and
 * wind yields.
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

		/*
		 * The corrective term to subtract that accounts for initial abundances
		 * in calculating net yields
		 */
		double initial = Z_PROGENITOR * m;
		if (WEIGHT_INITIAL) initial *= callback_1arg_evaluate(
			*EXPLODABILITY, m);

		unsigned int i;
		for (i = 0; i < GRIDSIZE; i++) {
			/* if the mass itself is on the grid, just return that yield */
			if (m == GRID[i][0]) {
				return (
					callback_1arg_evaluate(*EXPLODABILITY, m) * GRID[i][1] +
					WIND[i][1] - initial
				);
			} else {
				continue;
			}
		}

		/*
		 * Can't simply call get_bin_number because GRID is 2-dimensional
		 */
		for (i = 0; i < GRIDSIZE - 1; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return (
					callback_1arg_evaluate(*EXPLODABILITY, m) *
					interpolate(GRID[i][0], GRID[i + 1][0], GRID[i][1],
						GRID[i + 1][1], m) +
					interpolate(WIND[i][0], WIND[i + 1][0], WIND[i][1],
						WIND[i + 1][1], m) -
					initial
				);
			} else {
				continue;
			}
		}

		/*
		 * If the code gets to this point, the mass is above the grid. In that
		 * case, python will raise a warning, and we automatically extrapolate
		 * yield linearly from the bottom two elements on the grid.
		 */
		return (
			callback_1arg_evaluate(*EXPLODABILITY, m) *
			interpolate(GRID[GRIDSIZE - 2][0], GRID[GRIDSIZE - 1][0],
				GRID[GRIDSIZE - 2][1], GRID[GRIDSIZE - 1][1], m) +
			interpolate(WIND[GRIDSIZE - 2][0], WIND[GRIDSIZE - 1][0],
				WIND[GRIDSIZE - 2][1], WIND[GRIDSIZE - 1][1], m) -
			initial
		);
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

