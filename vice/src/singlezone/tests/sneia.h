
#ifndef SINGLEZONE_TESTS_SNEIA_H
#define SINGLEZONE_TESTS_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence edge-case test on the mdot_sneia function in the
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
 * source: sneia.c
 */
extern unsigned short quiescence_test_mdot_sneia(SINGLEZONE *sz);

/*
 * Performs the max age ssp edge-case test on the mdot_sneia function in the
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
 * source: sneia.c
 */
extern unsigned short max_age_ssp_test_mdot_sneia(SINGLEZONE *sz);

/*
 * Performs the zero age ssp edge-case test on the mdot_sneia function in the
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
 * source: sneia.c
 */
extern unsigned short zero_age_ssp_test_mdot_sneia(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_SNEIA_H */
