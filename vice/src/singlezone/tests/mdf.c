/*
 * This file implements testing of the MDF routines in the parent directory
 */

#include <math.h>
#include "../../utils.h"
#include "../mdf.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static unsigned short all_nan_or_single_nonzero(double *arr,
	unsigned long length);


/*
 * Performs the quiescence edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: mdf.h
 */
extern unsigned short quiescence_test_MDF(SINGLEZONE *sz) {

	/*
	 * The value of the metallicity distribution after normalizing to a
	 * simulation in which no stars form will be NaN in all bins for all
	 * reported distributions.
	 */

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		unsigned long j;
		for (j = 0u; j < (*(*sz).mdf).n_bins; j++) {
			status &= isnan((*(*sz).mdf).abundance_distributions[i][j]);
			if (!status) break;
		}
		if (!status) break;
	}
	for (i = 0u; i < choose((*sz).n_elements, 2); i++) {
		unsigned long j;
		for (j = 0u; j < (*(*sz).mdf).n_bins; j++) {
			status &= isnan((*(*sz).mdf).ratio_distributions[i][j]);
			if (!status) break;
		}
		if (!status) break;
	}
	return status;

}


/*
 * Performs the max age SSP edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: mdf.h
 */
extern unsigned short max_age_ssp_test_MDF(SINGLEZONE *sz) {

	/*
	 * The single stellar population formed is zero metallicity, so the
	 * distribution should be the same as in the quiescent case.
	 */
	return quiescence_test_MDF(sz);

}


/*
 * Performs the zero age SSP edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: mdf.h
 */
extern unsigned short zero_age_ssp_test_MDF(SINGLEZONE *sz) {

	/*
	 * The stellar populations formed in the 1 or 2 timesteps after the end
	 * of the simulation may produce enough elements to be above the lower
	 * bound of the MDF, so test for either NaNs or a single nonzero.
	 */
	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= all_nan_or_single_nonzero(
			(*(*sz).mdf).abundance_distributions[i],
			(*(*sz).mdf).n_bins
		);
		if (!status) break;
	}
	for (i = 0u; i < choose((*sz).n_elements, 2); i++) {
		status &= all_nan_or_single_nonzero(
			(*(*sz).mdf).ratio_distributions[i],
			(*(*sz).mdf).n_bins
		);
		if (!status) break;
	}
	return status;

}


/*
 * Determines if an array is full of NaNs or has a single nonzero value.
 *
 * Parameters
 * ==========
 * arr: 	The array itself
 * length: 	The number of element in the array
 *
 * Returns
 * =======
 * 0 if the array has anything other than NaNs or more than one nonzero value.
 * 1 otherwise.
 */
static unsigned short all_nan_or_single_nonzero(double *arr,
	unsigned long length) {

	unsigned long i;
	unsigned short all_nan = 1u, n_nonzeroes = 0u;
	for (i = 0u; i < length; i++) {
		all_nan &= isnan(arr[i]);
		if (arr[i]) n_nonzeroes++;
	}
	return all_nan || n_nonzeroes == 1u;

}

