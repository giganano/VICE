/*
 * This file implements testing of the single-element time-evolution routines
 * at element.h in the parent directory.
 */

#include "../element.h"
#include <math.h>

/*
 * Implements the quiescence test on the update_element_mass function in the
 * parent directory by ensuring that each element's mass is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short quiescence_test_update_element_mass(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= (*(*sz).elements[i]).mass == 0;
		if (!status) break;
	}
	return status;

}


/*
 * Performs the max age SSP edge-case test on the update_element_mass function
 * in the parent directory by ensuring that each element's mass is nonzero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short max_age_ssp_test_update_element_mass(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= (*(*sz).elements[i]).mass > 0;
		if (!status) break;
	}
	return status;

}


/*
 * Performs the zero age SSP edge-case test on the update_element_mass function
 * in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short zero_age_ssp_test_update_element_mass(SINGLEZONE *sz) {

	/* The same criteria as the max age test */
	return max_age_ssp_test_update_element_mass(sz);

}


/*
 * Implements the quiescence test on the onH function in the parent directory
 * by ensuring that [X/H] = -infinity for each element.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short quiescence_test_onH(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		#ifdef INFINITY
			status &= onH(*sz, *(*sz).elements[i]) == -INFINITY;
		#else
			#ifdef NAN
				status &= isnan(onH(*sz, *(*sz).elements[i]));
			#else
				status &= onH(*sz, *(*sz).elements[i]) == -100;
			#endif
		#endif
		if (!status) break;
	}
	return status;

}


/*
 * Performs the max age SSP edge-case test on the onH function in the parent
 * directory by ensuring that [X/H] is finite and less than zero for each
 * element.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short max_age_ssp_test_onH(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		/* manylinux distributions throw warning about isfinite declaration */
		#ifdef isfinite
			status &= isfinite(onH(*sz, *(*sz).elements[i]));
		#endif
		status &= onH(*sz, *(*sz).elements[i]) < 0;
		if (!status) break;
	}
	return status;

}


/*
 * Performs the zero age SSP test on the onH function in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short zero_age_ssp_test_onH(SINGLEZONE *sz) {

	/* The same criteria as the max age test */
	return max_age_ssp_test_onH(sz);

}

