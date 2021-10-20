
#ifndef SSP_MLR_PM1993_H
#define SSP_MLR_PM1993_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism of Padovani & Matteucci (1993).
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
 * Padovani & Matteucci (1993), ApJ, 416, 26
 *
 * source: pm1993.c
 */
extern double pm1993_turnoffmass(double time, double postMS, double Z);

/*
 * Compute the lifetime of a star of known mass according to the formalism
 * of Padovani & Matteucci (1993).
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
 * Padovani & Matteucci (1993), ApJ, 416, 26
 *
 * source: pm1993.c
 */
extern double pm1993_lifetime(double mass, double postMS, double Z);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_PM1993_H */
