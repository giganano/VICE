
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
 * t: 			Stellar population age in Gyr 
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

/* 
 * Calculate main sequence turnoff mass according to the analytic form 
 * presented in Larson (1974), which is a fit to the compilation of 
 * evolutionary lifetimes presented in Tinsley (1972). 
 * 
 * Parameters 
 * ==========
 * t: 			Stellar population age in Gyr 
 * postMS: 		Ratio of a star's main sequence lifetime to its post main 
 * 				sequence lifetime. 
 * 
 * Returns 
 * =======
 * The main sequence turnoff mass calculated according to the following 
 * relation: 
 * 
 * log(t) = alpha + (beta + gamma * log(m)) * log(m) 
 * 
 * where t is measured in Gyr and m is measured in solar masses. The value of 
 * alpha quantifies the log of the main sequence lifetime of the sun, which 
 * sets the overall scaling of this relation. 
 * 
 * Notes 
 * =====
 * This function takes alpha = 1.0, beta = -3.42, and gamma = 0.88 based on 
 * Kobayashi (2004), who adopt the form from David, Forman & Jones (1990). 
 * Kobayashi (2004) uses alpha = 10.0 rather than 1.0, the difference arising 
 * due to her use of yr rather than Gyr as the time unit. 
 * 
 * References 
 * ==========
 * David, Forman & Jones (1990), ApJ, 359, 29 
 * Kobayashi (2004), MNRAS, 347, 74 
 * Larson (1974), MNRAS, 166, 585 
 * Tinsley (1972), A&A, 20, 383 
 * 
 * header: mlr.h 
 */ 
extern double Larson1974(double t, double postMS); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_MLR_H */ 

