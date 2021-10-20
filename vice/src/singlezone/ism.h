
#ifndef SINGLEZONE_ISM_H
#define SINGLEZONE_ISM_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Initialize the ISM mass, star formation rate, and infall rate in
 * preparation of a singlezone simulation
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to setup the evolution for
 *
 * Returns
 * =======
 * 0 on success, 1 on an unrecognized mode
 *
 * source: ism.c
 */
extern unsigned short setup_gas_evolution(SINGLEZONE *sz);

/*
 * Moves the infall rate, total gas mass, and star formation rate in a
 * singlezone simulation forward one timestep
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object for the current simulation
 *
 * Returns
 * =======
 * 0 on success; 1 on an unrecognized mode
 *
 * source: ism.c
 */
extern unsigned short update_gas_evolution(SINGLEZONE *sz);

/*
 * Determine the star formation efficiency timescale at the NEXT timestep.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 * setup: 	1 if this function is being called from the setup, 0 otherwise
 *
 * Returns
 * =======
 * The timescale relating star formation rate and gas supply in Gyr at the
 * next timestep.
 *
 * source: ism.c
 */
extern double get_SFE_timescale(SINGLEZONE sz, unsigned short setup);

/*
 * Determines the mass of the ISM at the NEXT timestep when the simulation is
 * ran in SFR mode.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * Returns
 * =======
 * The mass of the ISM at the next timestep
 *
 * source: ism.c
 */
extern double get_ism_mass_SFRmode(SINGLEZONE sz, unsigned short setup);

/*
 * Performs a sanity check on the ISM parameters immediately after they
 * were updated one timestep in a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to sanity check
 *
 * source: ism.c
 */
extern void update_gas_evolution_sanitycheck(SINGLEZONE *sz);

/*
 * Takes into account each element's primordial abundance in the inflow
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object for this simulation
 *
 * source: ism.c
 */
extern void primordial_inflow(SINGLEZONE *sz);

/*
 * Determine the ISM mass outflow rate in a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * Returns
 * =======
 * The mass outflow rate in Msun/Gyr
 *
 * Notes
 * =====
 * This function does not take into account entrainment of nucleosynthetic
 * products. This only determines the value of \eta<\dot{M}_\star>_\tau_s, the
 * mass outflow rate from the ISM. Outflow metallicities are recalcualted in
 * write_zone_history in src/io/singlezone.c.
 *
 * source: ism.c
 */
extern double get_outflow_rate(SINGLEZONE sz);

/*
 * Determines the mass outflow rate of each element in a singlezone simulation
 * due solely to entrainment.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * Returns
 * =======
 * mass: The mass added to the outflow at the current timestep in Msun divided
 * by the timestep size in Gyr.
 *
 * source: ism.c
 */
extern double *singlezone_unretained(SINGLEZONE sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SINGLEZONE_ISM_H */

