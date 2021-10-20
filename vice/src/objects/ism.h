
#ifndef OBJECTS_ISM_H
#define OBJECTS_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an ISM struct. Automatically
 * initializes all fields to NULL. Allocates memory for a 5-element char *
 * mode specifier.
 *
 * source: ism.c
 */
extern ISM *ism_initialize(void);

/*
 * Free up the memory stored in an ISM struct.
 *
 * source: ism.c
 */
extern void ism_free(ISM *ism);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_ISM_H */

