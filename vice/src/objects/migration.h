
#ifndef OBJECTS_MIGRATION_H
#define OBJECTS_MIGRATION_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for an return a pointer to a migration object.
 *
 * Parameters
 * ==========
 * n:		The number of zones in the multizone simulation
 *
 * source: migration.c
 */
extern MIGRATION *migration_initialize(unsigned int n);

/*
 * Free up the memory stored in a migration object.
 *
 * source: migration.c
 */
extern void migration_free(MIGRATION *mig);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_MIGRATION_H */

