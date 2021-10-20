
#ifndef MULTIZONE_MDF_H
#define MULTIZONE_MDF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Resets all MDFs in a multizone object and fills them with the data from
 * its tracer particles.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object to redo the MDF for
 *
 * source: mdf.c
 */
extern void tracers_MDF(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_MDF_H */

