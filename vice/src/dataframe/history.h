
#ifndef DATAFRAME_HISTORY_H 
#define DATAFRAME_HISTORY_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "../objects.h" 

/* 
 * Pull a row of data from a history object. This will automatically calculate 
 * the abundances by mass, their logarithmic counterparts, and all ratios for 
 * that output time. 
 * 
 * Parameters
 * ========== 
 * ff: 				A pointer to the fromfile object 
 * row: 			The row number to pull 
 * elements: 		The symbols of the elements to pull 
 * n_elements: 		The number of elements in the simulation 
 * solar: 			The solar abundance of each element 
 * Z_solar: 		The adopted solar metallicity by mass 
 * 
 * Returns 
 * ======= 
 * The corresponding row of the data; NULL on failure. 
 * 
 * source: history.c 
 */ 
extern double *history_row(FROMFILE *ff, unsigned long row, char **elements, 
	unsigned int n_elements, double *solar, double Z_solar); 

/* 
 * Determine the number of elements in one row of history output 
 * 
 * Parameters 
 * ========== 
 * ff: 				A pointer to the fromfile object 
 * n_elements: 		The number of elements in the output 
 * 
 * Returns 
 * ======= 
 * The total number of elements in the output 
 * 
 * source: history.c 
 */ 
extern unsigned int row_length(FROMFILE *ff, unsigned int n_elements); 

/*
 * Calculate the metallicity by mass Z of a given element in a history 
 * object. 
 * 
 * Parameters 
 * ========== 
 * ff:			A pointer to the fromfile object 
 * element: 	The element to calculate the metallicity by mass of 
 * 
 * Returns 
 * ======= 
 * A double pointer to Z(element) at all output times; NULL if the element is 
 * not found in the output 
 * 
 * source: history.c 
 */ 
extern double *Z_element(FROMFILE *ff, char *element); 

/* 
 * Calculate the logarithmic abundance ratio of two elements [X/Y] relative 
 * to the sun from a history object 
 * 
 * Parameters 
 * ========== 
 * ff: 				A pointer to the fromfile object 
 * element1: 		The symbol of element X 
 * element2: 		The symbol of element Y 
 * elements: 		The symbols of all of the elements in the simulation 
 * n_elements: 		The number of elements in the simulation 
 * solar: 			Each element's solar abundance 
 * 
 * Returns 
 * ======= 
 * A double pointer to [X/Y] at all output times; NULL if either element was 
 * not found in the output. 
 * 
 * Notes 
 * ===== 
 * This function responds properly when element2 == 'h' (i.e. when asked to 
 * calculate [X/H]) 
 * 
 * source: history.c 
 */ 
extern double *logarithmic_abundance_ratio(FROMFILE *ff, char *element1, 
	char *element2, char **elements, unsigned int n_elements, double *solar); 

/* 
 * Determine the scaled metallicity by mass at all output times according to: 
 * 
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar) 
 * 
 * Parameters 
 * ========== 
 * ff: 				A pointer to the fromfile object 
 * n_elements: 		The number of elements in the simulation 
 * elements: 		The symbols of each element 
 * solar: 			The solar abundance of each element 
 * Z_solar: 		The adopted solar abundance from the simulation 
 * 
 * Returns 
 * ======= 
 * A double pointer to the scaled metallicity by mass in the ISM at all output 
 * times. NULL on failure. 
 * 
 * See Also 
 * ======== 
 * Section 5.4 of Science Documentation 
 * 
 * source: history.c 
 */ 
extern double *Zscaled(FROMFILE *ff, unsigned int n_elements, char **elements, 
	double *solar, double Z_solar); 

/* 
 * Determine the scaled logarithmic total metallicity relative to solar [M/H] 
 * at all output times from a history object. 
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
 * A double pointer to [M/H] at all output times 
 * 
 * See Also 
 * ======== 
 * Section 5.4 of Science Documentation 
 * 
 * header: history.h 
 */ 
extern double *logarithmic_scaled(FROMFILE *ff, unsigned int n_elements, 
	char **elements, double *solar); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus*/ 

#endif /* DATAFRAME_HISTORY_H */ 


