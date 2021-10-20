/*
 * This file implements tests of the initial-remnant mass relation at
 * vice/src/ssp/remnants.h
 */

#include "../../ssp.h"
#include "remnants.h"


/*
 * Test the implementation of the Kalirai et al. (2008) initial-final
 * remnant mass relationship at vice/src/ssp/remnants.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: remnants.h
 */
extern unsigned short test_Kalirai08_remnant_mass(void) {

	unsigned short i;
	for (i = 1u; i < 100u; i++) {
		if (i < 8 && Kalirai08_remnant_mass(i) != 0.394 + 0.109 * i) {
			return 0u;
		} else if (i >= 8 && Kalirai08_remnant_mass(i) != 1.44) {
			return 0u;
		} else {
			continue;
		}
	}
	return 1u;

}

