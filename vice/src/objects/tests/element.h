
#ifndef TESTS_OBJECTS_ELEMENT_H
#define TESTS_OBJECTS_ELEMENT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Test the function which constructs an element object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: element.c
 */
extern unsigned short test_element_initialize(void);

/*
 * Test the function which frees the memory stored by an element object
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: element.c
 */
extern unsigned short test_element_free(void);

/*
 * Obtain a pointer to a test instance of the ELEMENT object.
 *
 * source: element.c
 */
extern ELEMENT *element_test_instance(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_OBJECTS_ELEMENT_H */
