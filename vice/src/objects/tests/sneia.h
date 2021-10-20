
#ifndef TESTS_OBJECTS_SNEIA_H
#define TESTS_OBJECTS_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a sneia_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: sneia.c
 */
extern unsigned short test_sneia_yield_initialize(void);

/*
 * Test the function which frees the memory stored in a sneia_yield_specs object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: sneia.c
 */
extern unsigned short test_sneia_yield_free(void);

/*
 * Obtain a pointer to a test instance of the SNEIA_YIELD_SPECS object
 *
 * source: sneia.c
 */
extern SNEIA_YIELD_SPECS *sneia_yield_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_SNEIA_H */
