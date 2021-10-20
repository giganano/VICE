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
	for (i = 0u; i < (*sz).n_elements; i++) {
		double recycled = (
			(*(*sz).ism).star_formation_rate * (*sz).dt *
			(*(*sz).elements[i]).Z[(*sz).timestep] *
			(*(*sz).ssp).crf[1]
		);
		double percent_difference = absval(
			(recycled - mass_recycled(*sz, (*sz).elements[i])) /
			mass_recycled(*sz, (*sz).elements[i])
		);
		status &= percent_difference < 1e-12;
		if (!status) break;
	}
	status &= mass_recycled(*sz, NULL) == (
		(*(*sz).ism).star_formation_rate * (*sz).dt * (*(*sz).ssp).crf[1]
	);
	return status;

}

