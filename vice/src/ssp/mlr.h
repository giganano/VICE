
#ifndef SSP_MLR_H 
#define SSP_MLR_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Determine the main sequence turnoff mass in solar masses of a single 
 * stellar population at a time t in Gyr following their formation. 
 * 
 * Parameters 
 * ========== 
 * t: 			Time in Gyr 
 * postMS: 		Ratio of a star's post main sequence lifetime to its main 
 * 				sequence lifetime 
 * 
 * Returns 
 * ======= 
 * Main sequence turnoff mass in solar masses via 
 * (t / (1 + postMS)(10 Gyr))^(-1/3.5) 
 * 
 * Notes 
 * ===== 
 * Versions >= 1.1: This is the mass of a dying star taking into account their 
 * 		post main sequence lifetimes. 
 * 10 Gyr and 3.5 are values that can be changed in ssp.h  
 * 
 * source: mlr.c 
 */ 
extern double main_sequence_turnoff_mass(double t, double postMS); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_MLR_H */ 

