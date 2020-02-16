/* 
 * This file implements testing of the cumulative return fraction 
 * calculations at vice/src/ssp/crf.h 
 */ 


#include <stdlib.h> 
#include <string.h> 
#include "../../ssp.h" 
#include "../imf.h" 
#include "crf.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static unsigned short test_CRF_common(char imf[]); 
static unsigned short test_CRF_engine(SSP ssp, double *times); 
static double *get_test_times(void); 

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
		set_test_custom_mass_distribution(test -> imf); 
	} else {} 
	double *times = get_test_times(); 
	unsigned short result = test_CRF_engine(*test, times); 
	free(times); 
	return result; 

} 


/* 
 * Test the CRF function for a given IMF. In VICE's current iteration, this 
 * is called once for each built-in and one custom IMF. 
 * 
 * Parameters 
 * ========== 
 * ssp: 		The SSP object to send to the CRF function 
 * times: 		Times at which to evaluate the CRF function 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 */ 
static unsigned short test_CRF_engine(SSP ssp, double *times) { 

	unsigned long i; 
	for (i = 1ul; i < TEST_N_TIMES; i++) { 
		if (CRF(ssp, times[i]) < CRF(ssp, times[i - 1ul])) return 0u; 
	} 
	return 1u; 

} 


/* 
 * Get dummy times to evaluate the CRF function at 
 * 
 * Returns 
 * ======= 
 * 0 to 10 in steps of 0.01 
 */ 
static double *get_test_times(void) {

	unsigned short i, TEST_N_TIMES = 1001u; 
	double *times = (double *) malloc (TEST_N_TIMES * sizeof(double)); 
	for (i = 0u; i < TEST_N_TIMES; i++) {
		times[i] = 0.01 * i; 
	} 
	return times; 

}

