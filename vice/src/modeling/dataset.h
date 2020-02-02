/* 
 * This is the header file for the dataset object. 
 */ 

#ifndef DATASET_H 
#define DATASET_H 

#ifdef __cpluspus 
extern "C" { 
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocates memory for and returns a pointer to a dataset object 
 * 
 * source: dataset.c 
 */ 
extern DATASET *dataset_initialize(void); 

/* 
 * Free the data stored in a dataset object. 
 * 
 * source: dataset.c 
 */ 
extern void dataset_free(DATASET *ds); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* DATASET_H */ 

