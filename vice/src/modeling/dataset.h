/* 
 * This is the header file for the dataset object. 
 */ 

#ifndef MODELING_DATASET_H 
#define MODELING_DATASET_H 

#ifdef __cpluspus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Assess the likelihood that the model predictions stored in the dataset 
 * object reproduce the stored data via a chi-squared likelihood function 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * 
 * See Also 
 * ======== 
 * chi_squared_likelihood (header: likelihood/chi_squared.h) 
 * 
 * source: dataset.c 
 */ 
extern double dataset_assess_model_predictions(DATASET *ds); 

/* 
 * Obtain and store the inverse covariance matrix of the data in the dataset 
 * object. 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset itself 
 * 
 * Notes 
 * ===== 
 * If the covariance matrix has already been set, this will automatically free 
 * the memory the current version occupies, and update it. 
 * 
 * This function will do nothing if there is no data in the dataset object yet. 
 * 
 * source: dataset.c 
 */ 
extern void dataset_covariance(DATASET *ds); 

/* 
 * Add a new quantity to the dataset. 
 * 
 * Parameters 
 * ========== 
 * ds: 				The dataset object 
 * measurements: 	Each measurement -> this must be measurements of the same 
 * 					quantity for each data point, not a point with its 
 * 					measurement of each quantity of interest. 
 * n: 				The number of observations. If quantities have already 
 * 					been added to the dataset, this must match the attribute 
 * 					n_quantities to ensure that the data is a square table 
 * 
 * Returns 
 * ======= 
 * 0 on success. 1 if measurements does not contain the same number of points 
 * as any data already present. 
 * 
 * source: dataset.c 
 */ 
extern unsigned short dataset_new_quantity(DATASET *ds, double *measurements, 
	unsigned long n); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_DATASET_H */ 

