/*
 * This script handles the numerical implementation of yield-weighted 
 * integration of the IMF. 
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cc_yields.h"
#include "io.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double weighted_kroupa_integrand(double m);
static double weighted_salpeter_integrand(double m);
static double kroupa_integrand(double m);
static double salpeter_integrand(double m);

/* 
 * These variables are declared globally in this file because it is easier for 
 * quadrature functions to be able to access them while still only taking one 
 * parameter. They're initialized in the numerator function, because that is 
 * the first routine that is called by Python. 
 * 
 * GRID: 		The stellar mass - element yield itself 
 * GRIDSIZE:	The number of stellar masses on which the yield grid is sampled 
 */
static double **GRID;
static int GRIDSIZE = 0; 

/*
 * Returns the yield-weighted integrated IMF 
 * 
 * Args:
 * =====
 * file:		The nme of the data file containing the grid
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * lower:		The lower mass limit on star formation in units of Msun
 * upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins
 * 
 * header: cc_yields.h 
 */
extern double *numerator(char *file, char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin) {

	GRIDSIZE = gridsize(file);		// Determine the gridsize globally 
	GRID = yields(file); 			// fill the grid 
	double *num;
	if (!strcmp(IMF, "kroupa")) {
		/* Assume a Kroupa IMF, weight by the yield, and integrate */ 
		num = quad(weighted_kroupa_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else if (!strcmp(IMF, "salpeter")) {
		/* Assume a Salpeter IMF, weight by the yield, and integrate */ 
		num = quad(weighted_salpeter_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else {
		/* This should be caught by Python anyway, included as failsafe */ 
		printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
		printf("giganano9@gmail.com.\n");
		free(GRID);
		exit(0);
	}
	/* Free up the memory and return the results */ 
	free(GRID);
	GRIDSIZE = 0; 
	return num;

}

/*
 * Returns the mass-weighted integrated IMF 
 * 
 * Args:
 * =====
 * IMF:			The IMF to use ('kroupa' or 'salpeter')
 * lower:		The lower mass limit on star formation in units of Msun
 * upper:		The upper mass limit on star formation in units of Msun
 * tolerance:	The maximum fractional error to allow
 * method:		The method of quadrature to use
 * Nmax:		Maximum number of bins (safeguard against divergent solns)
 * Nmin:		Minimum number of bins
 * 
 * header: cc_yields.h 
 */
extern double *denominator(char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin) {

	if (!strcmp(IMF, "kroupa")) {
		/* Assume a Kroupa IMF, weight by the mass, and integrate */ 
		return quad(kroupa_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else if (!strcmp(IMF, "salpeter")) {
		/* Assume a Salpeter IMF, weight by the mass, and integrate */ 
		return quad(salpeter_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else {
		/* This should be caught by Python anyway, included as a failsafe */ 
		printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
		printf("giganano9@gmail.com.\n");
		exit(0);
	}

}

/* 
 * Interpolates the mass yield of an element from core-collapse supernovae 
 * between masses sampled on a grid 
 * 
 * Args:
 * =====
 * m:			The mass of a star whose yield is to be interpolated 
 */ 
static double interpolate_yield(double m) {

	if (m < 8) {	// Stars below 8 Msun do not explode as CCSNe in VICE 
		return 0;
	} else {
		int i;
		for (i = 0; i < GRIDSIZE; i++) {
			/* If the mass is itself on the grid, just return that yield */ 
			if (m == GRID[i][0]) {
				return GRID[i][1];
			} else {
				continue;
			}
		}
		/* 
		 * Go through each element on the grid, and the mass is between two 
		 * adjacent elements, interpolate between those two masses 
		 */
		for (i = 0; i < GRIDSIZE - 1; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return (GRID[i + 1][1] - GRID[i][1]) / (GRID[i + 1][0] - 
					GRID[i][0]) * (m - GRID[i][0]) + GRID[i][1];
			} else {
				continue;
			}
		}
		/* 
		 * If the code gets to this point, the mass is above the grid. In 
		 * that case, Python will raise a warning, and we automatically 
		 * extrapolate the yield linearly from the bottom two elements on 
		 * the grid 
		 */ 
		return ((GRID[GRIDSIZE - 1][1] - GRID[GRIDSIZE - 2][1]) / 
			(GRID[GRIDSIZE - 1][0] - GRID[GRIDSIZE - 2][0]) * 
			(m - GRID[GRIDSIZE - 1][0]) + GRID[GRIDSIZE - 1][1]);
	}

}

/* 
 * Returns the Kroupa integrand weighted by the mass yield of a given element 
 * 
 * Args:
 * =====
 * m:			The stellar mass of stars exploding as CCSNe 
 */ 
static double weighted_kroupa_integrand(double m) {

	return interpolate_yield(m) * kroupa(m);

}

/* 
 * Returns the Salpeter integrand weighted by the mass yield of a given element 
 * 
 * Args:
 * =====
 * m:			The stellar mass of stars exploding as CCSNe 
 */ 
static double weighted_salpeter_integrand(double m) {

	return interpolate_yield(m) * salpeter(m);

}

/* 
 * Returns the Kroupa integrand weighted by stellar mass 
 * 
 * Args:
 * =====
 * m: 			The stellar mass in Msun 
 */
static double kroupa_integrand(double m) {

	return m * kroupa(m);

}

/* 
 * Returns the Salpeter integrand weighted by the stellar mass 
 * 
 * Args:
 * =====
 * m:			The stellar mass in Msun
 */
static double salpeter_integrand(double m) {

	return m * salpeter(m);

}

