
#ifndef TESTS_OBJECTS_CCSNE_H
#define TESTS_OBJECTS_CCSNE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a ccsne_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ccsne.c
 */
extern unsigned short test_ccsne_yield_initialize(void);

/*
 * Test the function which frees the memory stored by a ccsne_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: ccsne.c
 */
extern unsigned short test_ccsne_yield_free(void);

/*
 * Obtain a pointer to a test instance of the CCSNE_YIELD_SPECS object
 *
 * source: ccsne.c
 */
extern CCSNE_YIELD_SPECS *ccsne_yield_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_CCSNE_H */
