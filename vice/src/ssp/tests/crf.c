/*
 * This file implements testing of the cumulative return fraction
 * calculations at vice/src/ssp/crf.h
 */


#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../../ssp.h"
#include "../../objects/tests.h"
#include "crf.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short test_CRF_common(char imf[]);
static unsigned short test_CRF_engine(SSP test, double *times);
static double *get_test_times(void);
static double test_imf(double mass, void *dummy);

/* The number of times to call CRF for a given IMF */
static unsigned short TEST_N_TIMES = 1001u;


/*
 * Test the CRF function at vice/src/ssp/crf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: crf.h
 */
extern unsigned short test_CRF(void) {

	return (
		test_CRF_common("salpeter") &&
		test_CRF_common("kroupa") &&
		test_CRF_common("custom")
	);

}


/*
 * Test the setup_CRF function at vice/src/ssp/crf.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: crf.h
 */
extern unsigned short test_setup_CRF(void) {

	SINGLEZONE *test = singlezone_test_instance();
	if (setup_CRF(test)) {
		singlezone_free(test);
		return 0u;
	} else {
		unsigned short i, result = 1u;
		for (i = 1u; i < (*test).n_outputs; i++) {
			if ((*(*test).ssp).crf[i] <= 0 ||
				(*(*test).ssp).crf[i] >= 1 ||
				(*(*test).ssp).crf[i] < (*(*test).ssp).crf[i - 1]) {
				result = 0u;
				break;
			} else {}
		}
		singlezone_free(test);
		return result;
	}

}


/*
 * Test the CRF function for a particular IMF
 *
 * Parameters
 * ==========
 * imf: 		"kroupa", "salpeter", or "custom" denoting which IMF to test
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short test_CRF_common(char imf[]) {

	SSP *test = ssp_initialize();
	strcpy(test -> imf -> spec, imf);
	if (!strcmp(imf, "custom")) {
		/* use the test case at vice/src/tests/imf.h */
		// set_test_custom_mass_distribution(test -> imf);
		test -> imf -> custom_imf -> callback = &test_imf;
		test -> imf -> custom_imf -> user_func = test;
	} else {}
	double *times = get_test_times();
	unsigned short result = test_CRF_engine(*test, times);
	free(times);
	ssp_free(test);
	return result;

}


/*
 * Test the CRF function for a given IMF. In VICE's current iteration, this
 * is called once for each built-in and one custom IMF.
 *
 * Parameters
 * ==========
 * test: 		The SSP object to send to the CRF function
 * times: 		Times at which to evaluate the CRF function
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short test_CRF_engine(SSP test, double *times) {

	unsigned short i;
	for (i = 1u; i < TEST_N_TIMES; i++) {
		if (CRF(test, times[i]) < CRF(test, times[i - 1ul])) return 0u;
	}
	return 1u;

}


/*
 * Get dummy times to evaluate the CRF function at
 *
 * Returns
 * =======
 * 0 to 10 in steps of 0.01, inclusive
 */
static double *get_test_times(void) {

	unsigned short i, TEST_N_TIMES = 1001u;
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

