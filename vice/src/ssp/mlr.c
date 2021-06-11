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
 * Versions >= 1.2.1: This function handles errors more robustly in the event 
 * 		that the age is either zero or negative. For zero age, it returns 
 * 		INFINITY (500 if not defined), and for negative age, it returns NAN 
 * 		(0 if not defined). 
 * 10 Gyr and 3.5 are values that can be changed in ssp.h 
 * 
 * header: mlr.h 
 */ 
extern double main_sequence_turnoff_mass(double t, double postMS) { 

	if (t > 0) {
		/* m_to = (t / ((1 + postMS) * 10 Gyr))^(-1/3.5) */ 
		return pow( 
			t / ((1 + postMS) * SOLAR_LIFETIME), 
			-1.0 / MASS_LIFETIME_PLAW_INDEX
		); 
	} else if (t < 0) { 
		/* 
		 * There was an error somewhere. This function shouldn't ever receive 
		 * a negative age as that's unphysical. 
		 */ 
		#ifdef NAN 
			return NAN; 
		#else 
			return 0; 
		#endif 
	} else { 
		/* 
		 * Stellar population has zero age, meaning no stars have died yet. 
		 * Return infinity if its defined, and if not, a sufficiently high 
		 * mass that it's above most IMF upper bounds anyway. 
		 */ 
		#ifdef INFINITY 
			return INFINITY; 
		#else 
			return 500; 
		#endif 
	}

} 


