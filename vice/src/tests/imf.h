
#ifndef TESTS_IMF_H 
#define TESTS_IMF_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cpluslpus */ 

#include "../objects.h" 

/* 
 * Test the function which sets the mass distribution 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: imf.c 
 */ 
extern unsigned short test_imf_set_mass_distribution(void); 

/* 
 * Test the function which determines the number of mass bins in an IMF object 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: imf.c 
 */ 
extern unsigned short test_n_mass_bins(void); 

/* 
 * Test the function which evaluates an IMF object at a given mass 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * source: imf.c 
 */ 
extern unsigned short test_imf_evaluate(void); 

/* 
 * Test the built-in Salpeter (1955) IMF 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * References 
 * ========== 
 * Salpeter (1955), ApJ, 121, 161 
 * 
 * source: imf.c 
 */ 
extern unsigned short test_salpeter55(void); 

/* 
 * Test the built-in Kroupa (2001) IMF 
 * 
 * Returns 
 * ======= 
 * 1 on success, 0 on failure 
 * 
 * References 
 * ========== 
 * Kroupa (2001), MNRAS, 322, 231 
 * 
 * source: imf.c 
 */ 
extern unsigned short test_kroupa01(void); 

/* 
 * Sets a custom mass distribution according to test_imf 
 * 
 * Returns 
 * ======= 
 * The value of imf_set_mass_distribution at vice/src/imf.h 
 * 
 * source: imf.c 
 */ 
extern unsigned short set_test_custom_mass_distribution(IMF_ *test); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TESTS_IMF_H */ 

