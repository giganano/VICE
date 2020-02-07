/* 
 * This file implements covariance matrix calculations for arbitrary datasets.  
 */ 

#include <stdlib.h> 
#include <stdio.h> 
#include <math.h> 
#include "../likelihood.h" 
#include "covariance.h" 
#include "linalg.h" 
#include "utils.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double **deviations_matrix(double **data, unsigned short dimension, 
	unsigned long n_points); 
static double **square_ones_matrix(unsigned long N); 


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
 * header: covariance.h 
 */ 
extern double **inverse_covariance_matrix(double **data, 
	unsigned short dimension, unsigned long n_points) {

	double **cov = covariance_matrix(data, dimension, n_points); 
	double **inv_cov = invert(cov, dimension); 
	free(cov); 
	return inv_cov; 

}


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
 * header: covariance.h 
 */ 
extern double **covariance_matrix(double **data, unsigned short dimension, 
	unsigned long n_points) { 

	double **deviations = deviations_matrix(data, dimension, n_points); 
	double **deviations_T = transpose(deviations, n_points, dimension); 
	double **prod = multiply_matrices(deviations_T, deviations, dimension, 
		n_points, dimension); 
	double **result = multiply_matrix_scalar(prod, 1.0 / n_points, 
		dimension, dimension); 
	free(deviations); 
	free(deviations_T); 
	free(prod); 
	return result; 

} 


/* 
 * Obtain the deviations matrix for a set of data points 
 * 
 * Parameters 
 * ========== 
 * data: 			The data matrix itself 
 * dimension: 		The dimensionality of the data (or number of columns in the 
 * 					matrix) 
 * n_points: 		The number of data points (or number of rows in the matrix) 
 * 
 * Returns 
 * ======= 
 * The deviations matrix, defined by a_ij = data_ij - <data_j> 
 * = data_ij - 1/n sum(data_ij, i = 1 - n_points). In short, the ij'th element 
 * is the ij'th element of the data minus the mean of the j'th column 
 */ 
static double **deviations_matrix(double **data, unsigned short dimension, 
	unsigned long n_points) {

	double **square_ones = square_ones_matrix(n_points); 
	double **sum_in_columns = multiply_matrices(square_ones, data, n_points, 
		n_points, dimension); 
	double **mean_in_columns = multiply_matrix_scalar(sum_in_columns, 
		1.0 / n_points, n_points, dimension); 
	double **deviations = subtract_matrices(data, mean_in_columns, n_points, 
		dimension); 
	free(square_ones); 
	free(sum_in_columns); 
	free(mean_in_columns); 
	return deviations; 

}


/* 
 * Construct an NxN matrix of ones. 
 * 
 * Parameters 
 * ========== 
 * N: 		The side-length of the matrix 
 * 
 * Returns 
 * ======= 
 * A pointer to the NxN ones matrix. 
 */ 
static double **square_ones_matrix(unsigned long N) {

	unsigned long i, j; 
	double **square_ones = (double **) malloc (N * sizeof(double *)); 
	for (i = 0ul; i < N; i++) {
		square_ones[i] = (double *) malloc (N * sizeof(double)); 
		for (j = 0ul; j < N; j++) {
			square_ones[i][j] = 1; 
		} 
	} 
	return square_ones; 

}


