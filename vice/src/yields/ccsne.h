
#ifndef YIELDS_CCSNE_H 
#define YIELDS_CCSNE_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Determine the value of the integrated IMF weighted by the mass yield of a 
 * given element, up to the normalization of the IMF. 
 * 
 * Parameters 
 * ========== 
 * intgrl: 		The integral object for the numerator of the yield 
 * imf:			The associated IMF object 
 * file:		The nme of the data file containing the grid
 * 
 * Returns 
 * ======= 
 * The mass yield from all CCSNe in a stellar population as predicted by the 
 * built-in yields, up to the normalization of the IMF. 
 * 
 * source: ccsne.c 
 */ 
extern unsigned short IMFintegrated_fractional_yield_numerator(
	INTEGRAL *intgrl, IMF_ *imf, char *file); 

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

