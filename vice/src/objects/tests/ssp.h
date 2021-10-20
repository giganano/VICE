
#ifndef TESTS_OBJECTS_SSP_H
#define TESTS_OBJECTS_SSP_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs an ssp object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ssp.c
 */
extern unsigned short test_ssp_initialize(void);

/*
 * Test the function which frees the memory stored in an ssp object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ssp.c
 */
extern unsigned short test_ssp_free(void);

/*
 * Obtain a pointer to a test instance of the SSP object.
 *
 * source: ssp.c
 */
extern SSP *ssp_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_SSP_H */
