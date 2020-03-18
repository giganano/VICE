
#ifndef TESTS_OBJECTS_DATASET_H 
#define TESTS_OBJECTS_DATASET_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Test the function which constructs a dataset object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: dataset.c 
 */ 
extern unsigned short test_dataset_initialize(void); 

/* 
 * Test the function which frees the memory stored by a dataset object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: dataset.c 
 */ 
extern unsigned short test_dataset_free(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_OBJECTS_DATASET_H */ 
