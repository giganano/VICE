
#ifndef YIELDS_CCSNE_H 
#define YIELDS_CCSNE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Set the global testing status. 
 * 
 * Parameters 
 * ========== 
 * testing: 	A boolean int describing whether or not testing is being ran. 
 * 
 * header: ccsne.h 
 */ 
extern void set_testing_status(unsigned short testing); 

/* 
 * Weight the initial composition of each star by explodability. This ensures 
 * that net yields are not reported as negative when the study did not 
 * separate wind and explosive yields. 
 * 
 * Parameters 
 * ==========
 * 1 to weight the initial composition by explodability, 0 to not. 
 * 
 * source: ccsne.c 
 */ 
extern void weight_initial_by_explodability(unsigned short weight); 

/* 
 * Set the value of the progenitor stars abundance by mass Z_x for the element 
 * x whose net yield is being calculated. 
 * 
 * Parameters 
 * ==========
 * Z: 		The initial abundance Z_x itself 
 * 
 * source: ccsne.c 
 */ 
extern void set_Z_progenitor(double Z); 

/* 
 * Calculate an IMF integrated fractional yield by sampling the IMF and 
 * summing up the yields and ZAMS masses as opposed to analytically 
 * evaluating the solution. 
 * 
 * Parameters 
 * ==========
 * N: 				The number of stars to sample from the IMF 
 * m_lower: 		The lower mass limit on star formation in Msun 
 * m_upper: 		The upper mass limit on star formation in Msun 
 * imf: 			The associated IMF object 
 * explodability: 	Stellar explodability as a function of mass 
 * path: 			The name of the data file containing the grid 
 * wind: 			Boolean int describing whether or not to include winds 
 * element: 		The symbol of the element 
 * 
 * Returns 
 * =======
 * The value of the IMF integrated fractional yield via stochastic sampling. 
 * 
 * source: ccsne.c 
 */ 
extern double IMFintegrated_fractional_yield_sampled(const unsigned long N, 
	double m_lower, double m_upper, IMF_ *imf, CALLBACK_1ARG *explodability, 
	char *path, const unsigned short wind, char *element); 

/* 
 * Determine the value of the integrated IMF weighted by the mass yield of a 
 * given element, up to the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 			The integral object for the numerator of the yield 
 * imf:				The associated IMF object
 * explodability: 	Stellar explodability as a function of mass 
 * path:			The nme of the data file containing the grid 
 * wind: 			Boolean int describing whether or not to include winds 
 * element: 		The symbol of the element 
 * 
 * Returns 
 * ======= 
 * 3 on an unrecognized IMF, otherwise the value returned by quad (see 
 * quadrature.h). 
 * 
 * source: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_numerator(
	INTEGRAL *intgrl, IMF_ *imf, CALLBACK_1ARG *explodability, 
	char *path, const unsigned short wind, char *element); 

/* 
 * Determine the value of the integrated IMF weighted by stellar mass, up to 
 * the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 		The integral object for the denominator of the yield 
 * imf:			The associated IMF object 
 * 
 * Returns 
 * ======= 
 * 3 on an unrecognized IMF, otherwise the value returned by quad (see 
 * quadrature.h) 
 * 
 * source: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_denominator(
	INTEGRAL *intgrl, IMF_ *imf); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* YIELDS_CCSNE_H */ 

