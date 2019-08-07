
#include <stdlib.h> 
#include <math.h> 
#include "stats.h" 
#include "utils.h" 

/* 
 * Generate a pseudo-random number from a normal distribution. This function 
 * makes use of the Box-Muller tranformation to do so. 
 * 
 * Parameters 
 * ========== 
 * mean: 		The mean of the distribution 
 * sigma: 		The standard deviation of the distribution 
 * 
 * Returns 
 * ======= 
 * A psuedo-random number drawn from a guassian distribution with specified mean 
 * and standard deviation. 
 * 
 * header: stats.h 
 */ 
extern double normal(double mean, double sigma) {

	/* 
	 * Start by seeding the random number generator and generating two 
	 * pseudo-random numbers 
	 */ 
	seed_random(); 
	double r1 = (double) rand() / RAND_MAX; 
	double r2 = (double) rand() / RAND_MAX; 

	/* The Box-Muller Transformation */ 
	double z1 = sqrt(-2 * log(r1)) * cos(2 * PI * r2); 
	double z2 = sqrt(-2 * log(r2)) * sin(2 * PI * r1); 

	/* 
	 * Box-Muller give two pseudo-random numbers generated according to a 
	 * normal distribution with mean 0 and standard deviation 1. Decide which 
	 * one to take via coin flip, let z1/z2 denote how many standard deviations 
	 * to offset by, add the mean and return. 
	 */ 
	if ((double) rand() / RAND_MAX >= 0.5) { 
		return mean + z1 * sigma; 
	} else {
		return mean + z2 * sigma; 
	}


}



