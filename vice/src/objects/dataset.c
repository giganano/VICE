/* 
 * This file implements memory management for the dataset object 
 */ 

#include <stdlib.h> 
#include "dataset.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static void dataset_data_free(double **data, unsigned long n_rows, 
	unsigned short n_cols); 


/* 
 * Allocate memory for and return a pointer to a dataset object 
 * 
 * header: dataset.h 
 */ 
extern DATASET *dataset_initialize(void) {

	DATASET *ds = (DATASET *) malloc (sizeof(DATASET)); 
	ds -> data = NULL; 
	ds -> errors = NULL; 
	ds -> inv_cov = NULL; 
	ds -> predictions = NULL; 
	ds -> labels = NULL; 
	ds -> n_quantities = 0u; 
	ds -> n_points = 0ul; 
	return ds; 

} 


/* 
 * Free the memory stored in a dataset object 
 * 
 * header: dataset.h 
 */ 
extern void dataset_free(DATASET *ds) {

	if (ds != NULL) { 

		dataset_reset(ds); 
		free(ds); 
		ds = NULL; 

	} else {} 

} 


/* 
 * Clear all of the memory stored in a dataset object, but leave it intact so 
 * that it may store new data 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object to reset 
 * 
 * header: dataset.h 
 */ 
extern void dataset_reset(DATASET *ds) {

	if (ds != NULL) { 

		dataset_data_free(ds -> data, (*ds).n_points, (*ds).n_quantities); 
		dataset_data_free(ds -> errors, (*ds).n_points, (*ds).n_quantities); 
		dataset_data_free(ds -> inv_cov, (*ds).n_quantities, (*ds).n_quantities); 
		dataset_data_free(ds -> predictions, (*ds).n_points, (*ds).n_quantities); 

		if ((*ds).labels != NULL) { 
			unsigned short i; 
			for (i = 0u; i < (*ds).n_quantities; i++) { 
				if ((*ds).labels[i] != NULL) {
					free(ds -> labels[i]); 
					ds -> labels[i] = NULL; 
				} else {} 
			} 
			free(ds -> labels); 
			ds -> labels = NULL; 
		} else {} 

		ds -> n_quantities = 0u; 
		ds -> n_points = 0ul; 

	}

}


/* 
 * Free up the memory stored in a double pointer in a dataset object 
 * 
 * Parameters 
 * ========== 
 * data: 		The data itself 
 * n_rows: 		The number of rows in the table 
 * n_cols: 		The number of columns in the table 
 */ 
static void dataset_data_free(double **data, unsigned long n_rows, 
	unsigned short n_cols) {

	if (data != NULL) {
		unsigned long i; 
		for (i = 0ul; i < n_rows; i++) {
			if (data[i] != NULL) {
				free(data[i]); 
				data[i] = NULL; 
			} else {} 
		} 
		free(data); 
		data = NULL; 		
	}

}

