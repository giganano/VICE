
#ifndef TESTS_OBJECTS_SINGLEZONE_H 
#define TESTS_OBJECTS_SINGLEZONE_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Test the function which constructs a singlezone object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short test_singlezone_initialize(void); 

/* 
 * Test the function which frees the memory stored by a singlezone object. 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: singlezone.c 
 */ 
extern unsigned short test_singlezone_free(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_OBJECTS_SINGLEZONE_H */ 
