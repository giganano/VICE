
#ifndef CCSNE_H 
#define CCSNE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#ifndef CC_YIELD_STEP 
#define CC_YIELD_STEP 1e-5 
#endif /* CC_YIELD_STEP */ 

#ifndef CC_YIELD_GRID_MIN 
#define CC_YIELD_GRID_MIN 0 
#endif /* CC_YIELD_GRID_MIN */ 

#ifndef CC_YIELD_GRID_MAX 
#define CC_YIELD_GRID_MAX 0.5 
#endif /* CC_YIELD_GRID_MAX */ 

/* minimum mass of a star for a CCSN in VICE */ 
#ifndef CC_MIN_STELLAR_MASS 
#define CC_MIN_STELLAR_MASS 8 
#endif /* CC_MIN_STELLAR_MASS */ 

#include "objects.h" 
#include "objects/ccsne.h" 
#include "singlezone/ccsne.h" 
#include "yields/ccsne.h" 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* CCSNE_H */ 

