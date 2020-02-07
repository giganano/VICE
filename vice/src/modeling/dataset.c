/* 
 * This file implements the datasest object for the modeling package. 
 */ 

#include <stdlib.h> 
#include "likelihood.h" 
#include "dataset.h" 


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
 * header: dataset.h 
 */ 
extern double dataset_assess_model_predictions(DATASET *ds) { 

	if ((*ds).predictions != NULL && (*ds).data != NULL) { 
		if ((*ds).inv_cov == NULL) dataset_covariance(ds); 
		if ((*ds).inv_cov == NULL) return -1; 
		return chi_squared_likelihood((*ds).inv_cov, (*ds).data, 
			(*ds).predictions, (*ds).n_quantities, (*ds).n_points); 
	} else { 
		return -1; 
	} 

} 


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
 * header: dataset.h 
 */ 
extern void dataset_covariance(DATASET *ds) {

	if ((*ds).inv_cov != NULL) {
		unsigned long i; 
		for (i = 0ul; i < (*ds).n_quantities; i++) {
			if ((*ds).inv_cov[i] != NULL) {
				free(ds -> inv_cov[i]); 
				ds -> inv_cov[i] = NULL; 
			} else {} 
		} 
		free(ds -> inv_cov); 
		ds -> inv_cov = NULL; 
	} else {} 

	/* Do nothing if there's no data yet */ 
	if ((*ds).n_quantities) { 
		ds -> inv_cov = inverse_covariance_matrix((*ds).data, 
			(*ds).n_quantities, (*ds).n_points); 
	} else {} 
		
}


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
 * header: dataset.h 
 */ 
extern unsigned short dataset_new_quantity(DATASET *ds, double *measurements, 
	unsigned long n) {

	if ((*ds).n_quantities) { 
		/* 
		 * Quantities already added to the dataset. Force the new column to 
		 * have the same number of measurements as those already added. 
		 */ 
		if (n == (*ds).n_points) {
			unsigned long i; 
			for (i = 0ul; i < n; i++) {
				ds -> data[i] = (double *) realloc (ds -> data[i], 
					((*ds).n_quantities + 1u) * sizeof(double)); 
				ds -> data[i][(*ds).n_quantities] = measurements[i]; 
			} 
			ds -> n_quantities++; 
			return 0u; 
		} else { 
			/* do nothing and return 1 for error handling */ 
			return 1u; 
		} 

	} else {
		/* 
		 * no quantities yet, just take the data. Start a table with 1 
		 * column, adding columns when more quantities are added. 
		 */ 
		unsigned long i; 
		ds -> data = (double **) malloc (n * sizeof(double *)); 
		for (i = 0ul; i < n; i++) {
			ds -> data[i] = (double *) malloc (sizeof(double)); 
			ds -> data[i][0] = measurements[i]; 
		} 
		ds -> n_points = n; 
		ds -> n_quantities = 1ul; 
		return 0u; 
	} 

}

