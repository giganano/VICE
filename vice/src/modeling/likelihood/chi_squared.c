/* 
 * The following implements biased and unbiased chi-squared calculations 
 * for use in likelihood calculations as part of fitting simulated data to 
 * observed data.  
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../likelihood.h" 
#include "chi_squared.h" 
#include "utils.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double biased_chi_squared(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points); 
static double unbiased_chi_squared(double **data, double **predictions, 
	unsigned short dimension, unsigned long n_points); 


/* 
 * Determine the likelihood via e^(-chi^2 / 2) that a set of predictions 
 * reproduce a given set of observational data. In a minimum chi-squared 
 * fit, this is the quantity that is to be maximized. In the case of a 
 * biased fit, chi-squared is measured from a set of data and predictions 
 * normalized by the uncertainty, giving weight to the measurements with the 
 * highest precision. 
 * 
 * Parameters 
 * ========== 
 * data: 			The n-dimensional measurements 
 * errors: 			The errors on each measurement 
 * predictions: 	The n-dimensional predictions for each point 
 * dimension: 		The dimensionality of the data 
 * n_points: 		The number of points and predictions (assumed to be the 
 * 					same) 
 * biased: 			0 for an unbiased fit, nonzero for biased 
 * 
 * Returns 
 * ======= 
 * e^-(chi^2 / 2) to an arbitrary normalization. 
 * 
 * Notes  
 * ===== 
 * In the case of an unbiasd fit, NULL may be passed for the errors parameter. 
 * 
 * header: chi_squared.h 
 */ 
extern double chi_squared_likelihood(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points, 
	unsigned short biased) { 

	if (biased) {
		return exp(
			-biased_chi_squared(data, errors, predictions, 
				dimension, n_points) / 2
		); 
	} else {
		return exp(
			-unbiased_chi_squared(data, predictions, dimension, n_points) / 2  
		); 
	} 

}


/* 
 * Determine the value of chi-squared with weight to the observational 
 * uncertainties. This is a biased fit to the data, in that the points with 
 * the smallest errors will have the most constraining power. 
 * 
 * Parameters 
 * ========== 
 * data: 			The n-dimensional measurements 
 * errors: 			The errors on each measurement 
 * predictions: 	The n-dimensional predictions for each point 
 * dimension: 		The dimensionality of the data 
 * n_points: 		The number of points and predictions (assumed to be the 
 * 					same) 
 * 
 * Returns 
 * ======= 
 * The value of chi-squared weighted by uncertainties for the given set of 
 * predictions. 
 */ 
static double biased_chi_squared(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points) {

	/* 
	 * The formula for chi-squared when quantities are normalized by the 
	 * uncertainties: 
	 * 
	 * s = sum( ( (y - f(x)) / sigma )^2 / (f(x) / sigma) ) 
	 * 
	 * where (x, y) are the data, f is a predicted fit, and sigma is the 
	 * error on the y-measurement. 
	 */ 

	/* Start by normalizing the data and the predictions by the errors */ 
	double **data_normed = normalize_by_errors(data, errors, dimension, 
		n_points); 
	double **pred_normed = normalize_by_errors(predictions, errors, dimension, 
		n_points); 

	/* Let the unbiased routine take care of the rest with the normed data */ 
	double s = unbiased_chi_squared(data, predictions, dimension, n_points); 
	free(data_normed); 
	free(pred_normed); 
	return s; 

}


/* 
 * Determine the value of chi-squared with no weight to the observational 
 * uncertainties. This is an unbiased fit to the data, in that the size of the 
 * errors on each measurement are irrelevant. 
 * 
 * Parameters 
 * ========== 
 * data: 			The n-dimensional measurements 
 * predictions: 	The n-dimensional predictions for each point 
 * dimension: 		The dimensionality of the data 
 * n_points: 		The number of points and predictions(assumed to be the 
 * 					same)
 * 
 * Returns 
 * ======= 
 * The value of chi-squared unweighted by uncertainties for the given set of 
 * predictions. 
 */ 
static double unbiased_chi_squared(double **data, double **predictions, 
	unsigned short dimension, unsigned long n_points) {

	/* 
	 * The value of chi-squared here is calculated similar as above, but with 
	 * no weight to the error: 
	 * 
	 * s = sum( (y - f(x))^2 / f(x) ) 
	 */ 

	double s = 0; 		/* iterative sum */ 
	unsigned long i; 
	for (i = 0ul; i < n_points; i++) {
		unsigned short j; 
		for (j = 0u; j < dimension; j++) {
			s += pow(data[i][j] - predictions[i][j], 2) / predictions[i][j]; 
		} 
	} 
	return s; 

}

