
#ifndef MULTIZONE_HYDRODISKSTARS_H
#define MULTIZONE_HYDRODISKSTARS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/* The hash-code for "linear" mode */
#ifndef LINEAR_MIGRATION
#define LINEAR_MIGRATION 635
#endif /* LINEAR_MIGRATION */

/* The hash-code for "sudden" migration */
#ifndef SUDDEN_MIGRATION
#define SUDDEN_MIGRATION 643
#endif /* SUDDEN_MIGRATION */

/* The hash-code for "diffusion" migration */
#ifndef DIFFUSION_MIGRATION
#define DIFFUSION_MIGRATION 967
#endif /* DIFFUSION_MIGRATION */

/*
 * Set the hydrodiskstars object globally.
 *
 * Parameters
 * ==========
 * address: The address of the hydrodiskstars object
 *
 * Notes
 * =====
 * This is necessary to avoid issues with the Cython compiler. Since the
 * multizone and hydrodiskstars objects are separate, the _hds attribute of
 * the c_hydrodiskstars object cannot be accessed by the multizone object.
 *
 * source: hydrodiskstars.c
 */
extern void set_hydrodiskstars_object(unsigned long address);

/*
 * Setup the zone history for a single tracer object born in a given zone and
 * at a given timestep.
 *
 * Parameters
 * ==========
 * mz: 				The multizone object
 * hds: 			The hydrodiskstars object
 * t: 				A pointer to the tracer object being set up
 * birth_zone: 		The zone of birth
 * birth_timestep: 	The timestep of birth
 * analog_index: 	The index of the analog star particle in the hds data
 *
 * Returns
 * =======
 * 0 on success, 1 on failure.
 *
 * source: hydrodiskstars.c
 */
extern unsigned short setup_hydrodisk_tracer(MULTIZONE mz, TRACER *t,
	unsigned int birth_zone, unsigned long birth_timestep, long analog_index);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MULTIZONE_HYDRODISKSTARS_H */
