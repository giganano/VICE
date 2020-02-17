/* 
 * This file tests the mass-lifetime relationship functions implemented at 
 * vice/src/ssp/mlr.h 
 */ 

#include <stdlib.h> 
#include "../../ssp.h" 
#include "mlr.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static unsigned short test_main_sequence_turnoff_mass_engine(double postMS); 
static double *get_test_times(void); 

/* The number of times to test the function at */ 
static unsigned short TEST_N_TIMES = 1001u; 


/* 
 * Tests the main sequence turnoff mass function at vice/src/ssp/mlr.h 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: mlr.h 
 */ 
extern unsigned short test_main_sequence_turnoff_mass(void) { 

	unsigned short i; 
	double postMS_test_values[11]; 
	for (i = 0u; i < 11u; i++) {
		postMS_test_values[i] = 0.01 * i; 
	} 
	for (i = 0u; i < 11u; i++) {
		if (!test_main_sequence_turnoff_mass_engine(postMS_test_values[i]) || 
			main_sequence_turnoff_mass(
				(1 + postMS_test_values[i]) * SOLAR_LIFETIME, 
				postMS_test_values[i] 
			) != 1) { 
			return 0u; 
		} else {} 
	} 
	return 1u; 

} 


/* 
 * Test the main sequence turnoff mass function for a given post main sequence 
 * lifetime 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 */ 
static unsigned short test_main_sequence_turnoff_mass_engine(double postMS) {

	unsigned short i; 	
	double *times = get_test_times(); 
	for (i = 1u; i < TEST_N_TIMES; i++) {
		if (main_sequence_turnoff_mass(times[i], postMS) > 
			main_sequence_turnoff_mass(times[i - 1u], postMS)) {
			return 0u; 
		} else {} 
	} 
	return 1u; 

}


/* 
 * Get an array of test times to send to the main sequence turnoff mass 
 * function 
 * 
 * Returns 
 * ======= 
 * 0 to 10 in steps of 0.01, inclusive 
 */ 
static double *get_test_times(void) {

	unsigned short i; 
	double *times = (double *) malloc (TEST_N_TIMES * sizeof(double)); 
	for (i = 0u; i < TEST_N_TIMES; i++) {
		times[i] = 0.01 * i; 
	} 
	return times; 

}

