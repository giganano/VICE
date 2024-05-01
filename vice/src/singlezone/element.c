/*
 * This file implements the evolution of element objects in VICE's singlezone
 * simulations.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../singlezone.h"
#include "../ssp.h"
#include "../element.h"
#include "element.h"


/*
 * Allocates memory for bookkeeping each elements previous ISM metallicity
 * and sets each element to zero.
 *
 * Parameters
 * ==========
 * e: 				A pointer to the element to setup the Z array for
 * n_timesteps: 	The number of elements in this array (i.e. the total
 * 					number of timesteps in the simulation)
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * header: element.h
 */
extern unsigned short malloc_Z(ELEMENT *e, unsigned long n_timesteps) {

	e -> Z = (double *) malloc (n_timesteps * sizeof(double));
	if ((*e).Z == NULL) {
		return 1;
	} else {
		unsigned long i;
		for (i = 0l; i < n_timesteps; i++) {
			e -> Z[i] = 0;
		}
		return 0;
	}

}


/*
 * Updates the mass of a single element at the current timestep.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object currently being simulated
 * e: 		A pointer to the element to update
 *
 * header: element.h
 */
extern void update_element_mass(SINGLEZONE sz, ELEMENT *e) {

	/*
	 * Change Note: version 1.3.1
	 *
	 * Rather than updating the element mass directly, one single value for
	 * the change is computed, and the total mass incremented at the end.
	 * This ensures that changes to the mass do not impact subsequent updates.
	 * Additionally, the increase in mass due to a species being present in
	 * primordial gas has moved to this function from the update_gas_evolution
	 * function in ism.c. This allows the element's mass to updated in one
	 * call, rather than in multiple places.
	 *
	 * See also changes notes in ism.c, singlezone.c.
	 */

	/*
	 * Pull the amount of mass produced by each enrichment channel, then add
	 * the retained part to the ISM mass and the unretained part to the
	 * instantaneous mass outflow.
	 */

	double dm = 0;
	double m_cc = mdot_ccsne(sz, *e) * sz.dt;
	double m_ia = mdot_sneia(sz, *e) * sz.dt;
	double m_agb = m_AGB(sz, *e);

	/* enrichment immediately lost to outflows */
	e -> unretained = 0;
	e -> unretained += (1 - (*(*e).ccsne_yields).entrainment) * m_cc;
	e -> unretained += (1 - (*(*e).sneia_yields).entrainment) * m_ia;
	e -> unretained += (1 - (*(*e).agb_grid).entrainment) * m_agb;

	/* enrichment entrained within the ISM */
	dm += (*(*e).ccsne_yields).entrainment * m_cc;
	dm += (*(*e).sneia_yields).entrainment * m_ia;
	dm += (*(*e).agb_grid).entrainment * m_agb;
	
	/*
	 * Subsequent terms in the enrichment equation - star formation and
	 * outflows proceed at the abundance by mass in the ISM Z.
	 */
	double Z = (*e).mass / (*sz.ism).mass;
	dm += mass_recycled(sz, e);
	dm -= (*sz.ism).star_formation_rate * sz.dt * Z;
	// if (strcmp((*e).symbol, "he")) {
	if (strcmp((*e).symbol, "he") && strcmp((*e).symbol, "au")) {
		dm -= (*sz.ism).enh[sz.timestep] * get_outflow_rate(sz) * sz.dt * Z;
	} else {
		/* Don't eject helium at an enhanced metallicity */
		dm -= get_outflow_rate(sz) * sz.dt * Z;
	}
	if ((*sz.ism).infall_rate > 0) {
		/*
		 * Seemingly unnecessary, this if statement is a safeguard against
		 * cases where the infall rate has been temporarily set to NaN, as in
		 * the first timestep in gas or star formation modes where the infall
		 * rate is not yet known. This is however taken into account by
		 * updating the gas supply before the elements when NOT running in
		 * infall mode, and vice versa when in infall mode.
		 */
 		double Zin = (*e).Zin[sz.timestep] + (*e).primordial;
	 	dm += (*sz.ism).infall_rate * sz.dt * Zin;
	} else {}

	e -> mass += dm;
	update_element_mass_sanitycheck(e);

}


/*
 * Performs a sanity check on a given element immediately after it's mass
 * was updated for the next timestep.
 *
 * Parameters
 * ==========
 * e: 		A pointer to the element to sanity check
 *
 * header: element.h
 */
extern void update_element_mass_sanitycheck(ELEMENT *e) {

	/*
	 * Allowing a zero element mass does not produce numerical artifacts in
	 * the ISM evolution -> just -infs in the associated [X/H] values.
	 * Moreover, 10^-12 Msun may be quite a bit of mass for some particularly
	 * heavy elements. Thus a lower bound of a true zero is implemented here.
	 */
	if ((*e).mass < 0) e -> mass = 0;

}


/*
 * Determine the [X/H] value for a given element in a zone.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object to pull the ISM mass from
 * e: 		The element to find the [X/H] value for
 *
 * Returns
 * =======
 * [X/H] = log10( mass(element) / mass(ISM) / solar )
 *
 * header: element.h
 */
extern double onH(SINGLEZONE sz, ELEMENT e) {

	/*
	 * Take into account the intrinsic mathematical domain of the log function
	 * to prevent floating point errors
	 */
	if ((*sz.ism).mass) {
		return log10( (e.mass / (*sz.ism).mass) / e.solar );
	} else {
		/*
		 * Take into account definition of INFINITY and NAN for generating the
		 * manylinux1 distributions.
		 */
		#ifdef INFINITY
			return INFINITY;
		#else
			#ifdef NAN
				return NAN;
			#else
				return -100;
			#endif
		#endif
	}

}

