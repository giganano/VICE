
#ifndef OBJECTS_MDF_H
#define OBJECTS_MDF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an MDF struct. Initializes all
 * fields to NULL.
 *
 * source: mdf.c
 */
extern MDF *mdf_initialize(void);

/*
 * Free up the memory stored in an MDF struct.
 *
 * source: mdf.c
 */
extern void mdf_free(MDF *mdf);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_MDF_H */

