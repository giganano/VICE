
#ifndef MIGRATION_H 
#define MIGRATION_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Migrates all gas, elements, and tracer particles between zones at the 
 * current timestep. 
 * 
 * Parameters 
 * ========== 
 * mz: 		A pointer to the multizone object for the current simulation 
 * 
 * source: migration.c 
 */ 
extern void migrate(MULTIZONE *mz); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* MIGRATION_H */ 

