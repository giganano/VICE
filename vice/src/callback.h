
#ifndef CALLBACK_H 
#define CALLBACK_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Evaluate a callback function at a given value x 
 * 
 * Parameters 
 * ========== 
 * cb1: 		The callback object 
 * x: 			The value to evaluate the function at 
 * 
 * Returns 
 * ======= 
 * f(x), where f is the function passed from python 
 * 
 * source: callback.c 
 */ 
extern double callback_1arg_evaluate(CALLBACK_1ARG cb1, double x); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* CALLBACK_H */ 

