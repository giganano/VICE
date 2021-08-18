
#ifndef SSP_MLR_TESTS_VINCENZO2016_H 
#define SSP_MLR_TESTS_VINCENZO2016_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

/* 
 * Test the Vincenzo et al. (2016) lifetime function at a range of values for 
 * post main sequence lifetimes and metallicities to ensure that the values 
 * are larger than the accepted minimum of 3 Myr. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: vincenzo2016.c 
 */ 
extern unsigned short test_vincenzo2016_minimum_lifetime(void); 

/* 
 * Test the Vincenzo et al. (2016) turnoff mass function for monotonicity at a 
 * range of values for post main sequence lifetimes and metallicities. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: vincenzo2016.c 
 */ 
extern unsigned short test_vincenzo2016_turnoffmass_monotonicity(void); 

/* 
 * Test the Vincenzo et al. (2016) lifetime function for monotonicity at a 
 * range of values for post main sequence lifetimes and metallicities. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: vincenzo2016.c 
 */ 
extern unsigned short test_vincenzo2016_lifetime_monotonicity(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_MLR_TESTS_VINCENZO_H */ 
