
#ifndef TESTS_OBJECTS_MDF_H 
#define TESTS_OBJECTS_MDF_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Test the function which constructs an mdf object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: mdf.c 
 */ 
extern unsigned short test_mdf_initialize(void); 

/* 
 * Test the function which frees the memory stored in an mdf object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: mdf.c 
 */ 
extern unsigned short test_mdf_free(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_OBJECTS_MDF_H */ 
