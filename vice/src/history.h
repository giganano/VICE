
#ifndef HISTORY_H 
#define HISTORY_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#include "objects.h" 

/* 
 * Allocate memory for and return a pointer to a history object. 
 * 
 * source: history.c 
 */ 
extern HISTORY *history_initialize(void); 

/* 
 * Free the memory stored in a history object 
 * 
 * source: history.c 
 */ 
extern void history_free(HISTORY *hist); 

/* 
 * Read in the data in a file into the history object 
 * 
 * Parameters 
 * ========== 
 * hist: 		A pointer to the history object 
 * 
 * Returns 
 * ======= 
 * 0 on success from reading the file; 1 on failure 
 * 
 * source: history.c 
 */ 
extern int history_read(HISTORY *hist); 

/* 
 * Modify a column of the data in a history object 
 * 
 * Parameters 
 * ========== 
 * hist: 	A pointer to the history object 
 * label: 	The label of the column to modify 
 * arr: 	The new array to put in place of the old column. Assumed to be of 
 * 			length (*hist).n_rows. 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * Notes 
 * ===== 
 * In the event that the label is not recognized, history_new_column is 
 * called automatically. 
 * 
 * source: history.c 
 */ 
extern int history_modify_column(HISTORY *hist, char *label, double *arr); 

/* 
 * Add a column to the data in a history object. 
 * 
 * Parameters 
 * ========== 
 * hist: 	A pointer to the history object 
 * label: 	The label to let the new column have 
 * arr: 	The new column itself 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on failure 
 * 
 * source: history.c 
 */ 
extern int history_new_column(HISTORY *hist, char *label, double *arr); 

/* 
 * Pull a row of data from a history object. This will automatically calculate 
 * the abundances by mass, their logarithmic counterparts, and all ratios for 
 * that output time. 
 * 
 * Parameters
 * ========== 
 * hist: 		The history object 
 * row: 		The row number to pull 
 * 
 * Returns 
 * ======= 
 * The corresponding row of the data; NULL on failure. 
 * 
 * source: history.c 
 */ 
extern double *history_row(HISTORY *hist, unsigned long row); 

/*
 * Calculate the metallicity by mass Z of a given element in a history 
 * object. 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * element: 	The element to calculate the metallicity by mass of 
 * 
 * Returns 
 * ======= 
 * A double pointer to Z(element) at all output times; NULL if the element is 
 * not found in the output 
 * 
 * source: history.c 
 */ 
extern double *Z_element(HISTORY *hist, char *element); 

/* 
 * Calculate the logarithmic abundance ratio of two elements [X/Y] relative 
 * to the sun from a history object 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * element1:	The first element (element X) 
 * element2: 	The second element (element Y) 
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
 * header: history.h 
 */ 
extern double *logarithmic_abundance_ratio(HISTORY *hist, char *element1, 
	char *element2); 

/* 
 * Determine the scaled metallicity by mass at all output times according to: 
 * 
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar) 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object 
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
extern double *Zscaled(HISTORY *hist); 

/* 
 * Determine the scaled logarithmic total metallicity relative to solar [M/H] 
 * at all output times from a history object. 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object 
 * 
 * Returns 
 * ======= 
 * A double pointer to [M/H] at all output times 
 * 
 * See Also 
 * ======== 
 * Section 5.4 of Science Documentation 
 * 
 * source: history.c 
 */ 
extern double *logarithmic_scaled(HISTORY *hist); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 


#endif /* HISTORY_H */ 

