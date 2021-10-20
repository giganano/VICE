/*
 * This file implements migration of gas and stars in VICE's multizone
 * simulations.
 */

#include <stdlib.h>
#include "../migration.h"
#include "../singlezone/singlezone.h"
#include "../utils.h"
#include "migration.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static unsigned short normalize_migration_element(MULTIZONE mz,
	double ***migration_matrix, unsigned int row, unsigned int column);
static void migrate_tracer(MULTIZONE mz, TRACER *t);
static void migrate_gas_element(MULTIZONE *mz, int index);
static void migration_sanity_check(MULTIZONE *mz);
static double **setup_changes(unsigned int n_zones);
static double **get_changes(MULTIZONE mz, int index);


/*
 * Performs a sanity check on a given migration matrix by making sure the sum
 * of migration probabilities out of a given zone at all times is <= 1.
 *
 * Parameters
 * ==========
 * migration_matrix: 		The migration matrix to sanity check
 * n_times: 				The number of times the simulation will evaluate
 * n_zones: 				The number of zones in the simulation
 *
 * Returns
 * =======
 * 0 on passing sanity check, 1 on failure
 *
 * header: migration.h
 */
extern unsigned short migration_matrix_sanitycheck(double ***migration_matrix,
	unsigned long n_times, unsigned int n_zones) {

	unsigned long i;
	for (i = 0l; i < n_times; i++) {
		unsigned int j;
		/*
		 * First set the diagonal equal to zero; migration within zones is
		 * simply ignored.
		 */
		for (j = 0; j < n_zones; j++) {
			migration_matrix[i][j][j] = 0.0;
		}
		for (j = 0; j < n_zones; j++) {
			/*
			 * At all times for all zones, total probability of migration out
			 * of the zone must be <= 1.
			 */
			if (sum(migration_matrix[i][j], n_zones) > 1) return 1;
		}
	}
	return 0;

}


/*
 * Allocates memory for the gas migration matrix.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * header: migration.h
 */
extern void malloc_gas_migration(MULTIZONE *mz) {

	/* Allocate memory for each timestep */
	unsigned long i, length = n_timesteps((*(*mz).zones[0]));
	mz -> mig -> gas_migration = (double ***) malloc (length *
		sizeof(double **));

	/*
	 * At each timestep, allocate memory for an n_zones x n_zones array of
	 * doubles.
	 */
	for (i = 0l; i < length; i++) {
		mz -> mig -> gas_migration[i] = (double **) malloc (
			(*(*mz).mig).n_zones * sizeof(double *));
		unsigned int j;
		for (j = 0; j < (*(*mz).mig).n_zones; j++) {
			mz -> mig -> gas_migration[i][j] = (double *) malloc (
				(*(*mz).mig).n_zones * sizeof(double));

			/* Initially set everything to zero */
			unsigned int k;
			for (k = 0; k < (*(*mz).mig).n_zones; k++) {
				mz -> mig -> gas_migration[i][j][k] = 0.0;
			}
		}
	}

}


/*
 * Sets up an element of the migration matrix at each timestep that it has
 * memory allocated for.
 *
 * Parameters
 * ==========
 * mz: 					The multizone object for the current simulation
 * migration_matrix: 	Pointer to the migration matrix itself
 * row: 				The row number of this element
 * column: 				The column number of this element
 * arr: 				The value of the migration matrix at each timestep
 *
 * Returns
 * =======
 * 1 if the normalization results in a probabiliy above 1 or below 0. 0 if
 * successful.
 *
 * header: migration.h
 */
extern unsigned short setup_migration_element(MULTIZONE mz,
	double ***migration_matrix, unsigned int row, unsigned int column,
	double *arr) {

	/*
	 * At each timestep, simply copy the value over. Memory will have already
	 * been allocated.
	 */
	unsigned long i, length = n_timesteps(*mz.zones[0]);

	if (row == column) {
		for (i = 0l; i < length; i++) {
			migration_matrix[i][row][column] = 0.0;
		}
		return 0;
	} else {
		for (i = 0; i < length; i++) {
			migration_matrix[i][row][column] = arr[i];
		}
		return normalize_migration_element(mz, migration_matrix, row, column);
	}

}


/*
 * Normalize an element of the migration matrix such based on the timestep
 * size. Multiplies the ij'th element by the timestep size over the
 * normalization time interval.
 *
 * Parameters
 * ==========
 * mz: 					A copy of the multizone object
 * migration_matrix: 	A pointer to the migration matrix
 * row: 				The row number i
 * column: 				The column number j
 *
 * Returns
 * =======
 * 1 if the normalization results in a probabiliy above 1 or below 0. 0 if
 * successful.
 */
static unsigned short normalize_migration_element(MULTIZONE mz,
	double ***migration_matrix, unsigned int row, unsigned int column) {

	/*
	 * The row,column'th element of the migration matrix will get multiplied
	 * by the timestep interval over 10 Myr.
	 *
	 * Notes
	 * =====
	 * This modifies the interpretation of the migration matrix.
	 * M_ij(1 - \delta_ij) now denotes the likelihood that
	 */
	unsigned long i, length = n_timesteps((*mz.zones[0]));
	for (i = 0l; i < length; i++) {
		migration_matrix[i][row][column] *= (*mz.zones[0]).dt;
		migration_matrix[i][row][column] /= NORMALIZATION_TIME_INTERVAL;
		if (migration_matrix[i][row][column] < 0 ||
			migration_matrix[i][row][column] > 1) return 1;
	}
	return 0;

}


/*
 * Migrates all gas, elements, and tracer particles between zones at the
 * current timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * header: migration.h
 */
extern void migrate(MULTIZONE *mz) {

	/* Migrate gas and all elements between zones */
	int i;
	for (i = -1; i < (signed) (*(*mz).zones[0]).n_elements; i++) {
		migrate_gas_element(mz, i);
	}

	/* Migrate all tracer particles between zones */
	unsigned long j;
	for (j = 0l; j < (*(*mz).mig).tracer_count; j++) {
		migrate_tracer(*mz, mz -> mig -> tracers[j]);
	}
	migration_sanity_check(mz); 	/* sanity check the migration */

}


/*
 * Updates a tracer particle's current zone number based on the zone_history
 * array at the next timestep.
 *
 * Parameters
 * ==========
 * mz: 			The multizone object for the current simulation
 * t: 			A pointer to the tracer particle to potentially move between
 * 				zones
 */
static void migrate_tracer(MULTIZONE mz, TRACER *t) {

	unsigned long timestep = (*mz.zones[0]).timestep;
	t -> zone_current = (unsigned) (*t).zone_history[timestep + 1l];

}


/*
 * Migrates ISM gas and ISM phase elements between zones.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 * index: 	The index of the element to migrate between zones
 * 			-1 for the gas reservoir itself
 */
static void migrate_gas_element(MULTIZONE *mz, int index) {

	unsigned int i, j;
	double **changes = get_changes(*mz, index);
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		for (j = 0; j < (*(*mz).mig).n_zones; j++) {
			if (i == j) {
				/* migration within zone */
				continue;
			} else {
				switch (index) {
					case -1:
						/* gas leaves zone i and goes into zone j */
						mz -> zones[i] -> ism -> mass -= changes[i][j];
						mz -> zones[j] -> ism -> mass += changes[i][j];
						break;
					default:
						/* element leaves zone i and goes into zone j */
						mz -> zones[i] -> elements[index] -> mass -= (
							changes[i][j]
						);
						mz -> zones[j] -> elements[index] -> mass += (
							changes[i][j]
						);
						break;
				}
			}
		}
	}
	free(changes);

}


/*
 * Looks at the ISM mass and total element mass in each zone and takes into
 * account the physical lower bound.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to sanity check
 */
static void migration_sanity_check(MULTIZONE *mz) {

	unsigned int i, j;
	for (i = 0; i < (*(*mz).mig).n_zones; i++) {
		for (j = 0; j < (*(*mz).zones[i]).n_elements; j++) {
			if ((*(*(*mz).zones[i]).elements[j]).mass < 0) {
				mz -> zones[i] -> elements[j] -> mass = 0;
			} else {
				continue;
			}
		}
		if ((*(*(*mz).zones[i]).ism).mass < 1.e-12) {
			mz -> zones[i] -> ism -> mass = 1.e-12;
		} else {
			continue;
		}
	}

}


/*
 * Determine how much of the nebular phase mass migrates between all zones at
 * the current timestep.
 *
 * Parameters
 * ==========
 * mz: 				The multizone object for the current simulation
 * index: 			The index of the element to determine the changes for
 * 					-1 for the gas reservoir
 *
 * Returns
 * =======
 * An n_zones x n_zones 2D array of double where the [i][j]'th element is the
 * amount of mass that moves from the i'th to the j'th zone at the current
 * timestep.
 */
static double **get_changes(MULTIZONE mz, int index) {

	unsigned int i, j;
	unsigned long timestep = (*mz.zones[0]).timestep;
	double **changes = setup_changes((*mz.mig).n_zones);

	for (i = 0; i < (*mz.mig).n_zones; i++) {
		for (j = 0; j < (*mz.mig).n_zones; j++) {
			if (i == j) {
				/* migration within zone */
				changes[i][j] = 0.0;
			} else {
				switch (index) {
					case -1:
						/* gas reservoir */
						changes[i][j] = (
							(*mz.mig).gas_migration[timestep][i][j] *
							(*(*mz.zones[i]).ism).mass
						);
						break;
					default:
						/* element in the i'th zone */
						changes[i][j] = (
							(*mz.mig).gas_migration[timestep][i][j] *
							(*(*mz.zones[i]).elements[index]).mass
						);
						break;
				}
			}
		}
	}
	return changes;

}


/*
 * Sets up a n_zones x n_zones 2D-array of zeroes, within which the change in
 * masses for ISM phase elements and gas can be temporarily stored.
 *
 * Parameters
 * ==========
 * n_zones: 	The number of zones in the simulation
 *
 * Returns
 * =======
 * An n_zones x n_zones 2D double array where each element is set to zero.
 */
static double **setup_changes(unsigned int n_zones) {

	unsigned int i, j;
	double **changes = (double **) malloc (n_zones * sizeof(double *));
	for (i = 0; i < n_zones; i++) {
		changes[i] = (double *) malloc (n_zones * sizeof(double));
		for (j = 0; j < n_zones; j++) {
			changes[i][j] = 0.0;
		}
	}
	return changes;

}

