
#ifndef MODELING_LIKELIHOOD_COVARIANCE_H 
#define MODELING_LIKELIHOOD_COVARIANCE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Obtain the inverse covariance matrix of a set of data points. In calculating 
 * chi-squared likelihoods, this matrix (rather than the covariance matrix 
 * itself) is of interest. 
 * 
 * Parameters 
 * ========== 
 * data: 			The observed data set 
 * dimension: 		The dimensionality of the data (i.e. number of quantities) 
 * n_points: 		The number of observations in the data set (length of the 
 * 					array) 
 * 
 * Returns 
 * ======= 
 * C^-1 - the matrix to be used in computing chi-squared likelihoods 
 * 
 * source: covariance.c 
 */ 
extern double **inverse_covariance_matrix(double **data, 
	unsigned short dimension, unsigned long n_points); 

/* 
 * Calculate the covariance matrix for a set of data 
 * 
 * Parameters 
 * ========== 
 * data: 		The data itself as an n_points x dimension matrix 
 * dimension: 	The number of columns in the data matrix 
 * n_points: 	The number of rows in the data matrix 
 * 
 * Returns 
 * ======= 
 * Cov_ij = <data_i data_j> - <data_i> <data_j> 
 * 
 * source: covariance.c 
 */ 
extern double **covariance_matrix(double **data, unsigned short dimension, 
	unsigned long n_points); 

#ifdef __cplusplus 
}
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_COVARIANCE_H */ 
