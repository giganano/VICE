
#ifndef MODELING_PREDICTIONS_H 
#define MODELING_PREDICTIONS_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../objects.h" 

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
 * source: predictions.c 
 */ 
extern void assign_predictions(DATASET *ds, double **simulated_data, 
	unsigned long n_simulated_pts); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_PREDICTION_H */ 
