
#ifndef MODELING_LIKELIHOOD_COVARIANCE_H 
#define MODELING_LIKELIHOOD_COVARIANCE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "../../objects.h" 

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
