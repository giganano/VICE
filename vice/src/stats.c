
#include <stdlib.h>
#include <math.h>
#include "stats.h"
#include "utils.h"


/*
 * Convert a distribution in a given binspace to a probability distribution
 * function (PDF).
 *
 * Parameters
 * ==========
 * dist:		The values of the distribution itself in each bin
 * bins: 		The bin edges on which the distribution is sampled
 * n_bins: 		The number of bins in the distribution. This is always 1 less
 * 				than the number of bin edges.
 *
 * Returns
 * =======
 * A distribution with the same trends as that which was passed, but whose
 * integral is equal to 1.
 *
 * header: stats.h
 */
extern double *convert_to_PDF(double *dist, double *bins,
	unsigned long n_bins) {

	/* Allocate memory; start counting at zero */
	double sum = 0, *pdf = (double *) malloc (n_bins * sizeof(double));
	unsigned long i;

	/* Add up the area in each bin */
	for (i = 0l; i < n_bins; i++) {
		sum += dist[i] * (bins[i + 1l] - bins[i]);
	}

	/* Divide each element by the value of the integral */
	for (i = 0l; i < n_bins; i++) {
		pdf[i] = dist[i] / sum;
	}

	return pdf;

}

