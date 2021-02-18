
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
 * A psuedo-random number drawn from a guassian distribution with specified 
 * mean and standard deviation. 
 * 
 * header: stats.h 
 */ 
extern double normal(double mean, double sigma); 

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



