
#ifndef OBJECTS_REPFUNC_H 
#define OBJECTS_REPFUNC_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a repfunc object. The number of 
 * points is automatically set to 0 and the coordinates to NULL. 
 * 
 * source: repfunc.c 
 */ 
extern REPFUNC *repfunc_initialize(void); 

/* 
 * Free up the memory stored in a repfunc object. 
 * 
 * source: repfunc.c 
 */ 
extern void repfunc_free(REPFUNC *rpf); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* OBJECTS_REPFUNC_H */ 
