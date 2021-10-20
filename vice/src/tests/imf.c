/*
 * This file implements tests of the core routines of the IMF object.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../imf.h"
#include "../utils.h"
#include "../callback.h"
#include "imf.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double test_imf(double m, void *dummy);
static IMF_ *get_test_imf(void);

/*
 * TEST_IMF_MAX_MASS:	The maximum stellar mass of the test case IMF
 * TEST_IMF_MIN_MASS: 	The minimum stellar mass of the test case IMF
 */
static double TEST_IMF_MAX_MASS = 100;
static double TEST_IMF_MIN_MASS = 0.08;


/*
 * Test the function which evaluates an IMF object at a given mass
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: imf.h
 */
extern unsigned short test_imf_evaluate(void) {

	IMF_ *test = get_test_imf();
	strcpy(test -> spec, "kroupa");
	if (imf_evaluate(*test, 1) != kroupa01(1)) {
		imf_free(test);
		return 0u;
	} else {}
	strcpy(test -> spec, "salpeter");
	if (imf_evaluate(*test, 1) != salpeter55(1)) {
		imf_free(test);
		return 0u;
	} else {}
	strcpy(test -> spec, "custom");
	test -> custom_imf = callback_1arg_initialize();
	if ((*test).custom_imf == NULL) {
		imf_free(test);
		return 0u;
	} else {
		test -> custom_imf -> callback = &test_imf;
		test -> custom_imf -> user_func = &test_imf;
		test -> custom_imf -> assumed_constant = -1;
		unsigned short result = imf_evaluate(*test, 1) == test_imf(1, NULL);
		imf_free(test);
		return result;
	}

}


/*
 * Test the built-in Salpeter (1955) IMF
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * References
 * ==========
 * Salpeter (1955), ApJ, 121, 161
 *
 * header: imf.h
 */
extern unsigned short test_salpeter55(void) {

	return (
		salpeter55(1) == 1 &&
		salpeter55(2) == pow(2, -2.35) &&
		salpeter55(-1) == -1
	);

}


/*
 * Test the built-in Kroupa (2001) IMF
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * References
 * ==========
 * Kroupa (2001), MNRAS, 322, 231
 *
 * header: imf.h
 */
extern unsigned short test_kroupa01(void) {

	return (
		/* normalization factors appear due to piece-wise nature */
		kroupa01(0.05) == pow(0.05, -0.3) &&
		kroupa01(0.1) == 0.08 * pow(0.1, -1.3) &&
		kroupa01(1) == 0.04
	);

}


/*
 * A test custom IMF with slope -2
 *
 * Parameters
 * ==========
 * m: 		Stellar mass in Msun
 * dummy: 	A dummy void pointer to allow testing with a callback object.
 */
static double test_imf(double m, void *dummy) {

	/* A top-heavy power-law IMF */
	return pow(m, -2);

}


/*
 * Get the test IMF object
 */
static IMF_ *get_test_imf(void) {

	return imf_initialize(TEST_IMF_MIN_MASS, TEST_IMF_MAX_MASS);

}

