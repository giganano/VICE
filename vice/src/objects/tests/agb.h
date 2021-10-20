
#ifndef TESTS_OBJECTS_AGB_H
#define TESTS_OBJECTS_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs an agb_yield_grid object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short test_agb_yield_grid_initialize(void);

/*
 * Test the function which frees the memory stored by an agb_yield_grid object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: agb.c
 */
extern unsigned short test_agb_yield_grid_free(void);

/*
 * Obtain a pointer to test instance of the AGB_YIELD_GRID object
 *
 *
 * source: agb.c
 */
extern AGB_YIELD_GRID *agb_yield_grid_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_AGB_H */
