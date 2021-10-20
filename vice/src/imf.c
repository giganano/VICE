/*
 * This file implements stellar initial mass functions (IMFs).
 */

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "callback.h"
#include "imf.h"
#include "utils.h"


/*
 * Evaluate the IMF at the stellar mass m in Msun
 *
 * Parameters
 * ==========
 * imf: 		The IMF object
 * m: 			The stellar mass to evaluate the IMF at
 *
 * Returns
 * =======
 * The un-normalized value of the IMF at the stellar mass m
 *
 * header: imf.h
 */
extern double imf_evaluate(IMF_ imf, double m) {

	/* If the mass in the specified mass range */
	if (imf.m_lower <= m && m <= imf.m_upper) {

		switch(checksum(imf.spec)) {

			case SALPETER:
				return salpeter55(m);

			case KROUPA:
				return kroupa01(m);

			case CUSTOM:
				return callback_1arg_evaluate(*imf.custom_imf, m);

			default: 	/* error handling */
				return -1;

		}

	} else {
		/* not in the specified mass range for star formation */
		return 0;
	}

}


/*
 * The Salpeter (1955) stellar initial mass function (IMF) up to a
 * normalization constant.
 *
 * Parameters
 * ==========
 * m: 			The stellar mass in Msun
 *
 * Returns
 * =======
 * The value of the IMF at that mass up to the normalization of the IMF.
 * -1 if m < 0.
 *
 * References
 * ==========
 * Salpeter (1955), ApJ, 121, 161
 *
 * header: imf.h
 */
extern double salpeter55(double m) {

	if (m > 0) {
		return pow(m, -2.35);
	} else {
		return -1;
	}

}


/*
 * The Kroupa (2001) stellar initial mass function (IMF) up to a
 * normalization constant.
 *
 * Parameters
 * ==========
 * m: 			The stellar mass in Msun
 *
 * Returns
 * =======
 * The value of the IMF at that mass up to the normalization of the IMF.
 * -1 if m < 0.
 *
 * References
 * ==========
 * Kroupa (2001), MNRAS, 322, 231
 *
 * header: imf.h
 */
extern double kroupa01(double m) {

	if (0 < m && m < 0.08) {
		return pow(m, -0.3);
	} else if (0.08 <= m && m <= 0.5) {
		/*
		 * Need to make sure kroupa01(0.08) = kroupa01(0.0799999999...)
		 *
		 * Xm^-1.3 = m^-0.3 at m = 0.08 => X = 0.08
		 */
		return 0.08 * pow(m, -1.3);
	} else if (m > 0.5) {
		/*
		 * Need to make sure kroupa01(0.5) = kroupa01(0.49999999....)
		 *
		 * Ym^-2.3 = Xm^-1.3 at m = 0.05 => Y = 0.08(0.5) = 0.04
		 */
		return 0.04 * pow(m, -2.3);
	} else {
		/* m < 0, return -1 for ValueError */
		return -1;
	}

}

