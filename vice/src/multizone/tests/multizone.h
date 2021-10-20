
#ifndef MULTIZONE_TESTS_MULTIZONE_H
#define MULTIZONE_TESTS_MULTIZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the no migration edge-case test on the multizone_stellar_mass
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
 * source: multizone.c
 */
extern unsigned short no_migration_test_multizone_stellar_mass(MULTIZONE *mz);

/*
 * Performs the separation test on the multizone stellar mass function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to run the tests on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: multizone.c
 */
extern unsigned short separation_test_multizone_stellar_mass(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_MULTIZONE_H */
