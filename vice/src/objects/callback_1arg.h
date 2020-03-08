
#ifndef OBJECTS_CALLBACK_H 
#define OBJECTS_CALLBACK_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a CALLBACK_1ARG object, 
 * initializing the user_func = NULL 
 * 
 * header: callback_1arg.h 
 */ 
extern CALLBACK_1ARG *callback_1arg_initialize(void); 

/* 
 * Free up the memory stored in a CALLBACK_1ARG object 
 * 
 * header: callback_1arg.h 
 */ 
extern void callback_1arg_free(CALLBACK_1ARG *cb1); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* OBJECTS_CALLBACK_H */ 

