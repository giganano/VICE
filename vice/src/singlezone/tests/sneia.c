/*
 * This file implements edge-case testing of the SNe Ia routines in the
 * parent directory.
 */

#include "../sneia.h"

/*
 * Performs the quiescence edge-case test on the mdot_sneia function in the
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
 * header: sneia.h
 */
extern unsigned short quiescence_test_mdot_sneia(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mdot_sneia(*sz, *(*sz).elements[i]) == 0;
		if (!status) break;
	}
	return status;

}


/*
 * Performs the max age ssp edge-case test on the mdot_sneia function in the
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
 * header: sneia.h
 */
extern unsigned short max_age_ssp_test_mdot_sneia(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= mdot_sneia(*sz, *(*sz).elements[i]) == (
			get_ia_yield(*(*sz).elements[i], 0) *
			(*(*sz).ism).star_formation_history[0] *
			(*(*(*sz).elements[i]).sneia_yields).RIa[(*sz).timestep]
		);
		if (!status) break;
	}
	return status;

}


/*
 * Performs the zero age ssp edge-case test on the mdot_sneia function in the
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
 * header: sneia.h
 */
extern unsigned short zero_age_ssp_test_mdot_sneia(SINGLEZONE *sz) {

	/*
	 * SNe Ia having an intrinsic delay, a zero age population shouldn't
	 * produce any SN Ia enrichment. This should thus be identical to the
	 * quiescent scenario.
	 */
	return quiescence_test_mdot_sneia(sz);

}

