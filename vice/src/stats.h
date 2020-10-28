
#ifndef STATS_H 
#define STATS_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#ifndef PI 
#define PI 3.14159265358979323846 
#endif /* PI */ 

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
 * source: stats.c 
 */ 
extern double normal(double mean, double sigma); 

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
 * Notes 
 * =====
 * This function implements inverse transform sampling from a discrete 
 * distribution. 
 * 
 * This function does NOT seed the random number generator. 
 * 
 * source: stats.c 
 */ 
extern double *sample(double *dist, double *bins, unsigned long n_bins, 
	unsigned long n); 

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
 * numbers < N. 
 * 
 * source: stats.c 
 */ 
extern double *convert_to_CDF(double *dist, double *bins, 
	unsigned long n_bins); 

/* 
 * Convert a distribution in a given binspace to a probability distribution 
 * function (PDF). 
 * 
 * Parameters 
 * ========== 
 * dist:		The value of the distribution itself 
 * bins: 		The bin edges on which the distribution is sampled 
 * n_bins: 		The number of bins in the distribution. This is always 1 less 
 * 				than the number of bin edges. 
 * 
 * Returns 
 * ======= 
 * A distribution with the same trends as that which was passed, but whose 
 * integral is equal to 1. 
 * 
 * source: stats.h 
 */ 
extern double *convert_to_PDF(double *dist, double *bins, 
	unsigned long n_bins); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* STATS_H */ 



