
#ifndef TESTS_OBJECTS_IMF_H
#define TESTS_OBJECTS_IMF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#ifndef TEST_IMF_M_LOWER
#define TEST_IMF_M_LOWER 0.08
#endif /* TEST_IMF_M_LOWER */

#ifndef TEST_IMF_M_UPPER
#define TEST_IMF_M_UPPER 100
#endif /* TEST_IMF_M_UPPER */

#include "../../objects.h"

/*
 * Test the function which constructs an IMF object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: imf.c
 */
extern unsigned short test_imf_initialize(void);

/*
 * Test the function which frees the memory stored by an IMF object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: imf.c
 */
extern unsigned short test_imf_free(void);

/*
 * Obtain a pointer to a test instance of the IMF_ object
 *
 * source: imf.c
 */
extern IMF_ *imf_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_IMF_H */
