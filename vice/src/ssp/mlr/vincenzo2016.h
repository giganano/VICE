
#ifndef SSP_MLR_VINCENZO2016_H
#define SSP_MLR_VINCENZO2016_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../../objects.h"

/*
 * Compute the mass of dying stars in a star cluster of known age according to
 * the Vincenzo et al. (2016) formalism (see source file for analytic form).
 *
 * Parameters
 * ==========
 * time: 		The age of the stellar population in Gyr.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetime. Zero for the main sequence turnoff mass.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The mass of the stars dying at that time in solar masses.
 *
 * Notes
 * =====
 * The Vincenzo et al. (2016) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * source: vincenzo2016.c
 */
extern double vincenzo2016_turnoffmass(double time, double postMS, double Z);

/*
 * Compute the lifetime of a star of known mass according to the Vincenzo et
 * al. (2016) formalism (see source file for analytic form).
 *
 * Parameters
 * ==========
 * mass: 		Stellar mass in solar masses.
 * postMS: 		The ratio of a star's post main sequence lifetime to its main
 * 				sequence lifetimes. Zero for just the main sequence lifetime.
 * Z: 			The metallicity by mass of the star.
 *
 * Returns
 * =======
 * The lifetime of the star in Gyr.
 *
 * Notes
 * =====
 * The Vincenzo et al. (2016) relation quantifies the relationship between
 * stellar mass and total lifetime, making the parameter postMS superfluous.
 * Although this formalism is independent of its value, the same call signature
 * as other mass-lifetime relations is retained here so than any one of them
 * can be called with a function pointer.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * source: vincenzo2016.c
 */
extern double vincenzo2016_lifetime(double mass, double postMS, double Z);

/*
 * Assign the full path to the Vincenzo et al. (2016) data to be stored as a
 * global within this file.
 *
 * Parameters
 * ==========
 * filename: 		The full path to the file
 *
 * source: vincenzo2016.c
 */
extern void set_vincenzo2016_filename(char *filename);

/*
 * Import the Vincenzo et al. (2016) data. This function must be called by
 * python before vincenzo2016_lifetime or vincenzo2016_turnoff mass can be
 * called, otherwise a segmentation fault will occur.
 *
 * Parameters
 * ==========
 * filename: 		The name of the file holding the data.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * source: vincenzo2016.c
 */
extern unsigned short vincenzo2016_import(char *filename);

/*
 * Free up the memory stored by the interpolation schema.
 *
 * References
 * ==========
 * Vincenzo et al. (2016), MNRAS, 460, 2238
 *
 * source: vincenzo2016.c
 */
extern void vincenzo2016_free(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MLR_VINCENZO2016_H */
