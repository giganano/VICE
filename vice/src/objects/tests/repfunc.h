
#ifndef OBJECTS_TESTS_REPFUNC_H 
#define OBJECTS_TESTS_REPFUNC_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

/* 
 * Tests the memory allocation routine for the repfunc object. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: repfunc.c 
 */ 
extern unsigned short test_repfunc_initialize(void); 

/* 
 * Test the function which frees the memory stored by a repfunc object. 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: repfunc.c 
 */ 
extern unsigned short test_repfunc_free(void); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* OBJECTS_TESTS_REPFUNC_H */ 
