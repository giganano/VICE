
#ifndef MULTIZONE_TESTS_RECYCLING_H
#define MULTIZONE_TESTS_RECYCLING_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the no migration edge-case test on the recycle_metals_from_tracers
 * function the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: recycling.c
 */
extern unsigned short no_migration_test_recycle_metals_from_tracers(
	MULTIZONE *mz);

/*
 * Performs the separation edge case test on the recycle_metals_from_tracers
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
 * source: recycling.c
 */
extern unsigned short separation_test_recycle_metals_from_tracers(
	MULTIZONE *mz);

/*
 * Performs the no migration edge case test on the gas_recycled_in_zone
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: recycling.c
 */
extern unsigned short no_migration_test_gas_recycled_in_zones(MULTIZONE *mz);

/*
 * Performs the separation test on the gas_recycled_in_zones function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: recycling.c
 */
extern unsigned short separation_test_gas_recycled_in_zones(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_RECYCLING_H */
