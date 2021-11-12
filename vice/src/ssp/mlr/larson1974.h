
#ifndef SSP_MLR_LARSON1974_H
#define SSP_MLR_LARSON1974_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Calculate the mass of dying stars in a single stellar population of known
 * age according to the Larson (1974) analytic form with parameters taken
 * from Kobayashi (2004).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of the post main sequence lifetime to the main
 * 				sequence lifetime. Zero for main sequence turnoff mass alone.
 * Z: 			The metallicity of the stellar population.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * Though the Larson (1974) MLR is metallicity-independent, all mass-lifetime
 * relations in VICE are implemented as functions of both mass and metallicity.
 * See source file for the analytic form.
 *
 * References
 * ==========
 * Kobayashi (2004), MNRAS, 347, 740
 * Larson (1974), MNRAS, 166, 585
 *
 * source: larson1974.c
 */
extern double larson1974_turnoffmass(double time, double postMS, double Z);

/*
 * Calculate the lifetime of a star of known mass in Gyr according to the
 * Larson (1974) analytic form with parameters taken from Kobayashi (2004).
 *
 * Parameters
 * ==========
 * mass: 		The mass of the star in solar masses
 * postMS: 		The ratio of the post main sequence lifetime to the main
 * 				sequence lifetime. Zero for main sequence lifetime alone.
 * Z: 			The metallicity of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * Though the Larson (1974) MLR is metallicity-independent, all mass-lifetime
 * relations in VICE are implemented as functions of both mass and metallicity.
 * See source file for the analytic form.
 *
 * References
 * ==========
 * Kobayashi (2004), MNRAS, 347, 740
 * Larson (1972), MNRAS, 166, 585
 *
 * source: larson1974.c
 */
extern double larson1974_lifetime(double mass, double postMS, double Z);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_LARSON1974_H */
