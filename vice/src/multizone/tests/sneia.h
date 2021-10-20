
#ifndef MULTIZONE_TESTS_SNEIA_H
#define MULTIZONE_TESTS_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the no migration edge case test on the mdot_sneia function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to perform the test on
 *
 * Returns
 * =======
 * 1 on scucess, 0 on failure
 *
 * source: sneia.c
 */
extern unsigned short no_migration_test_m_sneia_from_tracers(MULTIZONE *mz);

/*
 * Performs the separation test on the m_sneia_from_tracers function in the
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
 * source: sneia.c
 */
extern unsigned short separation_test_m_sneia_from_tracers(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_SNEIA_H */
