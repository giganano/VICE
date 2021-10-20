/*
 * This file implements the time evolution of the interstellar medium (ISM)
 * in VICE's singlezone simulations.
 */

#include <stdlib.h>
#include <math.h>
#include "../singlezone.h"
#include "../callback.h"
#include "../ssp.h"
#include "../ism.h"
#include "../utils.h"
#include "ism.h"


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
 * header: ism.h
 */
extern unsigned short setup_gas_evolution(SINGLEZONE *sz) {

	/* SFR = MG * tau_star^-1 */

	switch (checksum((*(*sz).ism).mode)) {

		case GAS:
			/*
			 * Set initial mass and star formation rate. If we only know the
			 * initial mass, there's no way to define an infall rate at t = 0.
			 */
			sz -> ism -> mass = (*(*sz).ism).specified[0];
			sz -> ism -> star_formation_rate = ((*(*sz).ism).mass /
				get_SFE_timescale(*sz, 1u));
			/*
			 * Take into account definition of NAN for generating the
			 * manylinux1 distributions.
			 */
			#ifdef NAN
				sz -> ism -> infall_rate = NAN;
			#else
				sz -> ism -> infall_rate = 0;
			#endif
			break;

		case IFR:
			/* initial gas supply set by python in this case */
			sz -> ism -> infall_rate = (*(*sz).ism).specified[0];
			sz -> ism -> star_formation_rate = ((*(*sz).ism).mass /
				get_SFE_timescale(*sz, 1u));
			break;

		case SFR:
			sz -> ism -> star_formation_rate = (*(*sz).ism).specified[0];
			sz -> ism -> mass = get_ism_mass_SFRmode(*sz, 0u);
			/* manylinux1 distributions, see above comment */
			#ifdef NAN
				sz -> ism -> infall_rate = NAN;
			#else
				sz -> ism -> infall_rate = 0;
			#endif
			break;

		default:
			return 1u; 		/* unrecognized mode */
	}

	/* Run the sanity checks to impose the lower bound */
	update_gas_evolution_sanitycheck(sz);

	/* Allocate memory for the star formation history at each timestep */
	sz -> ism -> star_formation_history = (double *) malloc (
		((unsigned long) ((*sz).output_times[(*sz).n_outputs - 1l] / (*sz).dt)
			+ 10l) * sizeof(double));
	sz -> ism -> star_formation_history[0l] = (*(*sz).ism).star_formation_rate;
	return 0u;

}


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
 * header: ism.h
 */
extern unsigned short update_gas_evolution(SINGLEZONE *sz) {

	/*
	 * The relation between star formation rate, infall rate, gas supply,
	 * timestep size, outflow rate, recycling rate, and star formation
	 * efficiency timescale:
	 *
	 * SFR = MG * tau_star^-1
	 *
	 * dMG = (IFR - SFR - OFR) * dt + M_recycled
	 *
	 * Primordial inflow is taken into account prior to updating the infall and
	 * gas supply so that there isn't a 1-timestep delay or advance in the
	 * amount of helium added
	 */

	primordial_inflow(sz);
	switch (checksum((*(*sz).ism).mode)) {

		case GAS:
			sz -> ism -> mass = (*(*sz).ism).specified[(*sz).timestep + 1l];
			sz -> ism -> star_formation_rate = ((*(*sz).ism).mass /
				get_SFE_timescale(*sz, 0u));
			sz -> ism -> infall_rate = (
				((*(*sz).ism).mass - (*(*sz).ism).specified[(*sz).timestep] -
					mass_recycled(*sz, NULL)) / (*sz).dt +
				(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz)
			);
			break;

		case IFR:
			sz -> ism -> mass += (
				((*(*sz).ism).infall_rate - (*(*sz).ism).star_formation_rate -
					get_outflow_rate(*sz)) * (*sz).dt + mass_recycled(*sz, NULL)
			);
			sz -> ism -> infall_rate = (*(*sz).ism).specified[(
				*sz).timestep + 1l];
			sz -> ism -> star_formation_rate = ((*(*sz).ism).mass /
				get_SFE_timescale(*sz, 0u));
			break;

		case SFR:
			sz -> ism -> star_formation_rate = (
				*(*sz).ism).specified[(*sz).timestep + 1l];
			double dMg = get_ism_mass_SFRmode(*sz, 0u) - (*(*sz).ism).mass;
			sz -> ism -> infall_rate = (
				(dMg - mass_recycled(*sz, NULL)) / (*sz).dt +
				(*(*sz).ism).star_formation_rate + get_outflow_rate(*sz)
			);
			sz -> ism -> mass += dMg;
			break;

		default:
			return 1u;

	}

	update_gas_evolution_sanitycheck(sz);
	sz -> ism -> star_formation_history[(*sz).timestep + 1l] = (
		*(*sz).ism).star_formation_rate;
	return 0u;

}

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
 * header: ism.h
 */
extern double get_SFE_timescale(SINGLEZONE sz, unsigned short setup) {

	/*
	 * If this function is not being called on singlezone setup, get the
	 * SFE timescale at the next timestep
	 */
	setup = 1 - setup;
	if ((*(*sz.ism).functional_tau_star).user_func != NULL) {
		/* User-specified function of time and gas mass, in that order. */
		return callback_2arg_evaluate(*(*sz.ism).functional_tau_star,
			sz.current_time, (*sz.ism).mass);
	} else if ((*sz.ism).schmidt) {
		/* Single-zone implementation of Kennicutt-Schmidt Law */
		return ((*sz.ism).tau_star[sz.timestep + setup] *
			pow((*sz.ism).mass / (*sz.ism).mgschmidt,
				-(*sz.ism).schmidt_index));
	} else {
		/* Instantaneous star formation efficiency */
		return (*sz.ism).tau_star[sz.timestep + setup];
	}

}


/*
 * Determines the mass of the ISM at the NEXT timestep when the simulation is
 * ran in SFR mode.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 * setup: 	1 if this function is being called from the setup, 0 otherwise
 *
 * Returns
 * =======
 * The mass of the ISM at the next timestep
 *
 * header: ism.h
 */
extern double get_ism_mass_SFRmode(SINGLEZONE sz, unsigned short setup) {

	/*
	 * The following are the analytically determined solutions for the gas
	 * supply under the equations in section 3.1 of VICE's science
	 * documentation. Special consideration must be taken aside from a simple
	 * SFR x get_SFE_timescale approach because this introduces numerical
	 * artifacts when the star formation rate is low.
	 *
	 * If this function is not being called on singlezone setup, get the SFE
	 * timescale at the next timestep.
	 */

	setup = 1 - setup;
	double tau_star;
	if ((*(*sz.ism).functional_tau_star).user_func != NULL) {
		/*
		 * User-specified function of time and star formation rate, in that
		 * order. Users specify star formation rate in Msun/yr, however, while
		 * this code records in Msun/Gyr, so add factor of 1e-9 for
		 * consistency.
		 */
		tau_star = callback_2arg_evaluate(*(*sz.ism).functional_tau_star,
			sz.current_time, 1e-9 * (*sz.ism).star_formation_rate);
	} else if ((*sz.ism).schmidt) {
		if ((*sz.ism).star_formation_rate) {
			/* The value implied by the current star formation rate */
			tau_star = (
				pow(
					(*sz.ism).tau_star[sz.timestep + setup],
					1 / (1 + (*sz.ism).schmidt_index)
				) * pow(
					(*sz.ism).star_formation_rate / (*sz.ism).mgschmidt,
					-(*sz.ism).schmidt_index / (1 + (*sz.ism).schmidt_index)
				)
			);
		} else {
			tau_star = 0;
		}
	} else {
		tau_star = (*sz.ism).tau_star[sz.timestep + setup];
	}

	return (*sz.ism).star_formation_rate * tau_star;

}


/*
 * Performs a sanity check on the ISM parameters immediately after they
 * were updated one timestep in a singlezone simulation.
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object to sanity check
 *
 * header: ism.h
 */
extern void update_gas_evolution_sanitycheck(SINGLEZONE *sz) {

	/*
	 * All three of the ISM mass, the star formation rate, and infall rate
	 * are forced to be positive definite by imposing a lower bound at
	 * 10^-12 in the adopted unit system. This avoids unphysical parameter
	 * spaces and numerical artifacts at zero.
	 */
	if ((*(*sz).ism).mass < 1e-12) {
		sz -> ism -> mass = 1e-12;
	} else {}

	if ((*(*sz).ism).star_formation_rate < 0) {
		sz -> ism -> star_formation_rate = 0;
	} else {}
	
	if ((*(*sz).ism).infall_rate < 0) {
		sz -> ism -> infall_rate = 0;
	} else {}

}


/*
 * Takes into account each element's primordial abundance in the inflow
 *
 * Parameters
 * ==========
 * sz: 		A pointer to the singlezone object for this simulation
 *
 * header: ism.h
 */
extern void primordial_inflow(SINGLEZONE *sz) {

	if (!isnan((*(*sz).ism).infall_rate)) {
		unsigned int i;
		for (i = 0; i < (*sz).n_elements; i++) {
			sz -> elements[i] -> mass += (
				(*(*sz).ism).infall_rate * (*sz).dt *
				(*(*sz).elements[i]).primordial
			);
		}
	} else {}

}


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
 * mass outflow rate from the ISM. Outflow metallicities and the *total* mass
 * outflow rate are calculated in write_zone_history in src/io/singlezone.c.
 *
 * header: ism.h
 */
extern double get_outflow_rate(SINGLEZONE sz) {

	if ((*sz.ism).smoothing_time < sz.dt) {
		/*
		 * If the smoothing time is less than the timestep, there's no
		 * timesteps to smooth over.
		 *
		 * outflow_rate = eta * smoothed star formation rate + unretained
		 */
		return (*sz.ism).eta[sz.timestep] * (*sz.ism).star_formation_rate;

	} else {
		/* The number of timesteps to smooth over */
		unsigned long i, n = (unsigned long) ((*sz.ism).smoothing_time /
			sz.dt);
		double mean_sfr = 0;
		if (n > sz.timestep) {
			/*
			 * If the simulation hasn't reached this many timesteps yet.
			 *
			 * In either case, simply add up the previous star formation rates
			 * and divide by the number of timesteps.
			 */
			for (i = 0l; i <= sz.timestep; i++) {
				mean_sfr += (*sz.ism).star_formation_history[sz.timestep - i];
			}
			mean_sfr /= sz.timestep + 1l;
		} else {
			for (i = 0l; i <= n; i++) {
				mean_sfr += (*sz.ism).star_formation_history[sz.timestep - i];
			}
			mean_sfr /= n + 1l;
		}

		return (*sz.ism).eta[sz.timestep] * mean_sfr;
	}

}


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
 * header: ism.h
 */
extern double *singlezone_unretained(SINGLEZONE sz) {

	unsigned short i;
	double *unretained = (double *) malloc (sz.n_elements * sizeof(double));
	for (i = 0u; i < sz.n_elements; i++) {
		unretained[i] = (*sz.elements[i]).unretained / sz.dt;
	}
	return unretained;

}

