
#ifndef MULTIZONE_TESTS_MDF_H
#define MULTIZONE_TESTS_MDF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the separation test on the tracers_MDF function in the parent
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
 * source: mdf.c
 */
extern unsigned short separation_test_tracers_MDF(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TESTS_MDF_H */
