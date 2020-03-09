/* 
 * This file implements testing of the main sequence mass fraction functions 
 * at vice/src/ssp/msmf.h 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include "../../ssp.h" 
#include "../imf.h" 
#include "msmf.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static unsigned short test_MSMF_common(char imf[]); 
static unsigned short test_MSMF_engine(SSP test, double *times); 
static double *get_test_times(void); 

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
		test_MSMF_common("salpeter") 
		// test_MSMF_common("custom") 
	); 

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
		set_test_custom_mass_distribution(test -> imf); 
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

