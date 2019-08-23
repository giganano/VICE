
#ifndef IMF_H 
#define IMF_H 

#ifdef __cplusplus 
extern "C" {
#endif 

#include "utils.h" 

/* hash-code for the Kropua (2001) IMF */ 
#ifndef KROUPA 
#define KROUPA 658 
#endif /* KROUPA */ 

/* hash code for the Salpeter (1955) IMF */ 
#ifndef SALPETER 
#define SALPETER 864 
#endif /* SALPETER */ 

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


