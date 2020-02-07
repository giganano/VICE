
#ifndef MODELING_LIKELIHOOD_CHI_SQUARED_H 
#define MODELING_LIKELIHOOD_CHI_SQUARED_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

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
