
#ifndef MODELING_LIKELIHOOD_UTILS_H 
#define MODELING_LIKELIHOOD_UTILS_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

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
 * source: utils.c 
 */ 
extern double **normalize_by_errors(double **data, double **errors, 
	unsigned short dimension, unsigned long n_points); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_UTILS_H */ 

