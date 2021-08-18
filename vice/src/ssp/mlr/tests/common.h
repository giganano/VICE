
#ifndef SSP_MLR_TESTS_COMMON_H 
#define SSP_MLR_TESTS_COMMON_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

/* The number of times to test the function at */ 
extern unsigned short TEST_N_TIMES; 

/* The number of masses to test the functions at */ 
extern unsigned short TEST_N_MASSES; 

/* The values of postMS to test the functions at */ 
extern double POSTMS_TEST_VALUES[16]; 

/* The values of Z to test the functions at */ 
extern double Z_TEST_VALUES[21]; 

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
 * source: common.c 
 */ 
extern unsigned short baseline_minimum_lifetime_test(
	double (*lifetime)(double, double, double)); 

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
 * source: common.c 
 */ 
extern unsigned short baseline_monotonicity_test_turnoffmass(
	double (*turnoffmass)(double, double, double)); 

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
 * source: common.c 
 */ 
extern unsigned short baseline_monotonicity_test_lifetime(
	double (*lifetime)(double, double, double)); 

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
 * source: common.c 
 */ 
extern unsigned short test_minimum_lifetime( 
	double (*lifetime)(double, double, double), double postMS, double Z); 

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
 * source: common.c 
 */ 
extern unsigned short test_turnoffmass_monotonicity(
	double (*turnoffmass)(double, double, double), double postMS, double Z); 

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
 * source: common.c 
 */ 
extern unsigned short test_lifetime_monotonicity(
	double (*lifetime)(double, double, double), double postMS, double Z); 

/* 
 * Get an array of test masses to send to the various mass-lifetime functions. 
 * 
 * Returns 
 * =======
 * 0.01 to 100 in steps of 0.01, inclusive. 
 * 
 * source: common.c 
 */ 
extern double *get_test_masses(void); 

/* 
 * Get an array of test times to send to the various mass-lifetime functions. 
 * 
 * Returns 
 * =======
 * 0 to 10 in timesteps of 0.01, inclusive. 
 * 
 * source: common.c 
 */ 
extern double *get_test_times(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_MLR_TESTS_COMMON_H */ 
