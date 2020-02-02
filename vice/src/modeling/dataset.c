/* 
 * This file implements the datasest object for the modeling package. 
 */ 

#include <stdlib.h> 
#include "dataset.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void dataset_data_free(double **arr, unsigned short n_quantities); 

/* 
 * Allocates memory for and returns a pointer to a dataset object 
 * 
 * header: dataset.h 
 */ 
extern DATASET *dataset_initialize(void) {

	DATASET *ds = (DATASET *) malloc (sizeof(DATASET)); 
	ds -> quantities = NULL; 
	ds -> errors = NULL; 
	ds -> n_quantities = 0; 
	ds -> n_errors = 0; 
	ds -> n_points = 0; 
	return ds; 

} 

/* 
 * Free the data stored in a dataset object. 
 * 
 * header: dataset.h 
 */ 
extern void dataset_free(DATASET *ds) {

	if (ds != NULL) {

		dataset_data_free(ds -> quantities, (*ds).n_quantities);  
		dataset_data_free(ds -> errors, (*ds).n_errors); 
		ds -> n_quantities = 0; 
		ds -> n_errors = 0; 
		ds -> n_points = 0; 
		free(ds); 
		ds = NULL; 

	} else {} 

}

/* 
 * Free the data stored in a 2D-pointer organized by quantity 
 * 
 * Parameters 
 * ========== 
 * arr: 			The pointer to the data 
 * n_quantities:	The number of elements in the first dimension 
 */ 
static void dataset_data_free(double **arr, unsigned short n_quantities) {

	if (arr != NULL) {
		unsigned short i; 
		for (i = 0u; i < n_quantities; i++) {
			if (arr[i] != NULL) {
				free(arr[i]); 
				arr[i] = NULL; 
			} else {} 
			free(arr); 
			arr = NULL; 
		} 
	} else {} 

}


