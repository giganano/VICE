
#ifndef MODELING_LIKELIHOOD_CHI_SQUARED_H 
#define MODELING_LIKELIHOOD_CHI_SQUARED_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Calculate relative likelihood using the "delta chi-squared" approach 
 * 
 * Parameters 
 * ========== 
 * chisq1: 			The chi-squared value to test 
 * chisq2: 			The reference chi-squared value 
 * 
 * Returns 
 * ======= 
 * e^( -(chisq1 - chisq2) / 2 ) 
 * 
 * source: chi_squared.c 
 */ 
extern double relative_likelihood(double chisq1, double chisq2); 

/* 
 * Calculate chi-squared for a given set of data and the model predictions. 
 * 
 * Parameters 
 * ========== 
 * inv_cov: 			The inverse covariance matrix of the data 
 * data: 				The data themselves 
 * predictions: 		The model predictions for each data point 
 * dimension: 			The dimensionality of the data 
 * n_points: 			The number of points in the data and predicted data sets 
 * 						(assumed to be the same) 
 * 
 * Returns 
 * ======= 
 * The value of chi-squared defined by:
 * sum( (y_k - y_mod(x_k)) * inv_cov * (y_k - y_mod(x_k))^T ) 
 * 
 * source: chi_squared.c 
 */ 
extern double chi_squared(double **inv_cov, double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points); 

/* 
 * Calculate the likelihood to an arbitrary normalization (only relative 
 * likelihoods are necessary in fitting) that model predictions reproduce a 
 * given data set via L \propto e^(-chi^2 / 2) 
 * 
 * Parameters 
 * ========== 
 * inv_cov: 			The inverse covariance matrix of the data 
 * data: 				The data themselves 
 * predictions: 		The model predictions for each data point 
 * dimension: 			The dimensionality of the data 
 * n_points: 			The number of points in the data and predicted data sets 
 * 						(assumed to be the same) 
 * 
 * Returns 
 * ======= 
 * The value of e^(-chi^2 / 2) 
 * 
 * source: chi_squared.c 
 */ 
extern double chi_squared_likelihood(double **inv_cov, double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_CHI_SQUARED_H */ 
