
#ifndef SSP_MSMF_H
#define SSP_MSMF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the main sequence mass fraction of a stellar population a some
 * time following its formation.
 *
 * Parameters
 * ==========
 * ssp: 		A SSP struct containing information on the stellar IMF and
 * 				the mass range of star formation
 * time: 		The age of the stellar population in Gyr
 *
 * Returns
 * =======
 * The value of the main sequence mass fraction at the specified age. -1 in
 * the case of an unrecognized IMF.
 *
 * source: ssp.c
 */
extern double MSMF(SSP ssp, double time);

/*
 * Evaluate the main sequence mass fraction across all timesteps in preparation
 * of a singlezone simulation. This will store the MSMF in the SSP struct
 * within the singlezone object.
 *
 * Parameters
 * ==========
 * sz: 		A singlezone object to setup the MSMF within
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: ssp.c
 */
extern unsigned short setup_MSMF(SINGLEZONE *sz);

/*
 * Determine the denominator of the main sequence mass fraction. This is
 * the total initial mass of the main sequence; see section 2.2 of VICE's
 * science documentation for further details.
 *
 * Parameters
 * ==========
 * ssp: 		A SSP struct containing information on the stellar IMF and
 * 				mass range of star formation
 *
 * Returns
 * =======
 * The total initial main sequence mass of the stellar population, up to the
 * normalization constant of the IMF. -1 in the case of an unrecognized IMF.
 *
 * Notes
 * =====
 * This calculation assumes solar metallicity in computing the main sequence
 * turnoff mass (0.014; Asplund et al. 2009). This drastically reduces
 * computing times by not requiring calculation of the CRF for all previous
 * timesteps. The effect of metallicity on the CRF is small, anyway.
 *
 * References
 * ==========
 * Asplund et al. (2009), ARA&A, 47, 481
 *
 * source: msmf.c
 */
extern double MSMFdenominator(SSP ssp);

/*
 * Determine the numerator of the main sequence mass fraction. This is the
 * total mass of stars still on the main sequence; see section 2.2 of VICE's
 * science documentation for further details.
 *
 * Parameters
 * ==========
 * ssp: 		A SSP struct containing information on the stellar IMF and
 * 				mass range of star formation
 * time: 		The age of the stellar population in Gyr
 *
 * Returns
 * =======
 * The total main sequence mass of the stellar population at the given age, up
 * to the normalization constant of the IMF.
 *
 * source: msmf.c
 */
extern double MSMFnumerator(SSP ssp, double t);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_MSMF_H */

