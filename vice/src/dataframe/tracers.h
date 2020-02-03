
#ifndef DATAFRAME_TRACERS_H 
#define DATAFRAME_TRACERS_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Determine the age of each tracer star particle by subtracting its formation 
 * time from the maximum formation time found in the output data. 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object holding the tracer particle data. 
 * 
 * Returns 
 * ======= 
 * age: A double pointer to the age of each tracer particle. 
 * 
 * source: tracers.c 
 */ 
extern double *tracers_ages(FROMFILE *ff); 

/* 
 * Calculate the metallicity by mass Z of a given element for all stars in a 
 * tracer particle output file. 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object holding the stellar data 
 * element: 	The element to lookup the metallicity by mass for 
 * 
 * Returns 
 * ======= 
 * Z(x) for each star in the output data 
 * 
 * source: tracers.c 
 */ 
extern double *tracers_Z_element(FROMFILE *ff, char *element); 

/* 
 * Calculate the logarithmic abundance ratio of two elements [X/Y] relative 
 * to the sun from star particle data 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object holding the tracer particle data 
 * element1: 	The symbol of the element X 
 * element2: 	The symbol of the element Y 
 * elements: 	The symbols of all of the elements in the simulation 
 * n_elements: 	The number of elements in the simulation 
 * solar: 		Each element's solar abundance 
 * 
 * Returns 
 * ======= 
 * A double pointer to [X/Y] for all tracer particles. NULL if either element 
 * was not found in the data. 
 * 
 * Notes 
 * ===== 
 * This function responds properly when element2 == 'h' (i.e. when asked to 
 * calculate [X/H]) 
 * 
 * source: tracers.c 
 */ 
extern double *tracers_log_abundance_ratio(FROMFILE *ff, char *element1, 
	char *element2, char **elements, unsigned int n_elements, double *solar); 

/* 
 * Determine the scaled metallicity by mass of all star particles according to: 
 * 
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar) 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object containing the tracer particle data 
 * n_elements: 	The number of elements in the simulation 
 * elements: 	The (lower-case) symbols of each element 
 * solar: 		The solar abundance of each element 
 * Z_solar: 	The adopted solar abundance from the simulation 
 * 
 * Returns 
 * ======= 
 * A double pointer to the scaled metallicity by mass of each star particle. 
 * NULL on failure. 
 * 
 * See Also 
 * ======== 
 * Section 5.4 of Science Documentation 
 * 
 * source: tracers.c 
 */ 
extern double *tracers_Zscaled(FROMFILE *ff, unsigned int n_elements, 
	char **elements, double *solar, double Z_solar); 

/* 
 * Determine the scaled logarithmic total metallicity relative to solar [M/H] 
 * for all star particles. 
 * 
 * Parameters 
 * ========== 
 * ff: 				A pointer to the fromfile object 
 * n_elements: 		The number of elements in the simulation 
 * elements: 		The symbols of each element 
 * solar: 			Each element's solar abundance 
 * 
 * Returns 
 * ======= 
 * A double pointer to [M/H] for all stars. NULL on failure. 
 * 
 * See Also 
 * ======== 
 * Section 5.4 of Science Documentation 
 * 
 * source: tracers.c 
 */ 
extern double *tracers_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements, 
	char **elements, double *solar); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* DATAFRAME_TRACERS_H */ 
