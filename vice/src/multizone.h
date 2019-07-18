
#ifndef MULTIZONE_H 
#define MULTIZONE_H 

#ifdef __cplusplus 
extern "C"{
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocates memory for and returns a pointer to a multizone object 
 * 
 * source: multizone.c 
 */ 
extern MULTIZONE *multizone_initialize(void); 

/*
 * Frees the memory stored in a multizone object 
 * 
 * source: multizone.c 
 */ 
extern void multizone_free(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MULTIZONE_H */ 



