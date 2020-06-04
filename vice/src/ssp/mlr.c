/* 
 * This file implements the stellar mass-lifetime relationship (MLR) in VICE. 
 */ 

#include <math.h> 
#include "../ssp.h" 
#include "mlr.h" 

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
 * 		main sequence lifetimes. 
 * 10 Gyr and 3.5 are values that can be changed in ssp.h  
 * 
 * header: mlr.h 
 */ 
extern double main_sequence_turnoff_mass(double t, double postMS) { 

	/* m_to = (t / ((1 + postMS) * 10 Gyr))^(-1/3.5) */ 
	return pow( 
		t / ((1 + postMS) * SOLAR_LIFETIME), 
		-1.0 / MASS_LIFETIME_PLAW_INDEX
	); 

} 


