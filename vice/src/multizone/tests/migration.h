
#ifndef MULTIZONE_TESTS_MIGRATION_H
#define MULTIZONE_TESTS_MIGRATION_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

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
 * source: migration.c
 */
extern unsigned short no_migration_test_migrate(MULTIZONE *mz);

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
 * source: migration.c
 */
extern unsigned short separation_test_migrate(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_MIGRATION_H */
