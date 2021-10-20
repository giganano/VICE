
#ifndef TESTS_OBJECTS_FROMFILE_H
#define TESTS_OBJECTS_FROMFILE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs a fromfile object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: fromfile.c
 */
extern unsigned short test_fromfile_initialize(void);

/*
 * Test the function which frees the memory stored by a fromfile object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: fromfile.c
 */
extern unsigned short test_fromfile_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_FROMFILE_H */
