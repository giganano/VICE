/*
 * This script handles the numerical implementation of enrichment by core 
 * collapse supernovae. 
 */

#include <stdlib.h>
#include <math.h>
#include "specs.h"
#include "enrichment.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double interpolate(double x1, double x, double x2, double y1, 
	double y2);

/* 
 * The stepsize of the yield grid. VICE implements core-collapse supernovae 
 * yields as a function of metallicity specified by the user. It then achieves 
 * this in C by simply sampling the function at each 10^-5 step in Z up to 
 * a metallicity of Z = 0.5. This fine of a grid does not consume a prohibitive 
 * amount of memory. 
 */
static double STEPSIZE = 1e-5; 

/*
 * Returns the time-derivative of the mass of an element from CCSNe at the 
 * current timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION structure for the current execution
 * m:			The MODEL structure for the current execution
 * index:		The index of the element 
 * 
 * header: enrichment.h 
 */
extern double mdot_ccsne(INTEGRATION run, MODEL m, int index) {

	/* Scale the metallicity */
	double scaled, solar = 0, z = 0; 
	int i;
	for (i = 0; i < run.num_elements; i++) {
		/* Solar abundance given only tracked elements */ 
		solar += run.elements[i].solar; 
		/* Measured abundance given only tracked elements */
		z += run.elements[i].m_tot / run.MG;
	}
	scaled = m.Z_solar * z / solar;

	/* Get the yield from the metallicity, multiply by SFR, and return. */
	return get_cc_yield(run.elements[index], scaled) * run.SFR;

}

/*
 * Fills the core-collapse yield grid as a function of metallicity up to 
 * Z = 0.5. 
 * 
 * Args:
 * =====
 * run:	A pointer to the INTEGRATION struct for this integration
 * index:	The index of the element to set the yield grid for
 * arr:	The array containing the yield at each sampled metallicity 
 * 
 * header: enrichment.h 
 */
extern int fill_cc_yield_grid(INTEGRATION *run, int index, double *arr) {

	long i, length = (long) (0.5 / STEPSIZE) + 1l; // length of the array 
	ELEMENT *e = &((*run).elements[index]); 
	e -> ccsne_yield = (double *) malloc (length * sizeof(double));
	for (i = 0l; i < length; i++) {
		e -> ccsne_yield[i] = arr[i]; // copy the grid passed from python 
	}
	return 1;

}

/*
 * Gets the CC yield interpolated off of the grid automatically from a 
 * specified metallicity given the stepsize of the grid. 
 * 
 * Args:
 * =====
 * e:		The element struct whose yield is being interpolated
 * Z:		The metallicity of the ISM by mass, properly scaled 
 * 
 * header: enrichment.h
 */
extern double get_cc_yield(ELEMENT e, double Z) {

	return interpolate(
		Z / STEPSIZE * STEPSIZE, 
		Z, 
		Z / STEPSIZE * STEPSIZE + STEPSIZE, 
		e.ccsne_yield[(long) (Z / STEPSIZE)], 
		e.ccsne_yield[(long) (Z / STEPSIZE + 1l)]
	);

}

/*
 * Interpolates a value of y sampled between two values of x. This is the 
 * standard interpolation expression in one dimension determined from the 
 * point-slope form of the equation for a line. 
 * 
 * Args:
 * =====
 * x1: 	The lower sampling point
 * x:		The point of interest
 * x2:		The upper sampling point
 * y1:		The value at the lower sampling point
 * y2:		The value at the upper sampling point
 */
static double interpolate(double x1, double x, double x2, double y1, 
	double y2) {

	return y2 + (y2 - y1) / (x2 - x1) * (x - x1);

}


