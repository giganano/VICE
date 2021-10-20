
#ifndef SSP_CRF_H
#define SSP_CRF_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Determine the cumulative return fraction from a single stellar population
 * a given time in Gyr after its formation.
 *
 * Parameters
 * ==========
 * ssp: 		An SSP struct containing information on the stallar IMF and
 * 				the mass range of star formation
 * time: 		The age of the stellar population in Gyr
 *
 * Returns
 * =======
 * The value of the CRF at that time for the IMF assumptions encoded into the
 * SSP struct
 *
 * source: ssp.c
 */
extern double CRF(SSP spp, double time);

/*
 * Evaluate the cumulative return fraction across all timesteps in preparation
 * of a singlezone simulation. This will store the CRF in the SSP struct
 * within the singlezone object.
 *
 * Parameters
 * ==========
 * sz: 		A singlezone object to setup the CRF within
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: ssp.c
 */
extern unsigned short setup_CRF(SINGLEZONE *sz);

/*
 * Determine the denominator of the cumulative return fraction. This is the
 * total mass of a single stellar population up to the normalization
 * constant of the IMF. This is determined by the mass range of star
 * formation and the IMF itself. See section 2.2 of VICE's science
 * documentation for details.
 *
 * Parameters
 * ==========
 * ssp: 		The SSP struct containing information on the IMF and the
 * 				allowed mass ranges of star formation
 *
 * Returns
 * =======
 * The denominator of the cumulative return fraction. When the returned mass
 * determined by functions in this module is divided by this value, the
 * CRF is determined. -1 in the case of an unrecognized IMF.
 *
 * source: crf.c
 */
extern double CRFdenominator(SSP ssp);

/*
 * Determine one term in the denominator of the cumulative return fraction.
 * See section 2.2 of VICE's science documentation for further details.
 *
 * Parameters
 * ==========
 * m_upper: 		The upper mass limit on this range of star formation
 * m_lower: 		The lower mass limit on this range of star formation
 * a: 				The power law index on the stellar IMF here
 *
 * Returns
 * =======
 * The total initial main sequence mass formed in a given range of star
 * formation, up to the normalization constant of the IMF.
 *
 * source: crf.c
 */
extern double CRFdenominator_IMFrange(double m_upper, double m_lower,
	double a);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SSP_CRF_H */

