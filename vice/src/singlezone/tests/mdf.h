
#ifndef SINGLEZONE_TESTS_MDF_H
#define SINGLEZONE_TESTS_MDF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: mdf.c
 */
extern unsigned short quiescence_test_MDF(SINGLEZONE *sz);

/*
 * Performs the max age SSP edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: mdf.c
 */
extern unsigned short max_age_ssp_test_MDF(SINGLEZONE *sz);

/*
 * Performs the zero age SSP edge-case test on the MDF routines in the parent
 * directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: mdf.c
 */
extern unsigned short zero_age_ssp_test_MDF(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_MDF_H */
