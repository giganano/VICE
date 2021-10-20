
#ifndef OBJECTS_INTERP_SCHEME_1D_H
#define OBJECTS_INTERP_SCHEME_1D_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an interp_scheme_1d object. The
 * number of points is automatically set to 0 and the coordinates to NULL.
 *
 * source: interp_scheme_1d.c
 */
extern INTERP_SCHEME_1D *interp_scheme_1d_initialize(void);


/*
 * Free up the memory stored in an interp_scheme_1d object.
 *
 * source: interp_scheme_1d.c
 */
extern void interp_scheme_1d_free(INTERP_SCHEME_1D *is1d);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_INTERP_SCHEME_1D_H */

