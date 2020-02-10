/* 
 * The following implements biased and unbiased square vertical offset 
 * functions for use in likelihood calculations as part of fitting simulated 
 * data to observed data. 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../likelihood.h" 
#include "vertical_offset.h" 
#include "utils.h" 


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
 * header: vertical_offset.h 
 */ 
extern double biased_sum_square_vertical_offset(double **data, double **errors, 
	double **predictions, unsigned short dimension, unsigned long n_points) {

	/* 
	 * To find the distance between two points in n-dimensional parameter 
	 * space, the vertical offsets are added in quadrature. To find the sum 
	 * squared distance, the square root can simply be removed. 
	 * 
	 * s = sum( ( (y - f(x))^2 / sigma )^2 )
	 * 
	 * where (x, y) are the data, f is a predicted fit, and sigma is the 
	 * error on the y-measurement. 
	 */ 

	/* Start by normalizing the data and the predictions by the errors */ 
	double **data_normed = normalize_by_errors(data, errors, dimension, 
		n_points); 
	double **pred_normed = normalize_by_errors(predictions, errors, dimension, 
		n_points);  

	/* Let the unbiased routine take care of the rest with the normed data */ 
	double s = unbiased_sum_square_vertical_offset(data_normed, pred_normed, 
		dimension, n_points); 
	free(data_normed); 
	free(pred_normed); 
	return s; 

} 


/* 
 * Determine the sum-squared vertical offset between a set of data points 
 * and simulated predictions with no weight on uncertainties. This is an 
 * unbiased fit to the data, in that the size of the errors on each 
 * measurement are irrelevant. In an unbiased least-squares fit, this is the 
 * quantity to be minimized. 
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
 * header: vertical_offset.h 
 */ 
extern double unbiased_sum_square_vertical_offset(double **data, 
	double **predictions, unsigned short dimension, unsigned long n_points) {

	/* 
	 * The sum squared distance here is calculated similar as above, but with 
	 * no weight to the error: 
	 * 
	 * s = sum( (y - f(x))^2 ) 
	 */ 

	double s = 0; 		/* iterative sum */ 
	unsigned long i; 
	for (i = 0ul; i < n_points; i++) {
		unsigned short j; 
		for (j = 0u; j < dimension; j++) {
			s += pow(data[i][j] - predictions[i][j], 2); 
		} 
	} 
	return s; 

}

