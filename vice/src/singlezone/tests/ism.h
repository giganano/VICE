
#ifndef SINGLEZONE_TESTS_ISM_H
#define SINGLEZONE_TESTS_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Performs the quiescence test on the update_gas_evolution function in the
 * parent directory by ensuring the star formation rate is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short quiescence_test_update_gas_evolution(SINGLEZONE *sz);

/*
 * Performs the max age ssp edge-case test on the update_gas_evolution
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short max_age_ssp_test_update_gas_evolution(SINGLEZONE *sz);

/*
 * Performs the zero age ssp edge-case test on the update_gas_evolution
 * function in the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short zero_age_ssp_test_update_gas_evolution(SINGLEZONE *sz);

/*
 * Performs the quiescence test on the get_outflow_rate function in the parent
 * directory by ensuring the outflow rate is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short quiescence_test_get_outflow_rate(SINGLEZONE *sz);

/*
 * Performs the max age ssp test on the get_outflow_rate function in the
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
 * source: ism.c
 */
extern unsigned short max_age_ssp_test_get_outflow_rate(SINGLEZONE *sz);

/*
 * Performs the zero age ssp test on the get_outflow_rate function in the
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
 * source: ism.c
 */
extern unsigned short zero_age_ssp_test_get_outflow_rate(SINGLEZONE *sz);

/*
 * Performs the quiescence test on the singlezone_unretained function in the
 * parent directory by ensuring the unretained production is equal to zero.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to run the quiescence test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short quiescence_test_singlezone_unretained(SINGLEZONE *sz);

/*
 * Performs the max age ssp edge-case test on the get_outflow_rate function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short max_age_ssp_test_singlezone_unretained(SINGLEZONE *sz);

/*
 * Performs the zero age SSP edge-case test on the get_outflow rate function in
 * the parent directory.
 *
 * Parameters
 * ==========
 * sz:		A pointer to the singlezone object to perform the test on
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short zero_age_ssp_test_singlezone_unretained(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_TESTS_ISM_H */
