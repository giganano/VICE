
#ifndef OBJECTS_SINGLEZONE_H
#define OBJECTS_SINGLEZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a SINGLEZONE struct.
 * Automatically initializes all fields to NULL.
 *
 * source: singlezone.c
 */
extern SINGLEZONE *singlezone_initialize(void);

/*
 * Free up the memory associated with a singlezone object.
 *
 * source: singlezone.c
 */
extern void singlezone_free(SINGLEZONE *sz);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_SINGLEZONE_H */

