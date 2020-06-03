
#ifndef OBJECTS_DATASET_H 
#define OBJECTS_DATASET_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a dataset object 
 * 
 * source: dataset.c 
 */ 
extern DATASET *dataset_initialize(void); 

/* 
 * Free the memory stored in a dataset object 
 * 
 * source: dataset.c 
 */ 
extern void dataset_free(DATASET *ds); 

/* 
 * Clear all of the memory stored in a dataset object, but leave it intact so 
 * that it may store new data 
 * 
 * Parameters 
 * ========== 
 * ds: 			The dataset object to reset 
 * 
 * source: dataset.c 
 */ 
extern void dataset_reset(DATASET *ds); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* OBJECTS_DATASET_H */ 

