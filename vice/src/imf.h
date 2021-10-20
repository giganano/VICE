
#ifndef IMF_H
#define IMF_H

#ifdef __cplusplus
extern "C" {
#endif

/* hash-code for the Kroupa (2001) IMF */
#ifndef KROUPA
#define KROUPA 658
#endif /* KROUPA */

/* hash code for the Salpeter (1955) IMF */
#ifndef SALPETER
#define SALPETER 864
#endif /* SALPETER */

/* hash code for a custom IMF */
#ifndef CUSTOM
#define CUSTOM 667
#endif /* CUSTOM */

/* The maximum size for the IMF's spec char pointer */
#ifndef SPEC_CHARP_SIZE
#define SPEC_CHARP_SIZE 100
#endif /* SPEC_CHARP_SIZE */

/* The stepsize taken in sampling a functional IMF */
#ifndef IMF_STEPSIZE
#define IMF_STEPSIZE 1e-3
#endif /* IMF_STEPSIZE */

#include "objects.h"
#include "objects/imf.h"

/*
 * Evaluate the IMF to an arbitrary normalization at the mass m
 *
 * Parameters
 * ==========
 * imf: 		The IMF object containing the parameters
 * m: 			The stellar mass to evaluate the IMF at
 *
 * Returns
 * =======
 * The un-normalized height of the IMF at that stellar mass
 *
 * source: imf.c
 */
extern double imf_evaluate(IMF_ imf, double m);

/*
 * The Salpeter (1955) stellar initial mass function (IMF) up to a
 * normalization constant.
 *
 * Parameters
 * ==========
 * m: 			The stellar mass in Msun
 *
 * Returns
 * =======
 * The value of the IMF at that mass up to the normalization of the IMF.
 * -1 if m < 0.
 *
 * References
 * ==========
 * Salpeter (1955), ApJ, 121, 161
 *
 * source: imf.c
 */
extern double salpeter55(double m);

/*
 * The Kroupa (2001) stellar initial mass function (IMF) up to a
 * normalization constant.
 *
 * Parameters
 * ==========
 * m: 			The stellar mass in Msun
 *
 * Returns
 * =======
 * The value of the IMF at that mass up to the normalization of the IMF.
 * -1 if m < 0.
 *
 * References
 * ==========
 * Kroupa (2001), MNRAS, 322, 231
 *
 * source: imf.c
 */
extern double kroupa01(double m);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IMF_H */


