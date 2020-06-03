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
 * Performs the __getitem__ function when the user is requesting an element of 
 * the observed data by column label. 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * label: 		The label of the desired quantity 
 * 
 * Returns 
 * ======= 
 * The column of the data with the given label. NULL if the label is not 
 * recognized. 
 * 
 * source: dataset.c 
 */ 
extern double *dataset_getitem_data(DATASET ds, char *label); 

/* 
 * Performs the __getitem__ function when the user is requesting an element of 
 * the observational errors by column label. 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * label: 		The label of the desiged quantity to get the error from 
 * 
 * Returns 
 * ======= 
 * The errors associated with the given quantity. NULL if the label is not 
 * recognized. 
 * 
 * source: dataset.c 
 */ 
extern double *dataset_getitem_errors(DATASET ds, char *label); 

/* 
 * Performs the __setitem__ function when the user is setting an element of the 
 * observed data by column label. 
 * 
 * Parameters 
 * ========== 
 * ds: 				The dataset object 
 * measurements: 	The measurements to be added to the dataset 
 * label: 			The label to attach to the quantities 
 * n: 				The number of elements in the measurements array 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 if measurements does not have the same number of elements 
 * as any data already present in the dataframe 
 * 
 * source: dataset.c 
 */ 
extern unsigned short dataset_setitem_data(DATASET *ds, double *measurements, 
	char *label, unsigned long n); 

/* 
 * Performs the __setitem__ function when the user is setting an element of the 
 * observational uncertainties by column label. 
 * 
 * Parameters 
 * ========== 
 * ds: 				The dataset itself 
 * errors: 			The errors to be added to the dataset 
 * label: 			The label to attach to the quantities 
 * n: 				The number of elements in the measurements array 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 if errors does not have the same number of elements as any 
 * data already present in the dataframe 
 * 
 * source: dataset.c 
 */ 
extern unsigned short dataset_setitem_errors(DATASET *ds, double *errors, 
	char *label, unsigned long n); 

#if 0 
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

/* 
 * Copy an array of doubles into the dataset object as the error on a given 
 * measurement 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * errors: 		The errors on a given measurement (assumed to be of length 
 * 				ds.n_points) 
 * idx: 		The column number (index) to copy the errors into. This should 
 * 				be the same as the column number of the measurements themselves 
 * 				in the attribute 'data'. 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on falure. 
 * 
 * source: dataset.c 
 */ 
extern unsigned short dataset_new_error(DATASET *ds, double *errors, 
	unsigned short idx); 
#endif 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MODELING_DATASET_H */ 

