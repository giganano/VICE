
#ifndef AGB_H 
#define AGB_H 

#ifdef __cplusplus 
extern "C" {
#endif 

/* The maximum mass of a star in Msun that undergoes an AGB phase in VICE */ 
#ifndef MAX_AGB_MASS 
#define MAX_AGB_MASS 8 
#endif /* MAX_AGB_MASS */ 

/* The minimum mass of a star in Msun that undergoes an AGB phase in VICE */ 
#ifndef MIN_AGB_MASS 
#define MIN_AGB_MASS 0 
#endif /* MIN_AGB_MASS */ 

#ifndef AGB_Z_GRID_STEPSIZE 
#define AGB_Z_GRID_STEPSIZE 1e-3 
#endif /* AGB_Z_GRID_STEPSIZE */ 

#ifndef AGB_Z_GRID_MIN 
#define AGB_Z_GRID_MIN 0 
#endif /* AGB_Z_GRID_MIN */ 

#ifndef AGB_Z_GRID_MAX 
#define AGB_Z_GRID_MAX 0.5 
#endif /* AGB_Z_GRID_MAX */ 

#include "objects.h" 
#include "singlezone/agb.h" 
#include "multizone/agb.h" 
#include "objects/agb.h" 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* AGB_H */ 

