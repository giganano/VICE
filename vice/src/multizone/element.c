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

	/*
	 * Change Note: version 1.3.1
	 *
	 * See corresponding change note in src/singlezone/element.c as the same
	 * changes have been incorporated here.
	 */

	unsigned int i, j;
	for (i = 0u; i < (*(*mz).zones[0]).n_elements; i++) {

		/*
		 * These enrichment channels which require tracer particles are written
		 * such that they can be called once for each element and updated
		 * in one foul swoop across all zones:
		 *
		 * Enrichment from SNe Ia
		 * Enrichment from AGB stars
		 * Re-enrichment from recycled stellar envelopes
		 */
		double *sneia = m_sneia_from_tracers(*mz, i);
		double *agb = m_AGB_from_tracers(*mz, i);
		double *recycled = recycled_mass(*mz, i);

		for (j = 0u; j < (*(*mz).mig).n_zones; j++) {

			/*
			 * These instantaneous pieces don't require tracer particles and
			 * can be taken straight from the birth zone:
			 *
			 * Enrichment from core collapse supernovae
			 * Depletion from star formation
			 * Depletion from outflows
			 * Metal-rich infall (or anything present in primordial gas)
			 */

			SINGLEZONE sz = *(*mz).zones[j];
			ELEMENT *e = mz -> zones[j] -> elements[i];

			double dm = 0;
			double m_cc = mdot_ccsne(sz, *e) * sz.dt;
			double m_ia = sneia[j];
			double m_agb = agb[j];

			/* 
			 * Enrichment immediately lost to outflows. For the enrichment
			 * channels requiring tracer particles, this uses the entrainment
			 * fraction from the CURRENT zone as opposed to the BIRTH zone,
			 * a choice which is likely more physical since whether or not, e.g.
			 * a fluid element from a SN Ia or an AGB star is included in an
			 * outflow likely has more to do with its current location than
			 * where it was born.
			 */
			e -> unretained = 0;
			e -> unretained += (1 - (*(*e).ccsne_yields).entrainment) * m_cc;
			e -> unretained += (1 - (*(*e).sneia_yields).entrainment) * m_ia;
			e -> unretained += (1 - (*(*e).agb_grid).entrainment) * m_agb;

			/* Enrichment entrained within the ISM */
			dm += (*(*e).ccsne_yields).entrainment * m_cc;
			dm += (*(*e).sneia_yields).entrainment * m_ia;
			dm += (*(*e).agb_grid).entrainment * m_agb;

			/*
			 * Subsequent terms in the enrichmen tequation - star formation and
			 * outflows proceed at the abundance by mass Z in the current zone.
			 */
			double Z = (*e).mass / (*sz.ism).mass;
			dm += recycled[j];
			dm -= (*sz.ism).star_formation_rate * sz.dt * Z;
			// if (strcmp((*e).symbol, "he")) {
			if (strcmp((*e).symbol, "he") && strcmp((*e).symbol, "au")) {
				dm -= (
					(*sz.ism).enh[sz.timestep] * get_outflow_rate(sz) *
					sz.dt * Z
				);
			} else {
				/* Don't eject helium at an enhanced abundance */
				dm -= get_outflow_rate(sz) * sz.dt * Z;
			}

			if ((*sz.ism).infall_rate > 0) {
				/*
				 * Safeguard against the infall rate being set to NaN, see
				 * comment on same if-statement in src/singlezone/element.c.
				 */
				double Zin = (*e).Zin[sz.timestep] + (*e).primordial;
				dm += (*sz.ism).infall_rate * (sz).dt * Zin;
			} else {}

			e -> mass += dm;
			update_element_mass_sanitycheck(e);

		}

		free(sneia);
		free(agb);
		free(recycled);

	}

}

