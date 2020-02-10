/* 
 * This file implements the datasest object for the modeling package. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "likelihood.h" 
#include "dataset.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double *dataset_getitem_common(DATASET ds, double **qtys, char *label); 
static unsigned short dataset_setitem_common(DATASET *ds, double **qtys, 
	double **other, double *arr, char *label, unsigned long n); 
static void append_column_nans(double **data, unsigned long n, 
	unsigned short dimension); 
static short dataset_column_number(DATASET ds, char *label); 
static void dataset_new_label(DATASET *ds, char *label); 


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
 * header: dataset.h 
 */ 
extern double *dataset_getitem_data(DATASET ds, char *label) {

	return dataset_getitem_common(ds, ds.data, label); 

} 


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
 * header: dataset.h 
 */ 
extern double *dataset_getitem_errors(DATASET ds, char *label) {

	return dataset_getitem_common(ds, ds.errors, label); 

}


/* 
 * Performs the __getitem__ function on either the observational measurements 
 * or the associated uncertainties, depending on the user's command 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * qtys: 		The quantities to pull measurements from (either data or errors) 
 * label: 		The label associated with the given quantity 
 * 
 * Returns 
 * ======= 
 * The column of the qtys table with the associated label. NULL if the label is 
 * not recognized 
 */ 
static double *dataset_getitem_common(DATASET ds, double **qtys, char *label) {

	unsigned long i; 
	short idx = dataset_column_number(ds, label); 
	double *column; 
	switch (idx) {

		case -1: 
			/* error handling */ 
			return NULL; 

		default: 
			column = (double *) malloc (ds.n_points * sizeof(double)); 
			for (i = 0ul; i < ds.n_points; i++) {
				column[i] = qtys[i][idx]; 
			} 
			return column; 

	}

}


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
 * header: dataset.h 
 */ 
extern unsigned short dataset_setitem_data(DATASET *ds, double *measurements, 
	char *label, unsigned long n) {

	return dataset_setitem_common(ds, ds -> data, ds -> errors, measurements, 
		label, n); 

} 


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
 * header: dataset.h 
 */ 
extern unsigned short dataset_setitem_errors(DATASET *ds, double *errors, 
	char *label, unsigned long n) {

	return dataset_setitem_common(ds, ds -> errors, ds -> data, errors, 
		label, n); 

} 


/* 
 * Performs the __setitem__ function when the user is setting either an element 
 * of the observed data or the associated uncertainty. 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object to put the data in 
 * qtys: 		The table within the dataset object to copy the data to 
 * other: 		The table within the dataset object to append a column of NaNs 
 * 				to, if necessary 
 * arr: 		The quantities to add to the dataframe themselves 
 * label: 		The label attached to this quantity 
 * n: 			The number of elements in the array arr 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 if the array does not have the same number of elements as 
 * any data already present in the dataframe 
 */ 
static unsigned short dataset_setitem_common(DATASET *ds, double **qtys, 
	double **other, double *arr, char *label, unsigned long n) {

	if ((*ds).n_quantities) {
		/* 
		 * Quantities already added to the dataset. Force the new column to have 
		 * the same number of measurements as those already added. 
		 */ 
		if (n == (*ds).n_points) {
			unsigned long i; 
			short idx = dataset_column_number(*ds, label); 
			switch (idx) {

				case -1: 
					dataset_new_label(ds, label); 
					for (i = 0ul; i < (*ds).n_points; i++) {
						qtys[i] = (double *) realloc (qtys[i], 
							((*ds).n_quantities + 1u) * sizeof(double)); 
						qtys[i][(*ds).n_quantities] = arr[i]; 
					} 
					append_column_nans(other, n, (*ds).n_quantities); 
					ds -> n_quantities++; 
					return 0u; 

				default: 
					for (i = 0u; i < (*ds).n_points; i++) {
						qtys[i][idx] = arr[i]; 
					} 
					return 0u; 

			} 
		} else {
			return 1u; 
		} 

	} else {
		/* 
		 * No quantities yet, just take the measurements. Start a table with 1 
		 * column, adding columns when more quantities are added. 
		 */ 
		unsigned long i; 
		qtys = (double **) malloc (n * sizeof(double *)); 
		for (i = 0ul; i < n; i++) {
			qtys[i] = (double *) malloc (sizeof(double)); 
			qtys[i][0] = arr[i]; 
		} 
		append_column_nans(other, n, (*ds).n_quantities); 
		ds -> n_points = n; 
		ds -> n_quantities = 1ul; 
		return 0u; 
	}

}


/* 
 * Append a column of NANs to a 2D array of doubles 
 * 
 * Parameters 
 * ========== 
 * data: 		The data table itself 
 * n: 			The number of elements in the array (along first axis) 
 * dimension: 	The CURRENT number of columns in the array (along second axis) 
 */ 
static void append_column_nans(double **data, unsigned long n, 
	unsigned short dimension) { 

	if (data == NULL) { 
		dimension = 0u; 
		data = (double **) malloc (n * sizeof(double *)); 
	} else {} 

	unsigned long i; 
	for (i = 0ul; i < n; i++) { 
		data[i] = (double *) realloc (data[i], 
			(dimension + 1u) * sizeof(double)); 
		data[i][dimension] = NAN; 
	} 

} 


/* 
 * Obtain the column number of a quantity in the dataset from its string label 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * label: 		The column label 
 * 
 * Returns 
 * ======= 
 * The column number of the data with that label. -1 if it is not found in the 
 * dataframe. 
 */ 
static short dataset_column_number(DATASET ds, char *label) { 

	short i; 
	for (i = 0; i < ds.n_quantities; i++) { 
		if (!strcmp(ds.labels[i], label)) return i; 
	} 
	return -1; 

}


/* 
 * Create a new label within the dataset object 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object 
 * label: 		The label to add to the dataframe 
 */ 
static void dataset_new_label(DATASET *ds, char *label) { 

	switch (dataset_column_number(*ds, label)) { 

		case -1: 
			ds -> labels = (char **) realloc (ds -> labels, 
				((*ds).n_quantities + 1u) * sizeof(char *)); 
			ds -> labels[(*ds).n_quantities] = (char *) realloc (
				ds -> labels[(*ds).n_quantities], strlen(label) * sizeof(char)); 
			strcpy(ds -> labels[(*ds).n_quantities], label); 
			break; 

		default: 
			break; 

	} 

} 

