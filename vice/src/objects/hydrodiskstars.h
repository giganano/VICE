
#ifndef OBJECTS_HYDRODISKSTARS_H
#define OBJECTS_HYDRODISKSTARS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a hydrodiskstars object.
 *
 * source: hydrodiskstars.c
 */
extern HYDRODISKSTARS *hydrodiskstars_initialize(void);


/*
 * Free the memory stored by a hydrodiskstars object.
 *
 * source: hydrodiskstars.c
 */
extern void hydrodiskstars_free(HYDRODISKSTARS *hds);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_HYDRODISKSTARS_H */
