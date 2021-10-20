/*
 * This file implements testing of the ISM routines in the parent directory.
 */

#include <stdlib.h>
#include "../ism.h"


/*
 * Performs the separation test on the update_zone_evolution function in the
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
 * header: ism.h
 */
extern unsigned short separation_test_update_zone_evolution(MULTIZONE *mz) {

	return (
		(*(*(*mz).zones[1]).ism).star_formation_rate == 0 &&
		(*(*(*mz).zones[0]).ism).star_formation_rate > 0
	);

}


/*
 * Performs the no migration edge-case test on the multizone_unretained
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ism.h
 */
extern unsigned short no_migration_test_multizone_unretained(MULTIZONE *mz) {

	/*
	 * There shouldn't be any unretained material under this model.
	 */
	unsigned int i, j;
	unsigned short status = 1u;
	double **unretained = multizone_unretained(*mz);
	if (unretained != NULL) {
		for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
			for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
				status &= unretained[i][j] == 0;
				if (!status) break;
			}
			if (!status) break;
		}
		free(unretained);
		return status;
	} else {
		return 0u;
	}

}

