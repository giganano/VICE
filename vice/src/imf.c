/* 
 * This file implements stellar initial mass functions (IMFs). 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <ctype.h> 
#include <math.h> 
#include "imf.h" 

/* ---------- static function comment headers not duplicated here ---------- */
// static void imf_add_mass_bin(IMF *imf); 

/* 
 * Allocate memory for and return a pointer to an IMF object. 
 * 
 * Parameters 
 * ========== 
 * user_spec: 	A string denoting which IMF to adopt, or "custom" in the case 
 * 				of user-specifications 
 * m_lower: 	The lower mass limit on star formation 
 * m_upper: 	The upper mass limit on star formation 
 * 
 * Returns 
 * ======= 
 * The IMF object; NULL if user_spec is not "salpeter", "kroupa", or "custom" 
 * 
 * header: imf.h 
 */ 
extern IMF *imf_initialize(char *user_spec, double m_lower, double m_upper) {

	/* 
	 * Allocate memory, copy the specification and the lower and upper mass 
	 * limits over. 
	 */ 
	IMF *imf = (IMF *) malloc (sizeof(IMF)); 
	imf -> spec = (char *) malloc (SPEC_CHARP_SIZE * sizeof(char)); 
	unsigned int i; 
	for (i = 0; i < strlen(user_spec); i++) {
		imf -> spec[i] = user_spec[i]; 
	} 
	imf -> spec[strlen(user_spec)] = '\0'; 
	imf -> m_lower = m_lower; 
	imf -> m_upper = m_upper; 

	/* 
	 * There will always be at least 2 elements on the mass bin and at least 
	 * one power law index 
	 */
	imf -> mass_bins = (double *) malloc (2 * sizeof(double)); 
	imf -> power_law_indeces = (double *) malloc (sizeof(double)); 
	imf -> mass_bins[0] = m_lower; 
	imf -> mass_bins[1] = m_upper;  
	imf -> n_bins = 1; 

	/* Set the mass bins based on the user specification */ 
	switch(checksum((*imf).spec)) {

		case SALPETER: /* Salpter IMF -> easy */ 
			imf -> power_law_indeces[0] = 2.35; 
			break; 

		case KROUPA: /* Kroupa IMF -> hard b/c piecewise */ 

			if (m_lower < 0.08) { 
				imf -> power_law_indeces[0] = 0.3; 
				if (m_upper > 0.08) { /* extend to m > 0.08, \propto m^-1.3 */ 
					imf_add_mass_bin(imf); 
					imf -> mass_bins[1] = 0.08; 
					imf -> power_law_indeces[1] = 1.3; 
				} else {
					break; 
				} 
				if (m_upper > 0.5) { /* extend to m > 0.5, \propto m^-2.3 */ 
					imf_add_mass_bin(imf); 
					imf -> mass_bins[2] = 0.5; 
					imf -> power_law_indeces[2] = 2.3; 
				} else {} 
				break; 
			
			} else if (0.08 <= m_lower && m_lower < 0.5) {
				imf -> power_law_indeces[0] = 1.3; 
				if (m_upper > 0.5) { /* extend to m > 0.5, \propto m^-2.3 */ 
					imf_add_mass_bin(imf); 
					imf -> mass_bins[1] = 0.5; 
					imf -> power_law_indeces[1] = 2.3; 
				} else {} 
				break; 

			} else {
				imf -> power_law_indeces[0] = 2.3; 
				break; 
			} 

		case CUSTOM: /* user-customized IMF */ 
			imf -> power_law_indeces[0] = 2.3; 	/* dummy value */ 
			break; 

		default: /* error handling */ 
			imf_free(imf); 
			return NULL; 

	}

	return imf; 

} 

/* 
 * Add a mass bin to the IMF specifications by reallocating memory 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object 
 */ 
extern void imf_add_mass_bin(IMF *imf) {

	imf -> n_bins++; 
	imf -> mass_bins = (double *) realloc (imf -> mass_bins, 
		((*imf).n_bins + 1l) * sizeof(double)); 
	imf -> power_law_indeces = (double *) realloc (imf -> power_law_indeces, 
		(*imf).n_bins * sizeof(double)); 
	imf -> mass_bins[(*imf).n_bins] = (*imf).m_upper; 

}

/* 
 * Free up the memory stored in an IMF object. 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object to free up 
 * 
 * header: imf.h 
 */ 
extern void imf_free(IMF *imf) {

	if (imf != NULL) {

		if ((*imf).spec != NULL) {
			free(imf -> spec); 
			imf -> spec = NULL; 	
		} else {} 

		if ((*imf).mass_bins != NULL) {
			free(imf -> mass_bins); 
			imf -> mass_bins = NULL; 
		} else {} 

		if ((*imf).power_law_indeces != NULL) {
			free(imf -> power_law_indeces); 
			imf -> power_law_indeces = NULL;
		} else {} 

		free(imf); 
		imf = NULL; 

	} else {} 

} 

/* 
 * Evaluate the IMF to an arbitrary normalization at the mass m 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object containing the parameters 
 * m: 			The stellar mass to evaluate the IMF at 
 * 
 * Returns 
 * ======= 
 * The un-normalized height of the IMF at that stellar mass 
 * 
 * header: imf.h 
 */ 
extern double imf_evaluate(IMF *imf, double m) {

	/* Get the bin number of the stellar mass */ 
	long bin = get_bin_number((*imf).mass_bins, (*imf).n_bins, m); 
	if (bin != -1l) { 

		/* 
		 * Take into account prefactors on the IMF to ensure that the 
		 * distribution is continuous. This simply divides the mass at the 
		 * boundary raised to the power law index on one side by that on 
		 * the other. 
		 */ 
		unsigned long i; 
		double prefactor = 1.0; 
		for (i = 0l; i < (unsigned) bin; i++) { 
			prefactor *= pow((*imf).mass_bins[bin], 
				(*imf).power_law_indeces[i + 1l] - (*imf).power_law_indeces[i]); 
		} 
		return prefactor * pow(m, -(*imf).power_law_indeces[bin]); 

	} else {
		/* Mass not on the IMF */ 
		return 0; 
	}

}

/* 
 * The Salpeter (1955) stellar initial mass function (IMF) up to a 
 * normalization constant. 
 * 
 * Parameters 
 * ========== 
 * m: 			The stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the IMF at that mass up to the normalization of the IMF. 
 * -1 if m < 0. 
 * 
 * References 
 * ========== 
 * Salpeter (1955), ApJ, 121, 161 
 * 
 * header: imf.h  
 */ 
extern double salpeter55(double m) { 

	if (m > 0) {
		return pow(m, -2.35); 
	} else {
		return -1; 
	}

} 

/* 
 * The Kroupa (2001) stellar initial mass function (IMF) up to a 
 * normalization constant. 
 * 
 * Parameters 
 * ========== 
 * m: 			The stellar mass in Msun 
 * 
 * Returns 
 * ======= 
 * The value of the IMF at that mass up to the normalization of the IMF. 
 * -1 if m < 0. 
 * 
 * References 
 * ========== 
 * Kroupa (2001), MNRAS, 322, 231 
 * 
 * header: imf.h 
 */ 
extern double kroupa01(double m) {

	if (0 < m && m < 0.08) {
		return pow(m, -0.3); 
	} else if (0.08 <= m && m <= 0.5) {
		/* 
		 * Need to make sure kroupa01(0.08) = kroupa01(0.0799999999...) 
		 * 
		 * Xm^-1.3 = m^-0.3 at m = 0.08 => X = 0.08 
		 */ 
		return 0.08 * pow(m, -1.3); 
	} else if (m > 0.5) {
		/* 
		 * Need to make sure kroupa01(0.5) = kroupa01(0.49999999....) 
		 * 
		 * Ym^-2.3 = Xm^-1.3 at m = 0.05 => Y = 0.08(0.5) = 0.04 
		 */ 
		return 0.04 * pow(m, -2.3); 
	} else {
		/* m < 0, return -1 for ValueError */ 
		return -1; 
	}

}


