
#ifndef TESTS_OBJECTS_ISM_H
#define TESTS_OBJECTS_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs an ism object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short test_ism_initialize(void);

/*
 * Test the function which frees the memory stored in an ism object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ism.c
 */
extern unsigned short test_ism_free(void);

/*
 * Obtain a pointer to a test instance of the ISM object
 *
 * source: ism.c
 */
extern ISM *ism_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_ISM_H */
