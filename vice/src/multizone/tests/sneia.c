/*
 * This file implements testing of the SN Ia functions in the parent directory.
 */

#include <stdlib.h>
#include "../sneia.h"
#include "../../utils.h"
#include "../../singlezone/sneia.h"


/*
 * Performs the no migration edge case test on the mdot_sneia function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on scucess, 0 on failure
 *
 * header: sneia.h
 */
extern unsigned short no_migration_test_m_sneia_from_tracers(MULTIZONE *mz) {

	/*
	 * Compare that calculated for each element in each zone to that expected
	 * for the singlezone object.
	 *
	 * This test usually passes with %-differences on the order of 1e-16.
	 */
	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		double *actual = m_sneia_from_tracers(*mz, i);
		if (actual != NULL) {
			unsigned int j;
			for (j = 0u; j < (*(*mz).mig).n_zones; j++) {
				double expected = mdot_sneia(
					*(*mz).zones[j],
					*(*(*mz).zones[j]).elements[i]
				) * (*(*mz).zones[j]).dt;
				double percent_difference = absval(
					(actual[j] - expected) / expected
				);
				status &= (percent_difference < 1e-3 ||
					(actual[j] == 0 && expected == 0));
				if (!status) break;
			}
			free(actual);
		} else {
			return 0u;
		}
		if (!status) break;
	}
	return status;

}


/*
 * Performs the separation test on the m_sneia_from_tracers function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: sneia.h
 */
extern unsigned short separation_test_m_sneia_from_tracers(MULTIZONE *mz) {

	/*
	 * There shouldn't be any in the star-forming zone due to the intrinsic
	 * time-delay -> all SN Ia enrichment should happen in the quiescent zone.
	 */
	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		double *sneia = m_sneia_from_tracers(*mz, i);
		if (sneia != NULL) {
			status &= sneia[0] == 0;
			if ((*(*(*(*(*
				mz).zones[0]).elements[i]).sneia_yields).yield_
				).assumed_constant) status &= sneia[1] > 0;
			free(sneia);
			if (!status) break;
		} else {
			return 0u;
		}
	}
	return status;

}

