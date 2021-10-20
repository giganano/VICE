
#ifndef OBJECTS_SSP_H
#define OBJECTS_SSP_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* default lower mass limit before being overridden in python */
#ifndef SSP_IMF_DEFAULT_M_LOWER
#define SSP_IMF_DEFAULT_M_LOWER 0.08
#endif /* SSP_IMF_DEFAULT_M_LOWER */

/* default upper mass limit before being overridden in python */
#ifndef SSP_IMF_DEFAULT_M_UPPER
#define SSP_IMF_DEFAULT_M_UPPER 100
#endif /* SSP_IMF_DEFAULT_M_UPPER */

#include "objects.h"

/*
 * Allocate memory for and return a pointer to an SSP struct. Automatically
 * sets both crf and msmf to NULL. Allocates memory for a 100-element char *
 * IMF specifier.
 *
 * source: ssp.c
 */
extern SSP *ssp_initialize(void);

/*
 * Free up the memory stored in an SSP struct.
 *
 * source: ssp.c
 */
extern void ssp_free(SSP *ssp);

#ifdef __cplusplus
}
#endif /* __cplusplus*/

#endif /* OBJECTS_SSP_H */

