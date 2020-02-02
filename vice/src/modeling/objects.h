/* 
 * This header file typedefs the structs that are used by the objects in the 
 * modeling package. 
 */ 

typedef struct dataset {

	double **quantities; 
	double **errors; 
	unsigned short n_quantities; 
	unsigned short n_errors; 
	unsigned long n_points; 

} DATASET; 


