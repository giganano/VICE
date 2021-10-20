/*
 * This file implements testing of the MDF routines in the parent directory.
 */

#include <math.h>
#include "../../utils.h"
#include "../mdf.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static unsigned short all_nan_or_single_nonzero(double *arr,
	unsigned long length);


/*
 * Performs the separation test on the tracers_MDF function in the parent
 * directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: mdf.h
 */
extern unsigned short separation_test_tracers_MDF(MULTIZONE *mz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		status &= all_nan_or_single_nonzero(
			(*(*(*mz).zones[0]).mdf).abundance_distributions[i],
			(*(*(*mz).zones[0]).mdf).n_bins
		);
		status &= 1 - all_nan_or_single_nonzero(
			(*(*(*mz).zones[1]).mdf).abundance_distributions[i],
			(*(*(*mz).zones[1]).mdf).n_bins
		);
		if (!status) break;
	}

	for (i = 0u; i < choose((*(*mz).zones[0]).n_elements, 2); i++) {
		/*
		 * Can't make any claims about a non-zero width abundance ratio
		 * distribution in the quiescent zone -> Sr and Fe produce a zero-width
		 * distribution with default yields and parameters.
		 */
		status &= all_nan_or_single_nonzero(
			(*(*(*mz).zones[0]).mdf).ratio_distributions[i],
			(*(*(*mz).zones[0]).mdf).n_bins
		);
		if (!status) break;
		
	}

	return status;

}


/*
 * Determines if an array is either entirely NaN's or only one nonzero.
 *
 * Parameters
 * ==========
 * arr: 		The array to run the check on
 * length: 		The number of elements of the array
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: mdf.h
 */
static unsigned short all_nan_or_single_nonzero(double *arr,
	unsigned long length) {

	unsigned long i, all_nan = 1ul, n_nonzeroes = 0ul;
	for (i = 0ul; i < length; i++) {
		all_nan &= (unsigned long) isnan(arr[i]);
		if (arr[i]) n_nonzeroes++;
	}
	return all_nan || n_nonzeroes == 1ul;

}

