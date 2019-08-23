
#ifndef SNEIA_H 
#define SNEIA_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

/* power-law index of built-in SNe Ia DTD */ 
#ifndef PLAW_DTD_INDEX 
#define PLAW_DTD_INDEX 1.1 
#endif /* PLAW_DTD_INDEX */ 

/* The time up to which the RIa DTD is evaluated */ 
#ifndef RIA_MAX_EVAL_TIME 
#define RIA_MAX_EVAL_TIME 15.0 
#endif /* RIA_MAX_EVAL_TIME */ 

/* hash-code for exp-mode */ 
#ifndef EXP 
#define EXP 333 
#endif /* EXP */ 

/* hash-code for plaw-mode */ 
#ifndef PLAW 
#define PLAW 436 
#endif /* PLAW */ 

/* hash-code for custom DTD */ 
#ifndef CUSTOM 
#define CUSTOM 667 
#endif /* CUSTOM */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a SNEIA_YIELD_SPECS struct. 
 * Automatically initializes RIa to NULL. Allocates memory for a 100-character 
 * dtd char * specifier. 
 * 
 * header: sneia.h 
 */ 
extern SNEIA_YIELD_SPECS *sneia_yield_initialize(void); 

/* 
 * Free up the memory stored in a SNEIA_YIELD_SPECS struct. 
 * 
 * header: sneia.h 
 */ 
extern void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yields); 

/* 
 * Determine the rate of mass enrichment of a given element at the current 
 * timestep from SNe Ia. See section 4.3 of VICE's science documentation for 
 * further details. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * e: 		The element to find the rate of mass enrichment for 
 * 
 * Returns 
 * ======= 
 * The time-derivative of the type Ia supernovae mass enrichment term 
 * 
 * source: sneia.c 
 */ 
extern double mdot_sneia(SINGLEZONE sz, ELEMENT e); 

/* 
 * Enrich each element in each zone according to the SNe Ia associated with 
 * tracer particles. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object for the current simulation 
 * 
 * source: sneia.c 
 */ 
extern void sneia_from_tracers(MULTIZONE *mz); 

/* 
 * Setup the SNe Ia rate in preparation for a singlezone simulation. 
 * 
 * Parameters 
 * ========== 
 * sz: 		A pointer to the singlezone object that is about to be ran 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: sneia.c 
 */ 
extern unsigned short setup_RIa(SINGLEZONE *sz); 

/* 
 * Normalize the SNe Ia delay-time distribution once it is set according to 
 * an arbitrary normalization. 
 * 
 * Parameters 
 * ========== 
 * e: 			The ELEMENT struct to normalize the DTD for 
 * length: 		The length of the e -> sneia_yields -> RIa array 
 * 
 * source: sneia.c 
 */ 
extern void normalize_RIa(ELEMENT *e, unsigned long length); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SNEIA_H */ 


