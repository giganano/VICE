
#ifndef SSP_H
#define SSP_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/* main sequence lifetime ~ M^-MASS_LIFETIME_PLAW_INDEX */
#ifndef MASS_LIFETIME_PLAW_INDEX
#define MASS_LIFETIME_PLAW_INDEX 3.5
#endif /* MASS_LIFETIME_PLAW_INDEX */

/* The lifetime of the sun in Gyr */
#ifndef SOLAR_LIFETIME
#define SOLAR_LIFETIME 10
#endif /* SOLAR_LIFETIME */

/* Tolerance on numerical integration of SSP quantities */
#ifndef SSP_TOLERANCE
#define SSP_TOLERANCE 1e-3
#endif /* SSP_TOLERANCE */

/*
 * Hash-code for simpson's rule
 * User modification strongly discouraged
 */
#ifndef SSP_METHOD
#define SSP_METHOD 777
#endif /* SSP_METHOD */

/*
 * Minimum number of bins in quadrature
 * User modification strongly discouraged
 */
#ifndef SSP_NMIN
#define SSP_NMIN 64l
#endif /* SSP_NMIN */

/*
 * Maximum number of bins in quadrature
 * User modification strongly discouraged
 */
#ifndef SSP_NMAX
#define SSP_NMAX 2e8
#endif /* SSP_NMAX */

#include "objects.h"
#include "objects/ssp.h"
#include "ssp/crf.h"
#include "ssp/mlr.h"
#include "ssp/msmf.h"
#include "ssp/remnants.h"
#include "ssp/ssp.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_H */

