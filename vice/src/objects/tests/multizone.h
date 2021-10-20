
#ifndef TESTS_OBJECTS_MULTIZONE_H
#define TESTS_OBJECTS_MULTIZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

#ifndef TESTS_N_ZONES
#define TESTS_N_ZONES 10u
#endif /* TESTS_N_ZONES */

/*
 * Test the function which constructs a multizone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: multizone.c
 */
extern unsigned short test_multizone_initialize(void);

/*
 * Test the function which frees the memory stored by a multizone object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: multizone.c
 */
extern unsigned short test_multizone_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_MULTIZONE_H */

