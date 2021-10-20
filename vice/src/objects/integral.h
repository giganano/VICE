
#ifndef OBJECTS_INTEGRAL_H
#define OBJECTS_INTEGRAL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an integral object.
 *
 * source: integral.c
 */
extern INTEGRAL *integral_initialize(void);

/*
 * Free up the memory stored in the integral object.
 *
 * source: integral.c
 */
extern void integral_free(INTEGRAL *intgrl);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_INTEGRAL_H */

