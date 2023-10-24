/*
 * This file implements testing of the mass_recycled function in the parent
 * directory.
 */

#include "../../utils.h"
#include "../recycling.h"


/*
 * Performs the quiescence edge-case test on the mass_recycled routine in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short quiescence_test_mass_recycled(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mass_recycled(*sz, (*sz).elements[i]) == 0;
		if (!status) break;
	}
	if (status) status &= mass_recycled(*sz, NULL) == 0;
	return status;

}


/*
 * Performs the max age SSP edge-case test on the mass_recycled function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short max_age_ssp_test_mass_recycled(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mass_recycled(*sz, (*sz).elements[i]) == 0;
		if (!status) break;
	}
	status &= mass_recycled(*sz, NULL) == (
		(*(*sz).ism).star_formation_history[0] * (*sz).dt * (
			(*(*sz).ssp).crf[(*sz).timestep + 1l] -
			(*(*sz).ssp).crf[(*sz).timestep]
		)
	);
	return status;

}


/*
 * Performs the zero age SSP edge-case test on the mass_recycled function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: recycling.h
 */
extern unsigned short zero_age_ssp_test_mass_recycled(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	double sfr = (*(*sz).ism).star_formation_history[(*sz).timestep - 1ul];
	for (i = 0u; i < (*sz).n_elements; i++) {
		/*
		 * The only stellar population to have formed is zero metallicity, so
		 * there shouldn't be any recycled metals...
		 */
		status &= mass_recycled(*sz, (*sz).elements[i]) == 0;
		if (!status) break;
	}
	/* ... but there is recycled gas. */
	status &= mass_recycled(*sz, NULL) == (
		sfr * (*sz).dt * ((*(*sz).ssp).crf[2] - (*(*sz).ssp).crf[1])
	);
	return status;

}

