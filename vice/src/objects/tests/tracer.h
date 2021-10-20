
#ifndef TESTS_OBJECTS_TRACER_H
#define TESTS_OBJECTS_TRACER_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a tracer object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: tracer.c
 */
extern unsigned short test_tracer_initialize(void);

/*
 * Test the function which frees the memory stored in a tracer object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: tracer.c
 */
extern unsigned short test_tracer_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_TRACER_H */
