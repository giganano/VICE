/* 
 * This file implements testing of the statistics functions at 
 * vice/src/stats.h
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../stats.h" 
#include "../utils.h" 
#include "stats.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short get_test_sample_bin_number(double deviation); 
static double unnormalized_gaussian(double x); 
static double standard_deviation(double *arr, unsigned long length); 

/* 
 * TEST_GAUSSIAN_SIGMA: 	The dispersion of the test distribution 
 * TEST_GAUSSIAN_MEAN: 		The mean of the test distribution 
 * TEST_N_SAMPLE: 			The number of points to sample in testing 
 */ 
static double TEST_GAUSSIAN_SIGMA = 1; 
static double TEST_GAUSSIAN_MEAN = 0; 
static unsigned long TEST_N_SAMPLE = 1e7; 


/* 
 * Test the normal distribution sampler at vice/src/stats.h 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: stats.h 
 */ 
extern unsigned short test_normal(void) { 

	seed_random(); 
	unsigned long i; 
	double *test_sample = (double *) malloc (TEST_N_SAMPLE * sizeof(double)); 
	for (i = 0ul; i < TEST_N_SAMPLE; i++) {
		test_sample[i] = normal(TEST_GAUSSIAN_MEAN, TEST_GAUSSIAN_SIGMA); 
	} 
	
	/* 
	 * Get the counts below 2 sigma, between 1 and 2 sigma below, between 
	 * the mean and 1 sigma below, between the mean and 1 sigma above, between 
	 * 1 sigma and 2 sigma above, and 2 sigma above. 
	 */ 
	unsigned long counts[6] = {0ul, 0ul, 0ul, 0ul, 0ul, 0ul}; 
	for (i = 0ul; i < TEST_N_SAMPLE; i++) { 
		counts[get_test_sample_bin_number(
			test_sample[i] - TEST_GAUSSIAN_MEAN
		)]++; 
	} 
	free(test_sample); 

	/* 
	 * Now determine the value of the test based on whether or not the counts 
	 * are consistent with a gaussian within poisson errors. 
	 */ 
	double densities[6]; 
	double errors[6]; 
	double correct[6] = {
		0.0227, 
		0.1359, 
		0.3413, 
		0.3413, 
		0.1359, 
		0.0227 
	}; 

	/* 
	 * The value of the test is based on whether or not the calculated 
	 * densities are within 3-sigma of the true gaussian densities 
	 */ 
	for (i = 0ul; i < 6ul; i++) { 
		densities[i] = (double) counts[i] / (double) TEST_N_SAMPLE; 
		errors[i] = sqrt( (double) counts[i] ) / (double) TEST_N_SAMPLE; 
		if (absval(densities[i] - correct[i]) > 3 * errors[i]) return 0u; 
	} 
	return 1u; 

} 


/* 
 * Get the bin number to place the counts within -> either 2 sigma below the 
 * test mean, between 1 and 2 sigma below, less than 1 sigma below, less than 
 * 1 sigma above, between 1 and 2 sigma above, and more than 2 sigma above, 
 * in that order. 
 */ 
static unsigned short get_test_sample_bin_number(double deviation) {

	if (deviation < -2 * TEST_GAUSSIAN_SIGMA) {
		return 0u; 
	} else if (-2 * TEST_GAUSSIAN_SIGMA < deviation && 
		deviation < -1 * TEST_GAUSSIAN_SIGMA) {
		return 1u; 
	} else if (-1 * TEST_GAUSSIAN_SIGMA < deviation && deviation < 0) {
		return 2u; 
	} else if (0 < deviation && deviation < TEST_GAUSSIAN_SIGMA) {
		return 3u; 
	} else if (TEST_GAUSSIAN_SIGMA < deviation && 
		deviation < 2 * TEST_GAUSSIAN_SIGMA) {
		return 4u; 
	} else { 
		return 5u; 
	} 

} 


/* 
 * Test the sample routine at vice/src/stats.h 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: stats.h 
 */ 
extern unsigned short test_sample(void) {

	/* 
	 * Test the function by sampling a gaussian distribution and ensuring that 
	 * the mean and standard deviation are within a reasonable numerical error 
	 * of the known values prior to resampling. 
	 * 
	 * In the case of the mean, ensure that it is within the error on the mean 
	 * of the known mean of the distribution. 
	 */ 

	unsigned long i, n_bins = 2e5, n_sample = 1e4; 
	double *bins = binspace(-10, 10, n_bins); 
	double *centers = bin_centers(bins, n_bins); 
	double *gaussian = (double *) malloc (n_bins * sizeof(double)); 
	for (i = 0u; i < n_bins; i++) {
		gaussian[i] = unnormalized_gaussian(centers[i]); 
	} 

	unsigned short status = 1u; 
	double *resampled = sample(gaussian, bins, n_bins, n_sample); 
	double mean = sum(resampled, n_sample) / n_sample; 
	double std = standard_deviation(resampled, n_sample); 
	status &= absval(mean - TEST_GAUSSIAN_MEAN) < 2 * std / sqrt(n_sample); 
	status &= absval(std - TEST_GAUSSIAN_SIGMA) < 0.1; 
	free(bins); 
	free(centers); 
	free(gaussian); 
	free(resampled); 
	return status; 

}


/* 
 * Test the convert to CDF function at vice/src/stats.h 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * header: stats.h 
 */ 
extern unsigned short test_convert_to_CDF(void) {

	unsigned short i, status = 1u, n = 20000u; 
	double *bins = binspace(-10, 10, n); 
	double *centers = bin_centers(bins, n); 
	double *gaussian = (double *) malloc (n * sizeof(double)); 
	for (i = 0u; i < n; i++) {
		gaussian[i] = unnormalized_gaussian(centers[i]); 
	} 

	double *cdf = convert_to_CDF(gaussian, bins, n); 
	for (i = 1u; i < n; i++) {
		status &= cdf[i] >= 0; 
		status &= cdf[i] >= cdf[i - 1u]; 
		if (!status) break; 
	} 
	status &= absval(cdf[n - 1u] - 1) < 1e-15; 

	free(bins); 
	free(centers); 
	free(gaussian); 
	free(cdf); 
	return status; 

}


/* 
 * Test the convert to PDF function at vice/src/stats.h 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * header: stats.h 
 */ 
extern unsigned short test_convert_to_PDF(void) { 

	unsigned short i, n = 20000u; 
	double *bins = binspace(-10, 10, n); 
	double *centers = bin_centers(bins, n); 
	double *gaussian = (double *) malloc (n * sizeof(double)); 
	for (i = 0u; i < n; i++) { 
		gaussian[i] = unnormalized_gaussian(centers[i]); 
	} 

	double s = 0, *normed = convert_to_PDF(gaussian, bins, n); 
	for (i = 0u; i < n; i++) {
		s += normed[i] * (bins[i + 1u] - bins[i]); 
	} 
	free(bins); 
	free(centers); 
	free(gaussian); 
	free(normed); 
	return absval(s - 1) < 1e-15; 

} 


/* 
 * An unnormalized gaussian with dispersion TEST_GAUSSIAN_SIGMA 
 * 
 * Parameters 
 * ========== 
 * x: 		The value to evaluate the distribution at 
 */ 
static double unnormalized_gaussian(double x) { 

	return exp(
		-pow( x - TEST_GAUSSIAN_MEAN, 2) / 
		(2 * pow(TEST_GAUSSIAN_SIGMA, 2)) 
	); 

}


/* 
 * Compute the standard deviation of a sample of numbers. 
 * 
 * Parameters 
 * ==========
 * arr: 		A double pointer to the array of numbers to compute the 
 * 				standard deviation for 
 * length: 		The length of the array arr 
 * 
 * Returns 
 * =======
 * The square root of the sum of the squared difference between each value and 
 * the mean of the sample divided by the sample size. 
 */ 
static double standard_deviation(double *arr, unsigned long length) {

	unsigned long i; 
	double s = 0, mean = sum(arr, length) / length; 
	for (i = 0ul; i < length; i++) {
		s += pow(arr[i] - mean, 2); 
	} 
	return sqrt(s / length); 

}

