
#ifndef OBJECTS_TESTS_HYDRODISKSTARS_H
#define OBJECTS_TESTS_HYDRODISKSTARS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../hydrodiskstars.h"

/*
 * Tests the constructor function for the hydrodiskstars object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: hydrodiskstars.c
 */
extern unsigned short test_hydrodiskstars_initialize(void);

/*
 * Tests the destructor function for the hydrodiskstars object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: hydrodiskstars.c
 */
extern unsigned short test_hydrodiskstars_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_TESTS_HYDRODISKSTARS_H */
