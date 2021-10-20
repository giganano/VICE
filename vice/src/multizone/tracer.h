
#ifndef MULTIZONE_TRACER_H
#define MULTIZONE_TRACER_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Injects tracer particles into a multizone object for the current timestep
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * Notes
 * =====
 * This function updates the tracer count only if the new tracer particles
 * formed before the final output time. This'll ensure that superfluous tracer
 * particles are left out of the output and distribution function calculations.
 *
 * source: tracer.c
 */
extern void inject_tracers(MULTIZONE *mz);

/*
 * Compute the masses of each tracer particle after a multizone simulation in
 * simple mode.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object
 *
 * source: tracer.c
 */
extern void compute_tracer_masses(MULTIZONE *mz);

/*
 * Determine the metallicity of a tracer particle.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object for the current simulation
 * t: 		The tracer particle to determine the metallicity of
 *
 * Returns
 * =======
 * The scaled metallicity of the tracer particle
 *
 * source: tracer.c
 */
extern double tracer_metallicity(MULTIZONE mz, TRACER t);

/*
 * Allocate memory for the stellar tracer particles
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for this simulation
 *
 * source: tracer.c
 */
extern void malloc_tracers(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_TRACER_H */

