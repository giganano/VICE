
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

/* 
 * Draw a given number of samples from a known distribution. 
 * 
 * Parameters 
 * ========== 
 * dist: 		The distribution itself, assumed to be unnormalized 
 * bins: 		The bin edges on which the distribution is sampled 
 * n_bins: 		The number of bins in the distribution. This is always 1 less 
 * 				than the number of bin edges. 
 * n: 			The number of samples to draw 
 * 
 * Returns 
 * ======= 
 * A double pointer to an n-element array of values drawn from the given 
 * distribution. 
 * 
 * header: stats.h 
 */ 
extern double *sample(double *dist, double *bins, unsigned long n_bins, 
	unsigned long n) {

	/* 
	 * Given the cumulative distribution function associated with a known 
	 * distribution, a sampled value can be drawn from the bin number of a 
	 * pseudorandom number between 0 and 1. Thus first convert the 
	 * distribution to a CDF and allocate memory for n doubles. 
	 */ 
	double *cdf = convert_to_CDF(dist, bins, n_bins); 
	double *values = (double *) malloc (n * sizeof(double)); 

	unsigned long i; 
	seed_random(); 
	for (i = 0l; i < n; i++) { 
		double x = (double) rand() / RAND_MAX; 
		long bin = get_bin_number(cdf, n_bins, x); 
		switch (bin) {

			case -1l: 
				/* 
				 * This shouldn't happen given the nature of this 
				 * implementation; included as a failsafe. 
				 */ 
				free(cdf); 
				free(values); 
				return NULL; 

			default: 
				/* 
				 * CDFs must be interpreted from the right-hand bin edges 
				 * rather than the left, so increment the bin number by 1 
				 * 
				 * Assume uniform likelihood within that bin of the CDF and 
				 * randomly draw a value in that range. 
				 */ 
				if ((unsigned) bin != n_bins - 1l) bin++; 
				values[i] = rand_range(bins[bin], bins[bin + 1l]); 
				break; 

		} 

	} 

	free(cdf); 
	return values; 

}

/* 
 * Convert a distribution to a cumulative distribution function (CDF). 
 * 
 * Parameters 
 * ========== 
 * dist: 		The values of the distribution itself in each bin 
 * bins: 		The bin edges on which the distribution is sampled 
 * n_bins: 		The number of bins in the distribution. This is always 1 less 
 * 				than the number of bin edges. 
 * 
 * Returns 
 * ======= 
 * A distribution whose values represent the fraction of values with bin 
 * numbers <= N. 
 * 
 * header: stats.h 
 */ 
extern double *convert_to_CDF(double *dist, double *bins, 
	unsigned long n_bins) { 

	/* First make a copy of the distribution */ 
	unsigned long i; 
	double *cdf = (double *) malloc (n_bins * sizeof(double)); 
	for (i = 0l; i < n_bins; i++) {
		cdf[i] = dist[i]; 
	}

	/* 
	 * Ignoring the first bin, add the value of the distribution from all 
	 * previous bins. 
	 */ 
	for (i = 1l; i < n_bins; i++) {
		cdf[i] += cdf[i - 1]; 
	} 

	/* 
	 * By definition a CDF converges to 1 as the bin number increases, so 
	 * enforce that definition here. 
	 */ 
	for (i = 0l; i < n_bins; i++) {
		cdf[i] /= cdf[n_bins - 1l]; 
	} 

	return cdf; 

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


