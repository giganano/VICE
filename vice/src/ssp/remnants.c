/*
 * This file implements initial-remnant mass relations in VICE.
 */

#include "../ssp.h"
#include "remnants.h"


/*
 * The Kalirai et al. (2008) initial-final remnant mass relationship
 *
 * Parameters
 * ==========
 * m: 		The initial stellar mass in Msun
 *
 * Returns
 * =======
 * The mass of the remnant under the Kalirai et al. (2008) model. Stars with
 * main sequence masses >= 8 Msun leave behind a 1.44 Msun remnant. Those < 8
 * Msun leave behind a 0.394 + 0.109 * m Msun mass remnant.
 *
 * References
 * ==========
 * Kalirai et al. (2008), ApJ, 676, 594
 *
 * header: remnants.h
 */
extern double Kalirai08_remnant_mass(double m) {

	if (m >= 8) {
		return 1.44;
	} else if (0 < m && m < 8) {
		return 0.394 + 0.109 * m;
	} else {
		return 0;
	}

}

