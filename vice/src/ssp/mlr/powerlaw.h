
#ifndef SSP_MLR_POWERLAW_H
#define SSP_MLR_POWERLAW_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Determine the mass of dying stars in a star cluster of known age according
 * to the simple power-law formulation (see source file header).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Versions >= 1.1: This is the mass of a dying star taking into account their
 * 		post main sequence lifetimes.
 * Versions >= 1.2.1: This function handles errors more robustly in the event
 * 		that the age is either zero or negative. For zero age, it returns
 * 		INFINITY (500 if not defined), and for negative age, it returns NAN
 * 		(0 if not defined).
 * Versions >= 1.3.0: In prior versions, this was the only mass-lifetime
 * 		relation built into VICE. In subsequent versions, the user can choose
 * 		between this and other formalisms.
 *
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * This function depends on the compile-time constants SOLAR_LIFETIME and
 * MASS_LIFETIME_PLAW_INDEX declared in vice/src/ssp.h.
 *
 * source: powerlaw.c
 */
extern double powerlaw_turnoffmass(double time, double postMS, double Z);

/*
 * Compute the lifetime of a star of known mass according to the simple
 * power-law formulation (see source file header).
 *
 * Parameters
 * ==========
 * mass: 		The mass of the star in solar masses.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * This function depends on the compile-time constants SOLAR_LIFETIME and
 * MASS_LIFETIME_PLAW_INDEX declared in vice/src/ssp.h.
 *
 * source: powerlaw.c
 */
extern double powerlaw_lifetime(double mass, double postMS, double Z);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_POWERLAW_H */
