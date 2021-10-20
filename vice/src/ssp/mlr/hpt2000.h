
#ifndef SSP_MLR_HPT2000_H
#define SSP_MLR_HPT2000_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the formalism in section 5.1 of of Hurley, Pols & Tout (2000).
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
 * Although the lifetime is computed analytically from a star of known mass
 * under the Hurley, Pols & Tout (2000) formalism, the equation is not
 * invertible analytically. This solution is thus computed numerically using
 * the bisection method (header file: root.h).
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 *
 * source: hpt2000.c
 */
extern double hpt2000_turnoffmass(double time, double postMS, double Z);

/*
 * Compute the lifetime of a star of known mass according to the formalism
 * in section 5.1 of Hurley, Pols & Tout (2000).
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
 * source: hpt2000.c
 */
extern double hpt2000_lifetime(double mass, double postMS, double Z);

/*
 * Import the Hurley, Pols & Tout (2000) data. This function must be called
 * from python before hpt2000_lifetime or hpt2000_turnoffmass can be called,
 * otherwise a segmentation fault will occur.
 *
 * Parameters
 * ==========
 * filename: 	The full path to the file holding the data.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: hpt2000.c
 */
extern unsigned short hpt2000_import(char *filename);

/*
 * Free up the memory stored by the Hurley, Pols & Tout (2000) data.
 *
 * References
 * ==========
 * Hurley, Pols & Tout (2000), MNRAS, 315, 543
 *
 * source: hpt2000.c
 */
extern void hpt2000_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_HPT2000_H */
