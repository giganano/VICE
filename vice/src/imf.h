
#ifndef IMF_H 
#define IMF_H 

#ifdef __cplusplus 
extern "C" {
#endif 

#include "objects.h" 
#include "utils.h" 

/* hash-code for the Kropua (2001) IMF */ 
#ifndef KROUPA 
#define KROUPA 658 
#endif /* KROUPA */ 

/* hash code for the Salpeter (1955) IMF */ 
#ifndef SALPETER 
#define SALPETER 864 
#endif /* SALPETER */

/* hash code for a custom IMF */ 
#ifndef CUSTOM 
#define CUSTOM 667 
#endif /* CUSTOM */ 

/* The maximum size for the IMF's spec char pointer */ 
#ifndef SPEC_CHARP_SIZE 
#define SPEC_CHARP_SIZE 100 
#endif /* SPEC_CHARP_SIZE */ 

/* The stepsize taken in sampling a functional IMF */ 
#ifndef IMF_STEPSIZE 
#define IMF_STEPSIZE 1e-3 
#endif /* IMF_STEPSIZE */ 

/* 
 * Allocate memory for and return a pointer to an IMF object. 
 * 
 * Parameters 
 * ========== 
 * m_lower: 	The lower mass limit on star formation 
 * m_upper: 	The upper mass limit on star formation 
 * 
 * Returns 
 * ======= 
 * The IMF object; NULL if user_spec is not "salpter", "kroupa", or "custom" 
 * 
 * source: imf.c 
 */ 
extern IMF_ *imf_initialize(double m_lower, double m_upper); 

/* 
 * Free up the memory stored in an IMF object. 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object to free up 
 * 
 * source: imf.c 
 */ 
extern void imf_free(IMF_ *imf); 

/* 
 * Set the mass distribution of the IMF. 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object to set the distribution for 
 * arr: 		The array containing the values of the distribution. This is 
 * 				assumed to be the same length as the mass array 
 * 
 * Returns 
 * ======= 
 * 1 on an unallowed value of the distribution; 0 on success 
 * 
 * source: imf.c 
 */ 
extern unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr); 

/* 
 * Determines the number of mass bins on the IMF grid. 
 * 
 * Parameters 
 * ========== 
 * imf:		The IMF object to determine the number of bins for 
 * 
 * source: imf.c 
 */ 
extern unsigned long n_mass_bins(IMF_ imf); 

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
 * source: imf.c 
 */ 
extern double imf_evaluate(IMF_ imf, double m); 

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
 * source: imf.c 
 */ 
extern double salpeter55(double m); 

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
 * source: imf.c 
 */ 
extern double kroupa01(double m); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* IMF_H */ 


