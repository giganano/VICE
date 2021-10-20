
#ifndef TESTS_UTILS_H
#define TESTS_UTILS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Test the choose operation (a b) implemented at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_choose(void);

/*
 * Test the absolute value function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_absval(void);

/*
 * Tests the sign function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_sign(void);

/*
 * Test the simple hash function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_simple_hash(void);

/*
 * Test the psuedorandom number generator at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_rand_range(void);

/*
 * Test the 1-D interpolation function vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_interpolate(void);

/*
 * Test the 2D interpolation function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_interpolate2D(void);

/*
 * Test the sqrt(x) interpolation function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_interpolate_sqrt(void);

/*
 * Tests the bin number lookup function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_get_bin_number(void);

/*
 * Test the binspace function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_binspace(void);

/*
 * Test the bin_centers function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_bin_centers(void);

/*
 * Test the sum function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_sum(void);

/*
 * Test the function which sets char pointer values from ordinal numbers
 * sent from Python at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_set_char_p_value(void);

/*
 * Test the max function at vice/src/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_max(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_UTILS_H */
