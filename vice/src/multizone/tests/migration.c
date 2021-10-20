/*
 * This file implements testing of the migration routines in the parent
 * directory.
 */

#include <stdlib.h>
#include "../migration.h"


/*
 * Performs the no migration edge-case test on the migration routines in the
 * parent directory by assuring that the ISM and element masses are the same
 * before and after the call to the migrate function.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: migration.h
 */
extern unsigned short no_migration_test_migrate(MULTIZONE *mz) {

	/*
	 * Allocate memory for ISM and element masses within each zone, then
	 * simply pull a copy before calling the migrate function
	 */
	double *ism_masses, **element_masses;
	ism_masses = (double *) malloc ((*(*mz).mig).n_zones * sizeof(double));
	element_masses = (double **) malloc ((*(*mz).mig).n_zones *
		sizeof(double *));

	unsigned int i, j;
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		ism_masses[i] = (*(*(*mz).zones[i]).ism).mass;
		element_masses[i] = (double *) malloc ((*(*mz).zones[i]).n_elements *
			sizeof(double));
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			element_masses[i][j] = (*(*(*mz).zones[i]).elements[j]).mass;
		}
	}

	migrate(mz);
	unsigned short status = 1u;

	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		status &= ism_masses[i] == (*(*(*mz).zones[i]).ism).mass;
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			status &= (
				element_masses[i][j] == (*(*(*mz).zones[i]).elements[j]).mass
			);
			if (!status) break;
		}
		if (!status) break;
	}

	free(ism_masses);
	free(element_masses);
	return status;

}


/*
 * Performs the separation test on the migration routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: migration.h
 */
extern unsigned short separation_test_migrate(MULTIZONE *mz) {

	/*
	 * There will be two rather than one timestep's worth of tracer particles
	 * in the star forming zone. This has to do with when tracer particles are
	 * injected and migrated -> the stars that just formed and the stars that
	 * are forming will, at the end of a timestep, still be in the star forming
	 * zone.
	 */
	unsigned long i, n = 0ul;
	for (i = 0ul; i < (*(*mz).mig).tracer_count; i++) {
		if ((*(*(*mz).mig).tracers[i]).zone_current == 0u) n++;
	}
	return n == 2 * (*(*mz).mig).n_tracers;

}

