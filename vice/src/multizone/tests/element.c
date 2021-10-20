/*
 * This file implements testing of the element routines in the parent
 * directory.
 */

#include <math.h>
#include "../element.h"


/*
 * Performs the separation test on the update_elements function the parent
 * directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: element.h
 */
extern unsigned short separation_test_update_elements(MULTIZONE *mz) {

	unsigned short i, status = 1u;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {
		/*
		 * There aren't any winds in the quiescent zone, so even if the
		 * element being tested is an alpha element, there should be more of
		 * it there than in the star-forming zone, but not necessarily by any
		 * significant amount.
		 */
		status &= (
			(*(*(*mz).zones[1]).elements[i]).mass >
			(*(*(*mz).zones[0]).elements[i]).mass
		);
		if (!status) break;
	}
	return status;

}

