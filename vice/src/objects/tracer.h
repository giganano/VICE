
#ifndef OBJECTS_TRACER_H
#define OBJECTS_TRACER_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "objects.h"

/*
 * Allocates memory for and returns a pointer to a TRACER particle.
 *
 * source: tracer.c
 */
extern TRACER *tracer_initialize(void);

/*
 * Frees up the memory stored by the tracer particle.
 *
 * source: tracer.c
 */
extern void tracer_free(TRACER *t);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_TRACER_H */

