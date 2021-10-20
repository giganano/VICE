
#ifndef OBJECTS_SNEIA_H
#define OBJECTS_SNEIA_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct.
 * Automatically initializes RIa to NULL. Allocates memory for a 100-character
 * dtd char * specifier.
 *
 * header: sneia.h
 */
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void);

/*
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct.
 *
 * header: sneia.h
 */
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_SNEIA_H */

