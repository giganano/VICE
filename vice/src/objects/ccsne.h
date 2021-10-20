
#ifndef OBJECTS_CCSNE_H
#define OBJECTS_CCSNE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a CCSNE_YIELD_SPECS struct.
 * This also allocates memory for the grid of metallicities and automatically
 * fills it with the grid defined by CC_YIELD_GRID_MIN, CC_YIELD_GRID_MAX,
 * and CC_YIELD_STEP as defined in ccsne.h. Initializes the yield_ value to
 * NULL.
 *
 * source: ccsne.c
 */
extern CCSNE_YIELD_SPECS *ccsne_yield_initialize(void);

/*
 * Free up the memory stored in a CCSNE_YIELD_SPECS struct
 *
 * source: ccsne.c
 */
extern void ccsne_yield_free(CCSNE_YIELD_SPECS *ccsne_yield);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_CCSNE_H */

