/*
 * This file implements edge-case testing of routines of the singlezone object
 * in the parent directory.
 */

#include "../singlezone.h"
#include "../../utils.h"

/*
 * Performs the quiescence edge-case test on the singlezone_stellar_mass
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
 * header: singlezone.h
 */
extern unsigned short quiescence_test_singlezone_stellar_mass(SINGLEZONE *sz) {

	return singlezone_stellar_mass(*sz) == 0;

}


/*
 * Performs the max age ssp edge-case test on the singlezone_stellar_mass
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
 * header: singlezone.h
 */
extern unsigned short max_age_ssp_test_singlezone_stellar_mass(SINGLEZONE *sz) {

	return singlezone_stellar_mass(*sz) == (
		(*(*sz).ism).star_formation_history[0] * (*sz).dt * (
			1 - (*(*sz).ssp).crf[(*sz).timestep]
		)
	);

}


/*
 * Performs the zero age spp edge-case test on the singlezone_stellar_mass
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
 * header: singlezone.h
 */
extern unsigned short zero_age_ssp_test_singlezone_stellar_mass(SINGLEZONE *sz) {

	/* In detail, the single episode of star formation is one timestep ago. */
	double mass = (*(*sz).ism).star_formation_history[(*sz).timestep - 1ul];
	mass *= (*sz).dt;
	mass *= (1 - (*(*sz).ssp).crf[1]);
	double percent_difference = absval(
		singlezone_stellar_mass(*sz) - mass) / mass;
	return percent_difference < 1e-12;

}

