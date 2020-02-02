
#ifndef CHANNEL_H 
#define CHANNEL_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cpluslus */ 

#ifndef CHANNEL_YIELD_GRID_STEP 
#define CHANNEL_YIELD_GRID_STEP 1e-5 
#endif /* CHANNEL_YIELD_STEP */ 

#ifndef CHANNEL_YIELD_GRID_MIN 
#define CHANNEL_YIELD_GRID_MIN 0 
#endif /* CHANNEL_YIELD_GRID_MIN */ 

#ifndef CHANNEL_YIELD_GRID_MAX 
#define CHANNEL_YIELD_GRID_MAX 0.5 
#endif /* CHANNEL_YIELD_GRID_MAX */ 

#include "objects.h" 
#include "singlezone/channel.h" 
#include "multizone/channel.h" 
#include "objects/channel.h" 

#ifdef __cpluslus 
} 
#endif /* __cplusplus */ 

#endif /* CHANNEL_H */ 



