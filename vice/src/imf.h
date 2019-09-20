
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

extern void imf_add_mass_bin(IMF *imf); 

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
 * The IMF object; NULL if user_spec is not "salpter", "kroupa", or "custom" 
 * 
 * source: imf.c 
 */ 
extern IMF *imf_initialize(char *user_spec, double m_lower, double m_upper); 

/* 
 * Free up the memory stored in an IMF object. 
 * 
 * Parameters 
 * ========== 
 * imf: 		The IMF object to free up 
 * 
 * source: imf.c 
 */ 
extern void imf_free(IMF *imf); 

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
extern double imf_evaluate(IMF *imf, double m); 

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


