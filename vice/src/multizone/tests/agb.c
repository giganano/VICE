/*
 * Implements testing of the m_AGB_from_tracers function in the parent
 * directory.
 */

#include <stdlib.h>
#include <math.h>
#include "../../singlezone/agb.h"
#include "../../utils.h"
#include "../agb.h"


/*
 * Performs the no migration edge-case test on the m_AGB_from_tracers function
 * in the parent directory by ensuring that the returned values are the same
 * as calculated by the corresponding singlezone routine.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: agb.h
 */
extern unsigned short no_migration_test_m_AGB_from_tracers(MULTIZONE *mz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		double *mass = m_AGB_from_tracers(*mz, i);
		if (mass != NULL) {
			unsigned int j;
			for (j = 0u; j < (*(*mz).mig).n_zones; j++) {
				/*
				 * Base the test on a reasonable percent difference between
				 * the two functions - a value of 1e-3 reflects roundoff error
				 * from two different algorithms in calculating the same
				 * quantity.
				 */
				double from_singlezone = m_AGB(*(*mz).zones[j],
					*(*(*mz).zones[j]).elements[i]);
				double percent_difference = absval(
					(from_singlezone - mass[j]) / mass[j]
				);
				status &= percent_difference < 1e-3;
				if (!status) break;
			}
			free(mass);
		} else {
			return 0u;
		}
		if (!status) break;
	}
	return status;

}


/*
 * Performs the separation edge-case test on the m_AGB_from_tracers function
 * in the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: agb.h
 */
extern unsigned short separation_test_m_AGB_from_tracers(MULTIZONE *mz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		double *m_AGB = m_AGB_from_tracers(*mz, i);
		if (m_AGB != NULL) {
			/* at least an order of magnitude more from the destination zone */
			if (m_AGB[0] > 0 && m_AGB[1] > 0) {
				status &= log10(m_AGB[1]) - log10(m_AGB[0]) > 1;
				free(m_AGB);
				if (!status) break;
			} else {}
		} else {
			return 0u;
		}
	}
	return status;

}

