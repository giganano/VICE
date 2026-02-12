/*
 * This file is part of the VICE package.
 * Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
 * License: MIT License. See LICENSE in top-level directory
 * at: https://github.com/giganano/VICE.git.
 *
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
 * Notes
 * =====
 * This function also adds the unretained mass from each additional enrichment
 * channel to the outflow, following the built-in AGB star, CCSN, and SN Ia
 * enrichment channels.
 *
 * header: channel.h
 */
extern double mdot_channels(SINGLEZONE sz, ELEMENT *e) {

	double mdot = 0;
	for (unsigned short i = 0u; i < (*e).n_channels; i++) {
		for (unsigned long j = 0ul; j < sz.timestep; j++) {
			double production_rate = (
				get_channel_yield((*(*e).channels[i]), scale_metallicity(sz, j)) *
				(*sz.ism).star_formation_history[j] *
				(*(*e).channels[i]).rate[sz.timestep - j]
			);
			mdot += production_rate * (*(*e).channels[i]).entrainment;
			e -> unretained += production_rate * sz.dt * (
				1 - (*(*e).channels[i]).entrainment);
		}
	}
	return mdot;

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
extern double get_channel_yield(CHANNEL ch, double Z) {

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
extern void normalize_channel_rates(CHANNEL *ch, unsigned long length) {

	double sum = 0;
	for (unsigned long i = 0ul; i < length; i++) sum += (*ch).rate[i];
	for (unsigned long i = 0ul; i < length; i++) ch -> rate[i] /= sum;

}

