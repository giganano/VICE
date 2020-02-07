/* 
 * This file implements memory management for the dataset object 
 */ 

#include <stdlib.h> 
#include "dataset.h" 

/* 
 * Allocate memory for and return a pointer to a dataset object 
 * 
 * header: dataset.h 
 */ 
extern DATASET *dataset_initialize(void) {

	DATASET *ds = (DATASET *) malloc (sizeof(DATASET)); 
	ds -> data = NULL; 
	ds -> predictions = NULL; 
	ds -> n_quantities = 0u; 
	ds -> n_points = 0ul; 

} 


/* 
 * Free the memory stored in a dataset object 
 * 
 * header: dataset.h 
 */ 
extern void dataset_free(DATASET *ds) {

	if (ds != NULL) {

		if ((*ds).data != NULL) {
			unsigned long i; 
			for (i = 0ul; i < (*ds).n_points; i++) { 
				if ((*ds).data[i] != NULL) {
					free(ds -> data[i]); 
					ds -> data[i] = NULL;
				} else {} 
			} 
			free(ds -> data); 
			ds -> data = NULL; 
		} else {} 

		if ((*ds).predictions != NULL) {
			unsigned long i; 
			for (i = 0ul; i < (*ds).n_points; i++) { 
				if ((*ds).predictions[i] != NULL) { 
					free(ds -> predictions[i]); 
					ds -> predictions[i] = NULL; 
				} else {} 
			} 
			free(ds -> predictions); 
			ds -> predictions = NULL; 
		} else {} 

		ds -> n_quantities = 0u; 
		ds -> n_points = 0ul; 
		free(ds); 
		ds = NULL; 

	} else {} 

}

