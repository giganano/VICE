
#ifndef MULTIZONE_TESTS_AGB_H
#define MULTIZONE_TESTS_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

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
 * source: agb.c
 */
extern unsigned short no_migration_test_m_AGB_from_tracers(MULTIZONE *mz);

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
 * source: agb.c
 */
extern unsigned short separation_test_m_AGB_from_tracers(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_AGB_H */
