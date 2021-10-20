/*
 * This file implements the functionality of the element object in multizone
 * simulations.
 */

#include <stdlib.h>
#include <string.h>
#include "../multizone.h"
#include "../singlezone.h"
#include "element.h"


/*
 * Updates the mass of each element in each zone to the proper value at the
 * next timestep.
 *
 * Parameters
 * ==========
 * mz: 		A pointer to the multizone object for the current simulation
 *
 * header: element.h
 */
extern void update_elements(MULTIZONE *mz) {

	unsigned int i, j;
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		SINGLEZONE *sz = mz -> zones[i];
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			ELEMENT *e = sz -> elements[j];
			/*
			 * Instantaneous pieces that don't require tracer particles:
			 *
			 * Enrichment from core collapse supernovae
			 * depletion from star formation
			 * depletion from outflows
			 * metal-rich infall
			 */

			e -> unretained = 0;
			double m_cc = mdot_ccsne(*sz, *e) * (*sz).dt;
			e -> mass += (*(*e).ccsne_yields).entrainment * m_cc;
			e -> unretained += (1 - (*(*e).ccsne_yields).entrainment) * m_cc;

			e -> mass -= (
				(*(*sz).ism).star_formation_rate * (*sz).dt *
				(*e).mass / (*(*sz).ism).mass
			);
			if (strcmp((*e).symbol, "he")) {
				e -> mass -= (
					(*(*sz).ism).enh[(*sz).timestep] * get_outflow_rate(*sz) *
					(*sz).dt * (*e).mass / (*(*sz).ism).mass
				);
			} else {
				e -> mass -= (
					get_outflow_rate(*sz) * (*sz).dt * (*e).mass /
					(*(*sz).ism).mass
				);
			}
			e -> mass += (
				(*(*sz).ism).infall_rate * (*sz).dt * (*e).Zin[(*sz).timestep]
			);

		}
	}

	/*
	 * Non-instantaneous pieces that do require tracer particles:
	 *
	 * Enrichment from AGB stars
	 * Enrichment from SNe Ia
	 * Re-enrichment from recycling
	 */
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {

		/* AGB stars taking into account entrainment in the current zone */
		double *agb = m_AGB_from_tracers(*mz, i);
		for (j = 0u; j < (*(*mz).mig).n_zones; j++) {
			ELEMENT *e = mz -> zones[j] -> elements[i];
			e -> mass += (*(*e).agb_grid).entrainment * agb[j];
			e -> unretained += (1 - (*(*e).agb_grid).entrainment) * agb[j];
		}
		free(agb);

		/* SNe Ia taking into account entrainment in the current zone. */
		double *sneia = m_sneia_from_tracers(*mz, i);
		for (j = 0u; j < (*(*mz).mig).n_zones; j++) {
			ELEMENT *e = mz -> zones[j] -> elements[i];
			e -> mass += (*(*e).sneia_yields).entrainment * sneia[j];
			e -> unretained += (1 -
				(*(*e).sneia_yields).entrainment) * sneia[j];
		}
		free(sneia);

		recycle_metals_from_tracers(mz, i);

	}

	/* sanity check each element in each zone */
	for (i = 0u; i < (*(*mz).mig).n_zones; i++) {
		for (j = 0u; j < (*(*mz).zones[i]).n_elements; j++) {
			update_element_mass_sanitycheck(mz -> zones[i] -> elements[j]);
		}
	}

}

