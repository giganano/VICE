
#ifndef SSP_MLR_MM1989_H
#define SSP_MLR_MM1989_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism of Maeder & Meynet (1989).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence lifetime only.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * References
 * ==========
 * Maeder & Meynet (1989), A&A, 210, 155
 *
 * source: mm1989.c
 */
extern double mm1989_turnoffmass(double time, double postMS, double Z);

/*
 * Compute the lifetime of a star of known mass according to the formula from
 * Maeder & Meynet (1989).
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
 * Although this function accepts metallicity by mass as a parameter, this
 * form is metallicity-independent. This is included for consistency with other
 * mass-lifetime relations implemented here so that any one can be called with
 * a function pointer.
 *
 * References
 * ==========
 * Maeder & Meynet (1989), A&A, 210, 155
 *
 * source: mm1989.c
 */
extern double mm1989_lifetime(double mass, double postMS, double Z);

#ifdef __cpluslpus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_MM1989_H */

