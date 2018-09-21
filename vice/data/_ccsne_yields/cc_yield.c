
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "cc_yields.h"

static double weighted_kroupa_integrand(double m);
static double weighted_salpeter_integrand(double m);
static double kroupa_integrand(double m);
static double salpeter_integrand(double m);
static double **GRID;

/*
Returns the yield-weighted integrated IMF 

Args:
=====
file:		The nme of the data file containing the grid
IMF:		The IMF to use ('kroupa' or 'salpeter')
lower:		The lower mass limit on star formation in units of Msun
upper:		The upper mass limit on star formation in units of Msun
tolerance:	The maximum fractional error to allow
method:		The method of quadrature to use
Nmax:		Maximum number of bins (safeguard against divergent solns)
Nmin:		Minimum number of bins
*/
extern double *numerator(char *file, char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin) {

	GRID = yields(file);
	if (!strcmp(IMF, "kroupa")) {
		return quad(weighted_kroupa_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else if (!strcmp(IMF, "salpeter")) {
		return quad(weighted_salpeter_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else {
		printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
		printf("giganano9@gmail.com.\n");
		exit(0);
	}
	free(GRID);

}

/*
Returns the mass-weighted integrated IMF 

Args:
=====
IMF:		The IMF to use ('kroupa' or 'salpeter')
lower:		The lower mass limit on star formation in units of Msun
upper:		The upper mass limit on star formation in units of Msun
tolerance:	The maximum fractional error to allow
method:		The method of quadrature to use
Nmax:		Maximum number of bins (safeguard against divergent solns)
Nmin:		Minimum number of bins
*/
extern double *denominator(char *IMF, double lower, double upper, 
	double tolerance, char *method, long Nmax, long Nmin) {

	if (!strcmp(IMF, "kroupa")) {
		return quad(kroupa_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else if (!strcmp(IMF, "salpeter")) {
		return quad(salpeter_integrand, lower, upper, tolerance, 
			method, Nmax, Nmin);
	} else {
		printf("ERROR in IMF-INTEGRATOR. Please submit bug report to ");
		printf("giganano9@gmail.com.\n");
		exit(0);
	}

}

static double interpolate_yield(double m) {

	if (m < 8) {
		return 0;
	} else {
		int i;
		for (i = 0; i < 10; i++) {
			if (m == GRID[i][0]) {
				return GRID[i][1];
			} else {
				continue;
			}
		}
		for (i = 0; i < 9; i++) {
			if (GRID[i][0] < m && m < GRID[i + 1][0]) {
				return (GRID[i + 1][1] - GRID[i][1]) / (GRID[i + 1][0] - 
					GRID[i][0]) * (m - GRID[i][0]) + GRID[i][1];
			} else {
				continue;
			}
		}
		return ((GRID[9][1] - GRID[8][1]) / (GRID[9][0] - GRID[8][0]) * 
			(m - GRID[9][0]) + GRID[9][1]);
	}

}

static double weighted_kroupa_integrand(double m) {

	return interpolate_yield(m) * kroupa(m);

}

static double weighted_salpeter_integrand(double m) {

	return interpolate_yield(m) * salpeter(m);

}

/* mass times the Kroupa IMF */
static double kroupa_integrand(double m) {

	return m * kroupa(m);

}

/* mass times the Salpeter IMF */
static double salpeter_integrand(double m) {

	return m * salpeter(m);

}

