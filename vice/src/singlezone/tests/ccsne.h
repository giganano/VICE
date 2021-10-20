
#ifndef SINGLEZONE_TESTS_CCSNE_H
#define SINGLEZONE_TESTS_CCSNE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence edge-case test on the mdot_ccsne function at
 * ../ccsne.h applicable to cases where the mass production should be zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ccsne.c
 */
extern unsigned short quiescence_test_m_ccsne(SINGLEZONE *sz);

/*
 * Performs the max age SSP edge-case test on the mdot_ccsne function at
 * ../ccsne.h applicable to cases where only the zero'th timestep has star
 * formation.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the tests on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ccsne.c
 */
extern unsigned short max_age_ssp_test_m_ccsne(SINGLEZONE *sz);

/*
 * Performs the zero age SSP edge-case test on the mdot_ccsne function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ccsne.h
 */
extern unsigned short zero_age_ssp_test_m_ccsne(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_CCSNE_H */
