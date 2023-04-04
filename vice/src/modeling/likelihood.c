/*
 * This file computes an estimate that a datum in some observed space (in
 * practice, always a single star) arose from a model predicted track through
 * that space. The likelihood function implemented is that of Johnson et al. 
 * (2022; see their Appendix A).
 *
 * References
 * ==========
 * Johnson et al. (2022), arxiv:2210.01816
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "likelihood.h"
#include "../objects.h"
#include "../modeling.h"
#include "../stats.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static double chi_squared(DATUM d, TRACK t, const unsigned short idx);
static double corrective_factor(DATUM d, TRACK t, const unsigned short idx);
static MATRIX *trackpoint(TRACK t, const unsigned short idx);
static TRACK *track_subset(DATUM d, TRACK t);
static signed short strindex(char **strlist, char *test,
	unsigned short strlistlength);

/*
 * If the correction for the finite length of a track line segment is ever
 * larger than some predefined threshold, then raise a flag that can be
 * picked up in python and raised as a ScienceWarning.
 *
 * LINE_SEGMENT_CORRECTION_THRESHOLD : the threshold above which the flag will
 * 		be raised.
 * LINE_SEGMENT_LENGTH_FLAG : the flag itself, to be switched to a value of 1
 * 		if the correction ever exceeds the LINE_SEGMENT_CORRECTION_THRESHOLD.
 */
static double LINE_SEGMENT_CORRECTION_THRESHOLD = 0.01;
static unsigned short LINE_SEGMENT_LENGTH_FLAG = 0u;


/*
 * Compute the natural logarithm of the likelihood that a given data vector
 * (in practice, a single star) arose from a model-predicted track through some
 * observed space (in practice, chemical-age space).
 *
 * Parameters
 * ==========
 * d: 		The datum itself as a vector in the observed space
 * t: 		The track itself as a matrix in the observed space. This may contain
 * 			more quantities than are present in the datum. The appropriate
 * 			quantities to base the calculation on will be determined by a
 * 			comparison of the datum and track labels.
 *
 * Returns
 * =======
 * ln L(D_i | M), defined as the line integral of a weighted likelihood
 * estimate along the length of the track. See Johnson et al. (2022) for
 * details.
 *
 * References
 * ==========
 * Johnson et al. (2022), arxiv:2210.01816
 *
 * header: likelihood.h
 */
extern double loglikelihood(DATUM d, TRACK t) {

	matrix_invert(*((MATRIX *) d.cov), (*d.cov).inv);
	unsigned short i;
	double result = 0;

	/*
	 * For a track sampled at n_rows points, there are n_rows - 1 line segments
	 * to marginalize over -- hence the exclusion of one point at the end.
	 */
	for (i = 0u; i < t.n_rows - 1u; i++) {
		double s = t.weights[i] * chi_squared(d, t, i);
		double correction = corrective_factor(d, t, i);
		LINE_SEGMENT_LENGTH_FLAG |= (
			absval(correction - 1) > LINE_SEGMENT_CORRECTION_THRESHOLD);
		s *= correction;
		result += s;
	}
	return log(result);

}


/*
 * Compute chi^2 given a datum and a point along the model-predicted track.
 *
 * Parameters
 * ==========
 * d: 		The datum itself
 * t:		The track itself
 * idx: 	The index of the point along the track to compute chi^2 for
 *
 * Returns
 * =======
 * \chi^2 = \Delta_{ij} C_i^{-1} \Delta_{ij}^T, a conventional matrix operation
 * which arises when the uncertainties on the datum d are a multivariate
 * gaussian.
 */
static double chi_squared(DATUM d, TRACK t, const unsigned short idx) {

	/*
	 * Each matrix operation will allocate memory, so pointers need to be
	 * tracked along the way to be freed later and prevent memory leaks.
	 */
	MATRIX *tpoint = trackpoint(t, idx);
	MATRIX *delta = matrix_subtract(*((MATRIX *) &d), *tpoint, NULL);
	MATRIX *delta_T = matrix_transpose(*delta, NULL);
	MATRIX *first_product = matrix_multiply(*delta, *(*d.cov).inv, NULL);
	MATRIX *second_product = matrix_multiply(*first_product, *delta_T, NULL);
	if ((*second_product).n_rows != 1 || (*second_product).n_cols != 1) {
		fatal_print("%s\n",
			"Chi-squared calculation resulted in a matrix larger than 1x1.");
	} else {
		double result = second_product -> matrix[0][0];
		matrix_free(tpoint);
		matrix_free(delta);
		matrix_free(delta_T);
		matrix_free(first_product);
		matrix_free(second_product);
		return result;
	}

}


/*
 * Compute the corrective factor in the likelihood function accounting for the
 * finite length of a line segment in the track.
 *
 * Parameters
 * ==========
 * d: 		The datum itself
 * t:		The track itself
 * idx: 	The index of the point along the track to compute the corrective
 * 			factor for (i.e., which line segment).
 *
 * Returns
 * =======
 * \beta_{ij}, defined according to equation (A12) in Johnson et al. (2022).
 *
 * References
 * ==========
 * Johnson et al. (2022), arxiv:2210.01816
 */
static double corrective_factor(DATUM d, TRACK t, const unsigned short idx) {

	/*
	 * Each matrix operation will allocate memory, so pointers need to be
	 * tracked along the way to be freed later and prevent memory leaks.
	 */
	MATRIX *tpoint_idx = trackpoint(t, idx);
	MATRIX *tpoint_next = trackpoint(t, idx + 1u);
	MATRIX *delta = matrix_subtract(*((MATRIX *) &d), *tpoint_idx, NULL);
	MATRIX *linesegment = matrix_subtract(*tpoint_next, *tpoint_idx, NULL);
	MATRIX *linesegment_T = matrix_transpose(*linesegment, NULL);
	MATRIX *first_product = matrix_multiply(*delta, *(*d.cov).inv, NULL);
	MATRIX *second_product = matrix_multiply(*first_product, *linesegment_T,
		NULL);
	double a = second_product -> matrix[0][0];
	matrix_free(first_product);
	matrix_free(second_product);
	first_product = matrix_multiply(*delta, *(*d.cov).inv, NULL);
	second_product = matrix_multiply(*first_product, *linesegment_T, NULL);
	double b = second_product -> matrix[0][0];
	matrix_free(first_product);
	matrix_free(second_product);
	matrix_free(linesegment_T);
	matrix_free(linesegment);
	matrix_free(delta);
	matrix_free(tpoint_next);
	matrix_free(tpoint_idx);
	double result = sqrt(PI / (2 * a));
	result *= exp(b * b / (2 * a));
	result *= erf((a - b) / sqrt(2 * a)) - erf(b / sqrt(2 * a));
	return result;

}


/*
 * Obtain the vector for a specific point along the model predicted track.
 *
 * Parameters
 * ==========
 * t: 		The track itself
 * idx: 	The index of the point to take
 *
 * Returns
 * =======
 * The MATRIX object containing the vector of the t_idx'th vertex along the
 * track.
 */
static MATRIX *trackpoint(TRACK t, const unsigned short idx) {

	unsigned short i;
	MATRIX *vector = matrix_initialize(1u, t.n_cols);
	for (i = 0u; i < t.n_cols; i++) vector -> matrix[0][i] = t.data[idx][i];
	return vector;

}


/*
 * Obtain a track object containing only the quantities present in the datum
 * by comparing their column labels.
 *
 * Parameters
 * ==========
 * d: 		The datum itself
 * t:		The model-predicted track, which may have more quantities than are
 * 			available for this particular datum (e.g., an age measurement).
 *
 * Returns
 * =======
 * A new track object whose dimensionality and quantities are a component-wise
 * match to this specific datum. 
 */
static TRACK *track_subset(DATUM d, TRACK t) {

	TRACK *sub = (TRACK *) matrix_initialize(t.n_rows, d.n_cols);
	sub = (TRACK *) realloc (sub, sizeof(TRACK));
	sub -> labels = (char **) malloc ((*sub).n_cols * sizeof(char *));
	unsigned short i, j;
	for (j = 0u; j < (*sub).n_cols; j++) {
		/* idx = the column of the track matrix to copy over to the sub */
		signed short idx = strindex(t.labels, d.labels[j], t.n_cols);
		if (idx == -1) {
			free(sub);
			return NULL;
		} else {
			sub -> labels[j] = (char *) malloc (
				strlen(d.labels[j]) * sizeof(char));
			strcpy(sub -> labels[j], d.labels[j]);
			for (i = 0u; i < t.n_rows; i++) {
				sub -> data[i][j] = t.data[i][j];
			}
		}
	}
	sub -> weights = (double *) malloc ((*sub).n_cols * sizeof(double));
	for (i = 0u; i < t.n_rows; i++) sub -> weights[i] = t.weights[i];
	return sub;

}


/*
 * Determine the index of a string within a list of strings.
 *
 * Parameters
 * ==========
 * strlist: 		The list of strings
 * test: 			The string to look for within strlist
 * strlistlength: 	The number of strings in strlist
 *
 * Returns
 * =======
 * The index i at which !strcmp(strlist[i], test) evaluates to 1. -1 if no such
 * element of strlist passes the test.
 */
static signed short strindex(char **strlist, char *test,
	unsigned short strlistlength) {

	signed short i;
	for (i = 0; i < strlistlength; i++) {
		if (!strcmp(strlist[i], test)) return i;
	}
	return -1;

}

