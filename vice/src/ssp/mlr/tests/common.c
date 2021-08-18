/* 
 * This file implements routines for testing mass-lifetime relationships that 
 * are universal to all forms. 
 */ 

#include <stdlib.h> 
#include "../../mlr.h" 
#include "common.h" 

/* The number of times to test the functions at */ 
unsigned short TEST_N_TIMES = 1001u; 

/* The number of masses to test the functions at */ 
unsigned short TEST_N_MASSES = 10000u; 

/* The values of postMS to test the functions at */ 
double POSTMS_TEST_VALUES[16] = {
	0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 
	0.10, 0.11, 0.12, 0.13, 0.14, 0.15 
}; 

/* The values of Z to test the functions at */ 
double Z_TEST_VALUES[21] = {
	0.0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 
	0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.02 
}; 

/* Most studies suggest the minimum lifetime of a star is 3 Myr */ 
static double MINIMUM_LIFETIME = 0.003; 


/* 
 * Test a lifetime function at 16 values of post main sequence lifetimes and 
 * 21 values of metallicity Z to ensure that lifetimes are always larger than 
 * a minimum of 3 Myr. 
 * 
 * Parameters 
 * ==========
 * lifetime: 		The lifetime function to test 
 * 
 * Returns 
 * =======
 * 1 on success at all values of postMS and Z, 0 if a single error occurs 
 * 
 * header: common.h 
 */ 
extern unsigned short baseline_minimum_lifetime_test(
	double (*lifetime)(double, double, double)) {

	unsigned short i, j, result = 1u; 
	for (i = 0u; i < 16u; i++) {
		for (j = 0u; j < 21u; j++) {
			result &= test_minimum_lifetime(lifetime, 
				POSTMS_TEST_VALUES[i], Z_TEST_VALUES[j]); 
			if (!result) break; 
		} 
		if (!result) break; 
	} 
	return result; 

}


/* 
 * Test a turnoff mass function for monotonicity at 16 values of post main 
 * sequence lifetimes postMS and 21 values of metallicity Z. 
 * 
 * Parameters 
 * ==========
 * turnoffmass: 		The turnoff mass function to test 
 * 
 * Returns 
 * =======
 * 1 on success at all values of postMS and Z, 0 if a single failure occurs 
 * 
 * header: common.h 
 */ 
extern unsigned short baseline_monotonicity_test_turnoffmass(
	double (*turnoffmass)(double, double, double)) {

	unsigned short i, j, result = 1u; 
	for (i = 0u; i < 16u; i++) {
		for (j = 0u; j < 21u; j++) {
			result &= test_turnoffmass_monotonicity(turnoffmass, 
				POSTMS_TEST_VALUES[i], Z_TEST_VALUES[j]); 
			if (!result) break; 
		} 
		if (!result) break; 
	} 
	return result; 

}


/* 
 * Test a lifetime function for monotonicity at 16 values of post main 
 * sequence lifetimes postMS and 21 values of metallicity z. 
 * 
 * Parameters 
 * ==========
 * lifetime: 		The lifetime function to test 
 * 
 * Returns 
 * =======
 * 1 on success at all values of postMS and Z, 0 if a single failure occurs 
 * 
 * header: common.h 
 */ 
extern unsigned short baseline_monotonicity_test_lifetime(
	double (*lifetime)(double, double, double)) {

	unsigned short i, j, result = 1u; 
	for (i = 0u; i < 16u; i++) {
		for (j = 0u; j < 21u; j++) {
			result &= test_lifetime_monotonicity(lifetime, 
				POSTMS_TEST_VALUES[i], Z_TEST_VALUES[j]); 
			if (!result) break; 
		} 
		if (!result) break; 
	} 
	return result; 

}


/* 
 * Test a lifetime function by asserting that it should predict lifetimes 
 * larger than 3 Myr, the canonically accepted minimum lifetime of a star. 
 * 
 * Parameters 
 * ==========
 * lifetime: 		The lifetime function to test the minimum value for 
 * postMS: 			The value of the parameter postMS to test at. 
 * 					See documentation of lifetime functions for details. 
 * Z: 				The metallicity by mass to test at. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: common.h 
 */ 
extern unsigned short test_minimum_lifetime( 
	double (*lifetime)(double, double, double), double postMS, double Z) {

	unsigned short i, result = 1u; 
	double *masses = get_test_masses(); 
	for (i = 0u; i < TEST_N_MASSES; i++) {
		result &= lifetime(masses[i], postMS, Z) > MINIMUM_LIFETIME; 
		if (!result) break; 
	}
	free(masses); 
	return result; 

}


/* 
 * Test a turnoff mass function by asserting that it should predict masses 
 * which decrease monotonically with increasing age. 
 * 
 * Parameters 
 * ==========
 * turnoffmass: 	The turnoffmass function to test. 
 * postMS: 			The value of the parameter postMS to test monotonicity at. 
 * 					See documentation of turnoffmass functions for details. 
 * Z: 				The metallicity to test for monotonicity at. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: common.h 
 */ 
extern unsigned short test_turnoffmass_monotonicity(
	double (*turnoffmass)(double, double, double), double postMS, double Z) {

	unsigned short i, result = 1u; 
	double *lifetimes = get_test_times(); 
	double *masses = (double *) malloc (TEST_N_TIMES * sizeof(double)); 
	for (i = 0u; i < TEST_N_TIMES; i++) {
		masses[i] = turnoffmass(masses[i], postMS, Z); 
		/* 
		 * The turnoff mass at a given time should be marginally smaller than 
		 * the turnoff mass at a slightly younger age. 
		 */ 
		if (i) result &= masses[i] < masses[i - 1u]; 
		if (!result) break; 
	} 
	free(lifetimes); 
	free(masses); 
	return result; 

}


/* 
 * Test a lifetime function by asserting that it should predict lifetimes 
 * which decrease monotonically with increasing stellar mass. 
 * 
 * Parameters 
 * ==========
 * lifetime: 		The lifetime function to test. 
 * postMS: 			The value of the parameter postMS to test monotonicity at. 
 * 					See documentation of lifetime functions for details. 
 * Z: 				The metallicity to test for monotonicity at. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: common.h 
 */ 
extern unsigned short test_lifetime_monotonicity(
	double (*lifetime)(double, double, double), double postMS, double Z) {

	unsigned short i, result = 1u; 
	double *masses = get_test_masses(); 
	double *lifetimes = (double *) malloc (TEST_N_MASSES * sizeof(double)); 
	for (i = 0u; i < TEST_N_MASSES; i++) {
		lifetimes[i] = lifetime(masses[i], postMS, Z); 
		/* 
		 * The lifetime of a star of a given mass should be marginally larger 
		 * than a marginally more massive star. Base the comparison of the >= 
		 * sign rather than the > sign because the Padovani & Matteucci (1993) 
		 * form flattens off at low masses. 
		 */ 
		if (i) result &= lifetimes[i] >= lifetimes[i - 1u]; 
		if (!result) break; 
	} 
	free(masses); 
	free(lifetimes); 
	return result; 

}


/* 
 * Get an array of test masses to send to the various mass-lifetime functions. 
 * 
 * Returns 
 * =======
 * 0.01 to 100 in steps of 0.01, inclusive. 
 * 
 * header: common.h 
 */ 
extern double *get_test_masses(void) {

	unsigned short i; 
	double *masses = (double *) malloc (TEST_N_MASSES * sizeof(double)); 
	for (i = 1u; i <= TEST_N_MASSES; i++) {
		masses[i - 1u] = 0.01 * i; 
	} 
	return masses; 

}


/* 
 * Get an array of test times to send to the various mass-lifetime functions. 
 * 
 * Returns 
 * =======
 * 0 to 10 in timesteps of 0.01, inclusive. 
 * 
 * header: common.h 
 */ 
extern double *get_test_times(void) {

	unsigned short i; 
	double *times = (double *) malloc (TEST_N_TIMES * sizeof(double)); 
	for (i = 0u; i < TEST_N_TIMES; i++) {
		times[i] = 0.01 * i; 
	} 
	return times; 

}

