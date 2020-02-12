/* 
 * This file implements the algorithm obtaining a predicted data set from 
 * the comparison between an observed and a simulated data set 
 */ 

#include <stdlib.h> 
#include <math.h> 
#include "../modeling.h" 
#include "predictions.h" 
#include "likelihood/linalg.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double *assign_prediction(double *pt, double *err, 
	double **simulated_data, unsigned short dimension, 
	unsigned long n_simulated_pts); 
static double *distsqrd_to_each_prediction(double *pt, double *err, 
 	double **simulated_data, unsigned short dimension, 
 	unsigned long n_simulated_pts); 
static double n_dimensional_distance_squared(double *pt1, double *pt2, 
	double *err, unsigned short dimension); 
static unsigned long idx_minimum(double *arr, unsigned long n); 
static double *copy_pt(double *pt, unsigned short dimension); 


/* 
 * Assign model predictions from a simulated dataset to each observational data 
 * point by adopting the point from the simulated data which is closest to it 
 * in n-dimensional parameter space, normalized by the observational 
 * uncertainty on each measurement. 
 * 
 * Parameters 
 * ========== 
 * ds: 					The dataset object 
 * simulated_data: 		The simulated data set, in the same format as the 
 * 						data within the dataset object. 
 * n_simulated_pts: 	The number of points in the simulated data 
 * 
 * Notes 
 * ===== 
 * The algorithm implemented here is mathematically identical to assigning 
 * model predictions to data based on the minimum chi-squared if covariance 
 * were ignored. Covariance is taken into account in likelihood calculations, 
 * but is not of concern when finding the simulated data point that best suits 
 * a single observed data point. 
 * 
 * This function will overwrite any assigned predictions already in the 
 * dataframe. 
 * 
 * header: predictions.h 
 */ 
extern void assign_predictions(DATASET *ds, double **simulated_data, 
	unsigned long n_simulated_pts) { 

	/* overwrite predictions currently there */ 
	unsigned long i; 
	if ((*ds).predictions != NULL) {
		for (i = 0ul; i < (*ds).n_points; i++) {
			if ((*ds).predictions[i] != NULL) {
				free(ds -> predictions[i]); 
				ds -> predictions[i] = NULL; 
			} else {} 
		} 
		free(ds -> predictions); 
		ds -> predictions = NULL; 
	} else {} 

	ds -> predictions = (double **) malloc ((*ds).n_points * sizeof(double *)); 
	for (i = 0ul; i < (*ds).n_points; i++) {
		ds -> predictions[i] = assign_prediction((*ds).data[i], (*ds).errors[i], 
			simulated_data, (*ds).n_quantities, n_simulated_pts); 
	} 

}


/* 
 * Assign a data point a model prediction from the simulated data set  
 * 
 * Parameters 
 * ========== 
 * pt: 					The data point to assign a prediction to 
 * err: 				The error on the data point 
 * simulated_data: 		The simulated data set 
 * dimension: 			The dimensionality of the data 
 * n_simulated_pts: 	The number of points in the simulated data set 
 * 
 * Returns 
 * ======= 
 * The simulated data point which has the smallest chi-squared ignoring 
 * covariance. In short, this assigns the simulated data point which is at the 
 * smallest distance to the observed data point in units of the observational 
 * uncertainty. 
 * 
 * Notes 
 * ===== 
 * The likelihood assigned to a given model does NOT ignore covariance. That is 
 * ignored here because this is only the algorithm which assigns a model 
 * prediction to a data point, and thus it is only the error on the measurements 
 * of each individual quantity which are relevant to this. 
 */ 
static double *assign_prediction(double *pt, double *err, 
	double **simulated_data, unsigned short dimension, 
	unsigned long n_simulated_pts) { 

	double *comparisons = distsqrd_to_each_prediction(pt, err, simulated_data, 
		dimension, n_simulated_pts); 
	unsigned long idx_min = idx_minimum(comparisons, n_simulated_pts); 
	free(comparisons); 
	return copy_pt(simulated_data[idx_min], dimension); 

}


/* 
 * Determine the distance squared between the observed data point and each 
 * simulated data point in n-dimensional parameter space. 
 * 
 * Parameters 
 * ========== 
 * pt: 					The observed data point 
 * err: 				The error on the data point 
 * simulated_data: 		The simulated data set 
 * dimension: 			The dimensionality of the data 
 * n_simulated_pts: 	The number of points in the simulated data set 
 * 
 * Returns 
 * ======= 
 * The n-dimensional distance squared from the observed point to each simulated 
 * point. 
 */ 
static double *distsqrd_to_each_prediction(double *pt, double *err, 
	double **simulated_data, unsigned short dimension, 
	unsigned long n_simulated_pts) {

	unsigned long i; 
	double *distsqrd = (double *) malloc (n_simulated_pts * sizeof(double)); 
	for (i = 0ul; i < n_simulated_pts; i++) {
		distsqrd[i] = n_dimensional_distance_squared(pt, simulated_data[i], 
			err, dimension); 
	} 
	return distsqrd; 

}


/* 
 * Determine the distance-squared between two points in n-dimensional space 
 * 
 * Parameters 
 * ========== 
 * pt1: 			The first point 
 * pt2: 			The second point 
 * err: 			The error to divide the distance by 
 * dimension: 		The dimensionality of the points (assumed the same) 
 * 
 * Returns 
 * ======= 
 * sum((pt1_i - pt2_i)^2) where i goes from 1 to dimension 
 */ 
static double n_dimensional_distance_squared(double *pt1, double *pt2, 
	double *err, unsigned short dimension) { 

	unsigned short i; 
	double distsqrd = 0; 
	for (i = 0u; i < dimension; i++) { 
		distsqrd += pow( (pt1[i] - pt2[i]) / err[i], 2); 
	} 
	return distsqrd; 

} 


/* 
 * Determine the index of the minimum value in an array of doubles 
 * 
 * Parameters 
 * ========== 
 * arr: 		The array itself 
 * n: 			The number of values in the array 
 * 
 * Returns 
 * ======= 
 * idx, where arr[idx] is the minimum value of the array 
 */ 
static unsigned long idx_minimum(double *arr, unsigned long n) {

	if (n >= 2) {
		unsigned long i, idx = arr[0] > arr[1] ? 0ul : 1ul; 
		for (i = 2ul; i < n; i++) {
			idx = arr[i] > arr[idx] ? i : idx; 
		} 
		return idx; 
	} else { 
		return 0ul; 
	} 

} 


/* 
 * Obtain a copy of a data point 
 * 
 * Parameters 
 * ========== 
 * pt: 			The point to copy 
 * dimension: 	The dimensionality of the data point 
 * 
 * Returns 
 * ======= 
 * The same as pt, but in a different block of memory 
 */ 
static double *copy_pt(double *pt, unsigned short dimension) {

	unsigned short i; 
	double *copy = (double *) malloc (dimension * sizeof(double)); 
	for (i = 0u; i < dimension; i++) {
		copy[i] = pt[i]; 
	} 
	return copy; 

} 

