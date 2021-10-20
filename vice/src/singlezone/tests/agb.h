
#ifndef SINGLEZONE_TESTS_AGB_H
#define SINGLEZONE_TESTS_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence edge-case test on the m_AGB function at ../agb.h
 * applicable to cases where the mass production should be zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short quiescence_test_m_AGB(SINGLEZONE *sz);

/*
 * Performs the max age SSP edge-case test on the m_AGB function at ../agb.h
 * applicable to cases where star formation is nonzero for the first timestep
 * and zero thereafter.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short max_age_ssp_test_m_AGB(SINGLEZONE *sz);

/*
 * Performs the zero age SSP edge-case test on the m_AGB function in the
 * parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short zero_age_ssp_test_m_AGB(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_AGB_H */
