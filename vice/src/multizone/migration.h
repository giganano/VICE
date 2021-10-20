
#ifndef MULTIZONE_MIGRATION_H
#define MULTIZONE_MIGRATION_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"


/*
 * Migrates all gas, elements, and tracer particles between zones at the
 * current timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * source: migration.c
 */
extern void migrate(MULTIZONE *mz);

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
 * source: migration.c
 */
extern unsigned short migration_matrix_sanitycheck(double ***migration_matrix,
	unsigned long n_times, unsigned int n_zones);

/*
 * Allocates memory for the gas migration matrix.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * source: migration.c
 */
extern void malloc_gas_migration(MULTIZONE *mz);

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
 * source: migration.c
 */
extern unsigned short setup_migration_element(MULTIZONE mz,
	double ***migration_matrix, unsigned int row, unsigned int column,
	double *arr);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_MDF_H */

