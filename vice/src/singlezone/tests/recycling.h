
#ifndef SINGLEZONE_TESTS_RECYCLING_H
#define SINGLEZONE_TESTS_RECYCLING_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence edge-case test on the mass_recycled routine in the
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
 * source: recycling.c
 */
extern unsigned short quiescence_test_mass_recycled(SINGLEZONE *sz);

/*
 * Performs the maxage SSP edge-case test on the mass_recycled function in the
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
 * source: recycling.c
 */
extern unsigned short max_age_ssp_test_mass_recycled(SINGLEZONE *sz);

/*
 * Performs the zero age SSP edge-case test on the mass_recycled function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: recycling.c
 */
extern unsigned short zero_age_ssp_test_mass_recycled(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_RECYCLING_H */
