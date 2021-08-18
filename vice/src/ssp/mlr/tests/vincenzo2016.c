/* 
 * Test the Vincenzo et al. (2016) mass-lifetime relationship. 
 */ 

#include "../vincenzo2016.h" 
#include "vincenzo2016.h" 
#include "common.h" 


/* 
 * Test the Vincenzo et al. (2016) lifetime function at a range of values for 
 * post main sequence lifetimes and metallicities to ensure that the values 
 * are larger than the accepted minimum of 3 Myr. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: vincenzo2016.h 
 */ 
extern unsigned short test_vincenzo2016_minimum_lifetime(void) {

	return baseline_minimum_lifetime_test(&vincenzo2016_lifetime); 

}


/* 
 * Test the Vincenzo et al. (2016) turnoff mass function for monotonicity at a 
 * range of values for post main sequence lifetimes and metallicities. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: vincenzo2016.h 
 */ 
extern unsigned short test_vincenzo2016_turnoffmass_monotonicity(void) {

	return baseline_monotonicity_test_turnoffmass(&vincenzo2016_turnoffmass); 

}


/* 
 * Test the Vincenzo et al. (2016) lifetime function for monotonicity at a 
 * range of values for post main sequence lifetimes and metallicities. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: vincenzo2016.h 
 */ 
extern unsigned short test_vincenzo2016_lifetime_monotonicity(void) {

	return baseline_monotonicity_test_lifetime(&vincenzo2016_lifetime); 

}

