
#ifndef OBJECTS_AGB_H
#define OBJECTS_AGB_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an AGB_YIELD_GRID struct and
 * initialize all fields to NULL.
 *
 * source: agb.c
 */
extern AGB_YIELD_GRID *agb_yield_grid_initialize(void);

/*
 * Free up the memory stored in an AGB_YIELD_GRID struct
 *
 * source: agb.c
 */
extern void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_AGB_H */

