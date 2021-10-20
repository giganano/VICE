
#ifndef SSP_MLR_H
#define SSP_MLR_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"
#include "./mlr/hpt2000.h"
#include "./mlr/ka1997.h"
#include "./mlr/larson1974.h"
#include "./mlr/mm1989.h"
#include "./mlr/pm1993.h"
#include "./mlr/powerlaw.h"
#include "./mlr/root.h"
#include "./mlr/vincenzo2016.h"

/* The hash-code for the power-law MLR */
#ifndef POWERLAW
#define POWERLAW 881u
#endif /* POWERLAW */

/* The hash-code for the Vincenzo et al. (2016) MLR */
#ifndef VINCENZO2016
#define VINCENZO2016 1077u
#endif /* VINCENZO2016 */

/* The hash-code for the Hurley, Pols & Tout (2000) MLR */
#ifndef HPT2000
#define HPT2000 526u
#endif /* HPT2000 */

/* The hash-code for the Kodama & Arimoto (1997) MLR */
#ifndef KA1997
#define KA1997 422u
#endif /* KA1997 */

/* The hash-code for the Padovani & Matteucci (1993) MLR */
#ifndef PM1993
#define PM1993 435u
#endif /* PM1993 */

/* The hash-code for the Maeder & Meynet (1989) MLR */
#ifndef MM1989
#define MM1989 437u
#endif /* MM1989 */

/* The hash-code for the Larson (1974) MLR */
#ifndef LARSON1974
#define LARSON1974 868u
#endif /* LARSON1974 */

/*
 * Determine the mass of dying stars from a single stellar population of known
 * age under the current mass-lifetime relationship setting.
 *
 * Parameters
 * ==========
 * time: 			The age of the stellar population in Gyr
 * postMS: 			The ratio of a star's post main sequence lifetime to its
 * 					main sequence lifetime. Zero for main sequence turnoff mass.
 * Z: 				The metallicity by mass of the stellar population.
 *
 * Returns
 * =======
 * The mass of stars in solar masses whose lifetime is given by the first
 * parameter.
 *
 * Notes
 * =====
 * Although not all mass-lifetime relationships implemented in VICE are
 * metallicity dependent and some take into account the post main sequence
 * lifetime already, this function accepts all three as parameters as do they
 * so that any can be called with a function pointer.
 * See header files in ./vice/src/ssp/mlr/ for details.
 *
 * source: mlr.c
 */
extern double dying_star_mass(double time, double postMS, double Z);

/*
 * Get the hashcode of the current mass-lifetime relationship setting. Their
 * values are #define'd in ./vice/src/ssp/mlr.h.
 *
 * source: mlr.c
 */
extern unsigned short get_mlr_hashcode(void);

/*
 * Set the global mass-lifetime relationship setting via the hashcodes
 * attached to each of them #define'd in ./vice/src/ssp/mlr.h.
 *
 * Parameters
 * ==========
 * hashcode: 		The hashcode corresponding to the desired MLR. See header
 * 					file for allowed values.
 *
 * Returns
 * =======
 * 0 on success, 1 on an unrecognized hashcode.
 *
 * source: mlr.c
 */
extern unsigned short set_mlr_hashcode(unsigned short hashcode);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_H */

