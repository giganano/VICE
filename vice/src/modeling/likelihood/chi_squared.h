
#ifndef MODELING_LIKELIHOOD_CHI_SQUARED_H 
#define MODELING_LIKELIHOOD_CHI_SQUARED_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

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
 * source: chi_squared.c 
 */  
extern double chi_squared_likelihood(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points, 
	unsigned short biased); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_CHI_SQUARED_H */ 
