/*
 * This file implements testing of the enrichment from asymptotic giant
 * branch stars in the parent directory.
 */

#include "../../utils.h"
#include "../../ssp.h"
#include "../agb.h"


/*
 * Performs the quiescence edge-case test on the m_AGB function at ../agb.h
 * applicable to cases where the mass production should be zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: agb.h
 */
extern unsigned short quiescence_test_m_AGB(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= m_AGB(*sz, *(*sz).elements[i]) == 0;
		if (!status) break;
	}
	return status;

}


/*
 * Performs the max age SSP edge-case test on the m_AGB function at ../agb.h
 * applicable to cases where star formation is nonzero for the first timestep
 * and zero thereafter.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: agb.h
 */
extern unsigned short max_age_ssp_test_m_AGB(SINGLEZONE *sz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*sz).n_elements; i++) {
		status &= m_AGB(*sz, *(*sz).elements[i]) == (
			get_AGB_yield(*(*sz).elements[i], 0,
				dying_star_mass((*sz).timestep * (*sz).dt,
					(*(*sz).ssp).postMS, 0)) *
			(*(*sz).ism).star_formation_history[0] * (*sz).dt *
			(
				(*(*sz).ssp).msmf[(*sz).timestep] -
				(*(*sz).ssp).msmf[(*sz).timestep + 1l]
			)
		);
		if (!status) break;
	}
	return status;

}


/*
 * Performs the zero age SSP edge-case test on the m_AGB function in the
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
 * header: agb.h
 */
extern unsigned short zero_age_ssp_test_m_AGB(SINGLEZONE *sz) {

	/*
	 * For a zero-age SSP, there shouldn't be any <8 Msun stars dying yet.
	 * This test should then be the same as the quiescent scenario.
	 */
	return quiescence_test_m_AGB(sz);

}

