/*
 * This file implements testing of the ISM evolution routines at ism.h in
 * the parent directory.
 */

#include <stdlib.h>
#include "../../utils.h"
#include "../ism.h"

static const double INITIAL_ISM_MASS = 6.0e9;


/*
 * Performs the quiescence test on the update_gas_evolution function in the
 * parent directory by ensuring the star formation rate is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short quiescence_test_update_gas_evolution(SINGLEZONE *sz) {

	unsigned short status = (*(*sz).ism).star_formation_rate == 0;
	if (status) {
		/*
		 * Recalculate the ISM mass and compare based on a maximum percent
		 * difference to account for round-off error.
		 */
		double ism_mass = (INITIAL_ISM_MASS +
			(*sz).current_time * (*(*sz).ism).infall_rate);
		double percent_difference = absval(
			((*(*sz).ism).mass - ism_mass) / (*(*sz).ism).mass
		);
		status &= percent_difference < 1e-12;
	} else {}
	return status;

}


/*
 * Performs the max age ssp edge-case test on the update_gas_evolution
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short max_age_ssp_test_update_gas_evolution(SINGLEZONE *sz) {

	unsigned short status = (*(*sz).ism).star_formation_rate == 0;
	if (status) {
		/*
		 * Recalculate the ISM mass and compare based on a maximum percent
		 * difference to account for round-off error.
		 */
		double ssp_mass = (*(*sz).ism).star_formation_history[0] * (*sz).dt;
		double ism_mass = (INITIAL_ISM_MASS +
			(*sz).current_time * (*(*sz).ism).infall_rate - ssp_mass +
			ssp_mass * (*(*sz).ssp).crf[(*sz).timestep] -
			(*(*sz).ism).eta[0] * ssp_mass
		);
		double percent_difference = absval(
			((*(*sz).ism).mass - ism_mass) / (*(*sz).ism).mass
		);
		status &= percent_difference < 1e-12;
	} else {}
	return status;

}


/*
 * Performs the zero age ssp edge-case test on the update_gas_evolution
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short zero_age_ssp_test_update_gas_evolution(SINGLEZONE *sz) {

	unsigned short status = (*(*sz).ism).star_formation_rate > 0;
	if (status) {
		/*
		 * Recalculate the ISM mass and compare based on a maximum percent
		 * difference to account for round-off error. With star formation at
		 * the timestep immediately following the end of the simulation, there
		 * is only the infall.
		 */
		double ism_mass = (INITIAL_ISM_MASS +
			(*sz).current_time * (*(*sz).ism).infall_rate
		);
		double percent_difference = absval(
			((*(*sz).ism).mass - ism_mass) / (*(*sz).ism).mass
		);
		status &= percent_difference < 1e-12;
	} else {}
	return status;

}


/*
 * Performs the quiescence test on the get_outflow_rate function in the parent
 * directory by ensuring the outflow rate is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short quiescence_test_get_outflow_rate(SINGLEZONE *sz) {

	return get_outflow_rate(*sz) == 0;

}


/*
 * Performs the max age ssp test on the get_outflow_rate function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short max_age_ssp_test_get_outflow_rate(SINGLEZONE *sz) {

	/* There shouldn't be any outflows under this edge case */
	return quiescence_test_get_outflow_rate(sz);

}


/*
 * Performs the zero age ssp test on the get_outflow_rate function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short zero_age_ssp_test_get_outflow_rate(SINGLEZONE *sz) {

	return get_outflow_rate(*sz) == (
		(*(*sz).ism).eta[(*sz).timestep] * (*(*sz).ism).star_formation_rate
	);

}


/*
 * Performs the quiescence test on the singlezone_unretained function in the
 * parent directory by ensuring the unretained production is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short quiescence_test_singlezone_unretained(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	double *unretained = singlezone_unretained(*sz);
	if (unretained != NULL) {
		for (i = 0u; i < (*sz).n_elements; i++) {
			status &= unretained[i] == 0;
			if (!status) break;
		}
		free(unretained);
		return status;
	} else {
		return 0u;
	}

}


/*
 * Performs the max age ssp edge-case test on the get_outflow_rate function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short max_age_ssp_test_singlezone_unretained(SINGLEZONE *sz) {

	/* There shouldn't be any unretained material under this test */
	return quiescence_test_singlezone_unretained(sz);

}


/*
 * Performs the zero age SSP edge-case test on the get_outflow rate function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz:		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short zero_age_ssp_test_singlezone_unretained(SINGLEZONE *sz) {

	/* There shouldn't be any unretained material under this test */
	return quiescence_test_singlezone_unretained(sz);

}

