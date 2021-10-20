
#ifndef OBJECTS_MULTIZONE_H
#define OBJECTS_MULTIZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocates memory for and returns a pointer to a multizone object
 *
 * Parameters
 * ==========
 * n: 		The number of zones in the simulation
 *
 * source: multizone.c
 */
extern MULTIZONE *multizone_initialize(unsigned int n);

/*
 * Frees the memory stored in a multizone object
 *
 * source: multizone.c
 */
extern void multizone_free(MULTIZONE *mz);


#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_MULTIZONE_H */

