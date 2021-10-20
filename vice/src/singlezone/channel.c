/*
 * This file implements enrichment from an arbitrary, custom enrichment
 * channel parameterized by the user in VICE singlezone simulations.
 */

#include <stdlib.h>
#include "../singlezone.h"
#include "../callback.h"
#include "../channel.h"
#include "../utils.h"
#include "channel.h"


/*
 * Determine the rate of mass enrichment of a given element at the current
 * timestep from all arbitrary enrichment channels.
 *
 * Parameters
 * ==========
 * sz: 		The SINGLEZONE object for the current simulation
 * e: 		The element to find the rate of mass enrichment for
 *
 * Returns
 * =======
 * The time-derivative of the arbitrary enrichment channels mass enrichment
 * term
 *
 * header: channel.h
 */
extern double mdot(SINGLEZONE sz, ELEMENT e) {

	unsigned short i;
	double mdot_ = 0;
	for (i = 0lu; i < e.n_channels; i++) {
		unsigned long j;
		for (j = 0l; j < sz.timestep; j++) {
			/* Entrainment to be handled in vice/src/singlezone/element.c */
			mdot_ += (get_yield((*e.channels[i]), scale_metallicity(sz, j)) *
				(*sz.ism).star_formation_history[j] *
				(*e.channels[i]).rate[sz.timestep - j]
			);
		}
	}
	return mdot_;

}


/*
 * Obtain the IMF-integrated fractional mass yield of a given element from
 * its internal yield table.
 *
 * Parameters
 * ==========
 * e: 		The element to find the yield for
 * Z: 		The metallicity to look up on the grid
 *
 * Returns
 * =======
 * The interpolated yield off of the stored yield grid within the CHANNEL
 * struct.
 *
 * header: channel.h
 */
extern double get_yield(CHANNEL ch, double Z) {

	return callback_1arg_evaluate(*ch.yield_, Z);

}


/*
 * Normalize the rate once it is set according to an arbitrary normalization
 * by the user in python.
 *
 * Parameters
 * ==========
 * e: 			The ELEMENT struct to normalize the rate for.
 * length: 		The length of the e -> channels[i] -> rate array
 *
 * header: channel.h
 */
extern void normalize_rates(ELEMENT *e, unsigned long length) {

	unsigned short i;
	for (i = 0u; i < (*e).n_channels; i++) {
		unsigned long j;
		double sum = 0;
		for (j = 0lu; j < length; j++) {
			sum += (*(*e).channels[i]).rate[j];
		}
		for (j = 0lu; j < length; j++) {
			e -> channels[i] -> rate[j] /= sum;
		}
	}

}

