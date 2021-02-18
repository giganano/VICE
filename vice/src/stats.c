
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
 * A psuedo-random number drawn from a guassian distribution with specified 
 * mean and standard deviation. 
 * 
 * header: stats.h 
 */ 
extern double normal(double mean, double sigma) { 
 
	/* Start with two random numbers between 0 and 1 */ 
	double r1 = (double) rand() / RAND_MAX; 
	double r2 = (double) rand() / RAND_MAX; 

	/* The Box-Muller Transformation */ 
	double z1 = sqrt(-2 * log(r1)) * cos(2 * PI * r2); 
	double z2 = sqrt(-2 * log(r1)) * sin(2 * PI * r2); 

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


/* 
 * Convert a distribution in a given binspace to a probability distribution 
 * function (PDF). 
 * 
 * Parameters 
 * ========== 
 * dist:		The values of the distribution itself in each bin 
 * bins: 		The bin edges on which the distribution is sampled 
 * n_bins: 		The number of bins in the distribution. This is always 1 less 
 * 				than the number of bin edges. 
 * 
 * Returns 
 * ======= 
 * A distribution with the same trends as that which was passed, but whose 
 * integral is equal to 1. 
 * 
 * header: stats.h 
 */ 
extern double *convert_to_PDF(double *dist, double *bins, 
	unsigned long n_bins) { 

	/* Allocate memory; start counting at zero */ 
	double sum = 0, *pdf = (double *) malloc (n_bins * sizeof(double)); 
	unsigned long i; 

	/* Add up the area in each bin */ 
	for (i = 0l; i < n_bins; i++) {
		sum += dist[i] * (bins[i + 1l] - bins[i]); 
	} 

	/* Divide each element by the value of the integral */ 
	for (i = 0l; i < n_bins; i++) {
		pdf[i] = dist[i] / sum; 
	} 

	return pdf; 

} 

