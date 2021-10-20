/*
 * This file implements testing of the main sequence mass fraction functions
 * at vice/src/ssp/msmf.h
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../ssp.h"
#include "../../objects/tests.h"
#include "msmf.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short test_MSMF_common(char imf[]);
static unsigned short test_MSMF_engine(SSP test, double *times);
static double *get_test_times(void);
static double test_imf(double mass, void *dummy);

/* The number of times to call MSMF for a given IMF */
static unsigned short TEST_N_TIMES = 1001u;


/*
 * Test the MSMF function at vice/src/ssp/msmf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: msmf.h
 */
extern unsigned short test_MSMF(void) {

	return (
		test_MSMF_common("kroupa") &&
		test_MSMF_common("salpeter") &&
		test_MSMF_common("custom")
	);

}


/*
 * Test the setup_MSMF function at vice/src/ssp/msmf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: msmf.h
 */
extern unsigned short test_setup_MSMF(void) {

	SINGLEZONE *test = singlezone_test_instance();
	if (setup_MSMF(test)) {
		singlezone_free(test);
		return 0u;
	} else {
		unsigned short i, result = 1u;
		for (i = 1u; i < (*test).n_outputs; i++) {
			if ((*(*test).ssp).msmf[i] <= 0 ||
				(*(*test).ssp).msmf[i] >= 1 ||
				(*(*test).ssp).msmf[i] > (*(*test).ssp).msmf[i - 1]) {
				result = 0u;
				break;
			} else {}
		}
		singlezone_free(test);
		return result;
	}

}


/*
 * Tests the MSMF function for a given IMF
 *
 * Parameters
 * ==========
 * imf: 		"kroupa", "salpeter", or "custom" denoting which IMF to use
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short test_MSMF_common(char imf[]) {

	SSP *test = ssp_initialize();
	strcpy(test -> imf -> spec, imf);
	if (!strcmp(imf, "custom")) {
		/* use the test case vice/tests/src/imf.h */
		// set_test_custom_mass_distribution(test -> imf);
		test -> imf -> custom_imf -> callback = &test_imf;
		test -> imf -> custom_imf -> user_func = test;
	} else {}
	double *times = get_test_times();
	unsigned short result = test_MSMF_engine(*test, times);
	free(times);
	ssp_free(test);
	return result;

}


/*
 * Test the MSMF function for a given IMF. In VICE's current iteration, this
 * is called once for each built-in and one custom IMF.
 *
 * Parameters
 * ==========
 * test: 		The SSP object to send to the MSMF function
 * times: 		Times at which to evaluate the MSMF function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short test_MSMF_engine(SSP test, double *times) {

	unsigned short i;
	for (i = 1u; i < TEST_N_TIMES; i++) {
		if (MSMF(test, times[i]) > MSMF(test, times[i - 1u])) return 0u;
	}
	return 1u;

}


/*
 * Get dummy times to evaluate MSMF at
 *
 * Returns
 * =======
 * 0 to 10 in steps of .01, inclusive
 */
static double *get_test_times(void) {

	unsigned short i;
	double *times = (double *) malloc (TEST_N_TIMES * sizeof(double));
	for (i = 0u; i < TEST_N_TIMES; i++) {
		times[i] = 0.01 * i;
	}
	return times;

}


/*
 * A test IMF to point a custom IMF callback object to
 */
static double test_imf(double mass, void *dummy) {

	return pow(mass, -2);

}

