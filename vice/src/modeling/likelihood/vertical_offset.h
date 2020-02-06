
#ifndef MODELING_LIKELIHOOD_VERTICAL_OFFSET_H 
#define MODELING_LIKELIHOOD_VERTICAL_OFFSET_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Determine the sum-squared vertical offset between a set of data points 
 * and simulated predictions in units of the error on each measurement. This 
 * is a biased fit in that the points with the smallest errors will have the 
 * most constraining power. In a biased least-squares fit, this is the 
 * quantity to be minimized. 
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
 * The sum-squared distance between the predictions and the data in the 
 * n-dimensional parameter space, weighted by observational uncertainty. 
 * 
 * source: utils.c 
 */ 
extern double biased_sum_square_vertical_offset(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points); 

/* 
 * Determine the sum-squared vertical offset between a set of data points 
 * and simulated predictions with no weight on uncertainties. This is an 
 * unbiased fit to the data, in that the size of the errors between each 
 * measurement and the prediction are irrelevant. In an unbiased least-squares 
 * fit, this is the quantity to be minimized. 
 * 
 * Parameters 
 * ========== 
 * data: 			The n-dimensional measurements 
 * predictions: 	The n-dimensional predictions for each point 
 * dimension: 		The dimensionality of the data 
 * n_points: 		The number of points and predictions (assumed to be the 
 * 					same) 
 * 
 * Returns 
 * ======= 
 * The sum-squared distance between the predictions and the data in the 
 * n-dimensional parameter space, unweighted by observational uncertainty. 
 * 
 * source: utils.c 
 */ 
extern double unbiased_sum_square_vertical_offset(double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_LIKELIHOOD_VERTICAL_OFFSET_H */ 

