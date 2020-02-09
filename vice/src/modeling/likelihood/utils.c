/* 
 * This file implements utility functions for the likelihood calculations 
 */ 

#include <stdlib.h> 
#include "../likelihood.h" 
#include "utils.h" 


/* 
 * Normalizes a dataset (either observed or predicted) by the associated 
 * errors on the observational dataset. 
 * 
 * Parameters 
 * ========== 
 * data: 		The dataset 
 * errors: 		The errors on each quantity in the dataset 
 * dimension: 	The dimensionality of the data 
 * n_points: 	The number of points in the data 
 * 
 * Returns 
 * ======= 
 * A new data table, where the ij'th element is the ij'th element of data 
 * divided by the ij'th element of errors. 
 * 
 * header: utils.h 
 */ 
extern double **normalize_by_errors(double **data, double **errors, 
	unsigned short dimension, unsigned long n_points) {

	unsigned long i; 
	unsigned short j; 
	double **normed = (double **) malloc (n_points * sizeof(double *)); 
	for (i = 0ul; i < n_points; i++) {
		normed[i] = (double *) malloc (dimension * sizeof(double)); 
		for (j = 0u; j < dimension; j++) {
			normed[i][j] = data[i][j] / errors[i][j]; 
		} 
	} 
	return normed; 

} 

