
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

/* 
 * Determine the metallicity of a tracer particle. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * t: 		The tracer particle to determine the metallicity of 
 * 
 * Returns 
 * ======= 
 * The scaled metallicity of the tracer particle 
 * 
 * source: tracer.c 
 */ 
extern double tracer_metallicity(MULTIZONE mz, TRACER t); 

/* 
 * Allocate memory for the stellar tracer particles 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for this simulation 
 * 
 * source: tracer.c 
 */ 
extern void malloc_tracers(MULTIZONE *mz); 

/*
 * Setup the zone history of a tracer particle assuming uniform migration 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object for the current simulation 
 * t: 			A pointer to the tracer particle to setup the zone history for 
 * origin: 		The zone of origin for the tracer particle 
 * final: 		The final zone number for the tracer particle 
 * birth: 		The timestep at which the tracer particle is born 
 * 
 * Returns 
 * ======= 
 * An error code: 0 for success; 1 for a birth timestep that's too large; 
 * 2 for a zone of origin that's too large; and 3 for a final zone that's 
 * too large 
 * 
 * source: tracer.c 
 */ 
extern unsigned short setup_zone_history(MULTIZONE mz, TRACER *t, 
	unsigned long origin, unsigned long final, unsigned long birth); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TRACER_H */ 

