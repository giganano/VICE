
#ifndef MULTIZONE_TESTS_ISM_H
#define MULTIZONE_TESTS_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

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
 * source: ism.c
 */
extern unsigned short separation_test_update_zone_evolution(MULTIZONE *mz);

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
 * source: ism.c
 */
extern unsigned short no_migration_test_multizone_unretained(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_ISM_H */
