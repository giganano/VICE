
#ifndef TESTS_OBJECTS_SINGLEZONE_H
#define TESTS_OBJECTS_SINGLEZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"
#include "../../singlezone.h"

#ifndef TEST_SINGLEZONE_N_STEPS
#define TEST_SINGLEZONE_N_STEPS 1
#endif /* TEST_SINGLEZONE_N_STEPS */

#ifndef TEST_SINGLEZONE_TIMESTEP_SIZE
#define TEST_SINGLEZONE_TIMESTEP_SIZE 0.01
#endif /* TEST_SINGLEZONE_TIMESTEP */

/*
 * Test the function which constructs a singlezone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: singlezone.c
 */
extern unsigned short test_singlezone_initialize(void);

/*
 * Test the function which frees the memory stored by a singlezone object.
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: singlezone.c
 */
extern unsigned short test_singlezone_free(void);

/*
 * Obtain a pointer to a test instance of the SINGLEZONE object.
 *
 * source: singlezone.c
 */
extern SINGLEZONE *singlezone_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_SINGLEZONE_H */
