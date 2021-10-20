
#ifndef SSP_REMNANTS_H
#define SSP_REMNANTS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * The Kalirai et al. (2008) initial-final remnant mass relationship
 *
 * Parameters
 * ==========
 * m: 		The initial stellar mass in Msun
 *
 * Returns
 * =======
 * The mass of the remnant under the Kalirai et al. (2008) model. Stars with
 * main sequence masses >= 8 Msun leave behind a 1.44 Msun remnant. Those < 8
 * Msun leave behind a 0.394 + 0.109 * m Msun mass remnant.
 *
 * References
 * ==========
 * Kalirai et al. (2008), ApJ, 676, 594
 *
 * source: remnants.c
 */
extern double Kalirai08_remnant_mass(double m);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_REMNANTS_H */

