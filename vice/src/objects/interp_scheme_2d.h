
#ifndef OBJECTS_INTERP_SCHEME_2D
#define OBJECTS_INTERP_SCHEME_2D

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an interp_scheme_2d object. The
 * number of x and y coordinates is automatically set to 0 and the coordinates
 * to NULL.
 *
 * header: interp_scheme_2d.h
 */
extern INTERP_SCHEME_2D *interp_scheme_2d_initialize(void);

/*
 * Free up the memory stored in an interp_scheme_2d object.
 *
 * source: interp_scheme_2d.c
 */
extern void interp_scheme_2d_free(INTERP_SCHEME_2D *is2d);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_INTERP_SCHEME_2D */
