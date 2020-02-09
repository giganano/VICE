/* 
 * The following implements biased and unbiased chi-squared calculations 
 * for use in likelihood calculations as part of fitting simulated data to 
 * observed data.  
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../likelihood.h" 
#include "chi_squared.h" 
#include "linalg.h" 
#include "utils.h" 


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
 * header: chi_squared.h 
 */ 
extern double relative_likelihood(double chisq1, double chisq2) {

	return exp( -(pow(chisq1, 2) - pow(chisq2, 2)) / 2 ); 

}


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
 * header: chi_squared.h 
 */ 
extern double chi_squared(double **inv_cov, double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points) {

	unsigned long i; 
	unsigned short j; 
	double chi_sq = 0; 
	for (i = 0ul; i < n_points; i++) { 
		/* 
		 * The row vector of the difference between the data and model 
		 * prediction for that point 
		 */ 
		double **diff = (double **) malloc (sizeof(double *)); 
		diff[0] = (double *) malloc (dimension * sizeof(double)); 
		for (j = 0u; j < dimension; j++) {
			diff[0][j] = data[i][j] - predictions[i][j]; 
		} 
		/* The associated column vector */ 
		double **diff_transpose = transpose(diff, 1, dimension); 

		/* multiply the row vector by the inverse covariance matrix */ 
		double **prod1 = multiply_matrices(diff, inv_cov, 1, dimension, 
			dimension); 

		/* 
		 * multiply the result by the column vector, resulting in a 1x1 
		 * matrix to be added to chi-squared 
		 */ 
		 double **prod2 = multiply_matrices(prod1, diff_transpose, 1, dimension, 
		 	1); 

		chi_sq += prod2[0][0]; 

		free(diff); 
		free(diff_transpose); 
		free(prod1); 
		free(prod2); 

	} 

	return chi_sq; 

} 


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
 * header: chi_squared.h 
 */ 
extern double chi_squared_likelihood(double **inv_cov, double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points) {

	return exp(
		-chi_squared(inv_cov, data, predictions, dimension, n_points) / 2 
	); 

} 

