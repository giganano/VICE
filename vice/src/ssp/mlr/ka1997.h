
#ifndef SSP_MLR_KA1997_H 
#define SSP_MLR_KA1997_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../../objects.h" 

/* 
 * Compute the mass of dying stars in a star cluster of known age according to 
 * the stellar evolution models of Kodama & Arimoto (1997). 
 * 
 * Parameters 
 * ==========
 * time: 		The age of the stellar population in Gyr. 
 * postMS: 		The ratio of a star's post main sequence lifetime to its main 
 * 				sequence lifetime. Zero for the main sequence lifetime only. 
 * Z: 			The metallicity by mass of the star. 
 * 
 * Notes 
 * =====
 * Although the lifetimes are computed analytically by a 2-D interpolation 
 * scheme, such a formalism is not analytically intertible. This solution is 
 * thus computed numerically using the bisection method (header file: root.h). 
 * 
 * Returns 
 * =======
 * The mass of the stars dying at that time in solar masses. 
 * 
 * References 
 * ========== 
 * Kodama & Arimoto (1997), A&A, 320, 41 
 * 
 * source: ka1997.c 
 */ 
extern double ka1997_turnoffmass(double time, double postMS, double Z); 

/* 
 * Compute the lifetime of a star of known mass according to the stellar 
 * evolution models of Kodama & Arimoto (1997). 
 * 
 * Parameters 
 * ==========
 * mass: 		The mass of the star in solar masses. 
 * postMS: 		The ratio of a star's post main sequence lifetime to its main 
 * 				sequence lifetime. Zero for the main sequence lifetime only. 
 * Z: 			The metallicity by mass of the star. 
 * 
 * Returns 
 * =======
 * The lifetime of the star in Gyr. 
 * 
 * References 
 * ==========
 * Kodama & Arimoto (1997), A&A, 320, 41 
 * 
 * source: ka1997.c 
 */ 
extern double ka1997_lifetime(double mass, double postMS, double Z); 

/* 
 * Import the Kodama & Arimoto (1997) data into a 2-dimension interpolation 
 * scheme. This function must be called from python before ka1997_lifetime or 
 * ka1997_turnoffmass can be called, otherwise a segmentation fault will occur. 
 * 
 * Parameters 
 * ==========
 * filename: 	The full path to the file holding the data. 
 * 
 * Returns 
 * =======
 * 0 on success, 1 on failure 
 * 
 * source: ha1997.c 
 */ 
extern unsigned short ka1997_import(char *filename); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* SSP_MLR_KA1997_H */ 
