
#ifndef TRACER_H 
#define TRACER_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocates memory for and returns a pointer to a TRACER particle. 
 * 
 * source: tracer.c 
 */ 
extern TRACER *tracer_initialize(void); 

/* 
 * Frees up the memory stored by the tracer particle. 
 * 
 * source: tracer.c 
 */ 
extern void tracer_free(TRACER *t); 

/* 
 * Injects tracer particles into a multizone object for the current timestep 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * source: tracer.c 
 */ 
extern void inject_tracers(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TRACER_H */ 

