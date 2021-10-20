
#ifndef OBJECTS_FROMFILE_H
#define OBJECTS_FROMFILE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory and return a pointer to a fromfile object. Automatically
 * allocates memory for the name of the file.
 *
 * source: fromfile.c
 */
extern FROMFILE *fromfile_initialize(void);

/*
 * Free up the memory stored in a fromfile object.
 *
 * source: fromfile.c
 */
extern void fromfile_free(FROMFILE *ff);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_FROMFILE_H */

