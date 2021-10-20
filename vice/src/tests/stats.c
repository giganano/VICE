/*
 * This file implements testing of the statistics functions at
 * vice/src/stats.h
 */

#include <stdlib.h>
#include <math.h>
#include "../stats.h"
#include "../utils.h"
#include "stats.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double unnormalized_gaussian(double x);


/*
 * Test the convert to PDF function at vice/src/stats.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: stats.h
 */
extern unsigned short test_convert_to_PDF(void) {

	unsigned short i, n = 1000u;
	double *bins = binspace(-3, 3, n);
	double *centers = bin_centers(bins, n);
	double *gaussian = (double *) malloc (n * sizeof(double));
	for (i = 0u; i < n; i++) {
		gaussian[i] = unnormalized_gaussian(centers[i]);
	}

	double s = 0, *normed = convert_to_PDF(gaussian, bins, n);
	for (i = 0u; i < n; i++) {
		s += normed[i] * (bins[i + 1u] - bins[i]);
	}
	free(bins);
	free(centers);
	free(gaussian);
	free(normed);
	return absval(s - 1) < 1e-15;

}


/*
 * An unnormalized gaussian with dispersion 1.
 *
 * Parameters
 * ==========
 * x: 		The value to evaluate the distribution at
 */
static double unnormalized_gaussian(double x) {

	return exp( -pow(x, 2) );

}

