
#ifndef TESTS_OBJECTS_INTEGRAL_H
#define TESTS_OBJECTS_INTEGRAL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs an integral object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_integral_initialize(void);

/*
 * Test the function which frees the memory stored by an integral object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: integral.c
 */
extern unsigned short test_integral_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_INTEGRAL_H */
