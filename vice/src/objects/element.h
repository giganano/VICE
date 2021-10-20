
#ifndef OBJECTS_ELEMENT_H
#define OBJECTS_ELEMENT_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for an return a pointer to an ELEMENT struct. This also
 * allocates memory for the AGB_YIELD_GRID, CCSNE_YIELD_SPECS, and
 * SNEIA_YIELD_SPECS stored in the ELEMENT struct. Allocates memory for a
 * 5-element string for each element's symbol.
 *
 * source: element.c
 */
extern ELEMENT *element_initialize(void);

/*
 * Free up the memory stored in an ELEMENT struct
 *
 * source: element.c
 */
extern void element_free(ELEMENT *e);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_ELEMENT_H */

