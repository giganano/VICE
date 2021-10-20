
#ifndef OBJECTS_CHANNEL_H
#define OBJECTS_CHANNEL_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a CHANNEL object.
 * Automatically initializes yield_ and rate to NULL. Allocates memory for and
 * fills the grid_.
 *
 * source: channel.c
 */
extern CHANNEL *channel_initialize(void);

/*
 * Free up the memory in a CHANNEL object.
 *
 * source: channel.c
 */
extern void channel_free(CHANNEL *ch);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_CHANNEL_H */

