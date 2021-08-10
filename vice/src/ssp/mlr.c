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
extern double Larson1974(double t, double postMS) {

	if (t) {

		double alpha = log10(SOLAR_LIFETIME); 
		double beta = -3.42; 
		double gamma = 0.88; 

		/* 
		 * Determined via the quadratic formula in the equation above, where 
		 * the version with the minus sign is the physical answer. If the plus 
		 * sign is taken from the quadratic, then the turnoff mass increases 
		 * with time. 
		 */ 

		double logm = (
			-beta - sqrt(pow(beta, 2) - 4 * gamma * (alpha - log10(t)))
		) / (
			2 * gamma 
		); 

		return pow(10, logm); 

	} else {
		#ifdef INFINITY 
			return INFINITY; 
		#else 
			return 500; 
		#endif 
	}

}

