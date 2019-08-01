/* 
 * This file implements the core routines of the history subclass of the 
 * VICE dataframe. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "history.h" 
#include "fromfile.h" 
#include "utils.h" 
#include "io.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double *logarithmic_abundance(HISTORY *hist, char *element); 
static int get_element_index(HISTORY *hist, char *element); 
static double *Ztotal_by_element(HISTORY *hist); 
static double Zsolar_by_element(HISTORY *hist); 

/* 
 * Allocate memory for and return a pointer to a history object. 
 * 
 * header: history.h 
 */ 
extern HISTORY *history_initialize(void) {

	HISTORY *hist = (HISTORY *) realloc (fromfile_initialize(), 
		sizeof(HISTORY)); 
	hist -> elements = NULL; 
	hist -> n_elements = 0; 
	hist -> Z_solar = 0.014; 	/* default to VICE's default from Asplund+09 */ 
	return hist; 

} 

/* 
 * Free the memory stored in a history object 
 * 
 * header: history.h 
 */ 
extern void history_free(HISTORY *hist) {

	if (hist != NULL) {

		if ((*hist).elements != NULL) { 
			unsigned int i; 
			for (i = 0; i < (*hist).n_elements; i++) { 
				if ((*hist).elements[i] != NULL) { 
					free(hist -> elements[i]); 
					hist -> elements[i] = NULL; 
				} else {
					continue; 
				} 
			} 
			free(hist -> elements); 
			hist -> elements = NULL; 
		} else {} 

		hist -> n_elements = 0; 
		fromfile_free((FROMFILE *) hist); 

	} else {} 

} 

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
 * header: history.h 
 */ 
extern int history_read(HISTORY *hist) {

	/* Equivalent of calling super().read() */ 
	return fromfile_read((FROMFILE *) hist); 

} 

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
 * header: history.h 
 */ 
extern int history_modify_column(HISTORY *hist, char *label, double *arr) {

	/* Equivalent of calling super().modify_column() */ 
	return fromfile_modify_column((FROMFILE *) hist, label, arr); 

} 

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
 * header: history.h 
 */ 
extern int history_new_column(HISTORY *hist, char *label, double *arr) {

	/* Equivalent of calling super().new_column() */ 
	return fromfile_new_column((FROMFILE *) hist, label, arr); 

}

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
 * header: history.h 
 */ 
extern double *history_row(HISTORY *hist, unsigned long row) {

	/* Allowed range of row numbers */ 
	if (row >= (*hist).n_rows) return NULL; 

	/* 
	 * One for each column already there, another two for each z(x) and [x/h] 
	 * measurement, then n choose 2 cross combinations of [X/Y] abundance 
	 * ratios 
	 */ 
	unsigned int length = (*hist).n_cols + (2 * (*hist).n_elements) + (
		(*hist).n_elements * ((*hist).n_elements - 1) / 2 
	); 

	/* Pull the columns already there and resize */ 
	double *data = fromfile_row((FROMFILE *) hist, row); 
	if (data != NULL) {
		data = (double *) realloc (data, length * sizeof(double)); 
	} else {
		return NULL; 
	} 
	
	/* Append the metallicity by mass of each element */ 
	unsigned int i, n = (*hist).n_cols; 
	for (i = 0; i < (*hist).n_elements; i++) { 
		double *Z = Z_element(hist, (*hist).elements[i]); 
		if (Z != NULL) { 
			data[n] = Z[row]; 
			free(Z); 
			n++; 
		} else { 
			free(data); 
			return NULL; 
		} 
	} 

	/* Append the logarithmic abundance relative to solar of each element */ 
	for (i = 0; i < (*hist).n_elements; i++) {
		double *onH = logarithmic_abundance(hist, (*hist).elements[i]); 
		if (onH != NULL) { 
			data[n] = onH[row]; 
			free(onH); 
			n++; 
		} else {
			free(data); 
			return NULL; 
		} 
	} 

	/* 
	 * Append the logarithmic abundance ratios relative to solar for each 
	 * combination of elements 
	 */ 
	for (i = 1; i < (*hist).n_elements; i++) { 
		unsigned int j; 
		for (j = 0; j < i; j++) { 
			double *XonY = logarithmic_abundance_ratio(hist, 
				(*hist).elements[i], 
				(*hist).elements[j]); 
			if (XonY != NULL) {
				data[n] = XonY[row]; 
				free(XonY); 
				n++; 
			} else {
				free(data); 
				return NULL; 
			} 
		} 
	} 
	// printf("n = %d\n", n); 
	return data; 

}

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
 * header: history.h 
 */ 
extern double *Z_element(HISTORY *hist, char *element) {

	/* Pull the mass of the element using fromfile_column */ 
	char label[7 + strlen(element)]; 
	strcpy(label, "mass("); 
	strcat(label, element); 
	strcat(label, ")\0"); 
	double *element_mass = fromfile_column((FROMFILE *) hist, label); 
	if (element_mass != NULL) { 
		/* Allocate memory and pull the ISM mass using fromfile_column */ 
		unsigned long i; 
		double *Z = (double *) malloc ((*hist).n_rows * sizeof(double)); 
		double *ism_mass = fromfile_column((FROMFILE *) hist, "mgas"); 
		for (i = 0l; i < (*hist).n_rows; i++) { 
			/* Z(x) = M_x / Mgas */ 
			Z[i] = element_mass[i] / ism_mass[i]; 
		} 
		free(element_mass); 
		free(ism_mass); 
		return Z; 
	} else { 
		/* error -> element not found in output */ 
		return NULL; 
	}

} 

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
	char *element2) {

	if (!strcmp(element2, "h")) { 
		/* Return simply [X/H] */ 
		return logarithmic_abundance(hist, element1); 
	} else { 
		/* Determine the abundances of [X/H] and [Y/H] independently */ 
		double *log_abundance1 = logarithmic_abundance(hist, element1); 
		double *log_abundance2 = logarithmic_abundance(hist, element2); 
		if (log_abundance1 != NULL && log_abundance2 != NULL) { 
			/* If both elements were found in the output */ 
			unsigned long i; 
			double *ratio = (double *) malloc ((*hist).n_rows * sizeof(double)); 
			for (i = 0l; i < (*hist).n_rows; i++) { 
				/* [X/Y] = [X/H] - [Y/H] */ 
				ratio[i] = log_abundance1[i] - log_abundance2[i]; 
			} 
			free(log_abundance1); 
			free(log_abundance2); 
			return ratio; 
		} else { 
			/* One of them not found -> return NULL */ 
			if (log_abundance1 != NULL) free(log_abundance1); 
			if (log_abundance2 != NULL) free(log_abundance2); 
			return NULL; 
		} 
	} 

}

/* 
 * Calculate the logarithmic abundance relative to solar of a given element 
 * in a history object. 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * element: 	The symbol of the element to get the logarithmic abundance for 
 * 
 * Returns 
 * ======= 
 * A double pointer to [X/H] at all output times; NULL if the element is not 
 * found in the output 
 */ 
static double *logarithmic_abundance(HISTORY *hist, char *element) {

	/* Start w/the metallicity by mass of the element */ 
	double *onH = Z_element(hist, element); 
	if (onH != NULL) { 
		unsigned long i; 
		int index = get_element_index(hist, element); 
		if (index != -1) { 
			for (i = 0l; i < (*hist).n_rows; i++) { 
				/* [X/H] = log10(Z(x) / Z_sun(x)) */ 
				onH[i] = log10(onH[i] / (*hist).solar[index]); 
			} 
			return onH; 
		} else {
			free(onH); 
			return NULL; 
		} 
	} else { 
		return NULL; 
	}
		

} 

/* 
 * Determine the index of an element in a history object. 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * element: 	The symbol of the element to get the index for 
 * 
 * Returns 
 * ======= 
 * The element's index: the integer such that hist.elements[index] is the 
 * same symbol as char *element. -1 if the element is not found in the history 
 * object. 
 */ 
static int get_element_index(HISTORY *hist, char *element) {

	unsigned int i; 
	for (i = 0; i < (*hist).n_elements; i++) {
		if (!strcmp((*hist).elements[i], element)) return (signed) i; 
	} 
	return -1; 

} 

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
 * header: history.h 
 */ 
extern double *Zscaled(HISTORY *hist) {

	double solar_by_element = Zsolar_by_element(hist); 
	double *total_by_element = Ztotal_by_element(hist); 
	if (total_by_element != NULL) { 
		unsigned long i; 
		double *scaled = (double *) malloc ((*hist).n_rows * sizeof(double)); 
		for (i = 0l; i < (*hist).n_rows; i++) {
			scaled[i] = (
				(*hist).Z_solar * total_by_element[i] / solar_by_element
			); 
		} 
		free(total_by_element); 
		return scaled; 
	} else {
		return NULL; 
	}

} 

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
 * header: history.h 
 */ 
extern double *logarithmic_scaled(HISTORY *hist) {

	double solar_by_element = Zsolar_by_element(hist); 
	double *total_by_element = Ztotal_by_element(hist); 
	if (total_by_element != NULL) { 
		unsigned long i; 
		double *scaled = (double *) malloc ((*hist).n_rows * sizeof(double)); 
		for (i = 0l; i < (*hist).n_rows; i++) {
			scaled[i] = log10(total_by_element[i] / solar_by_element); 
		} 
		free(total_by_element); 
		return scaled; 
	} else {
		return NULL; 
	}

}

/* 
 * Calculate the sum total metallicity of the ISM by mass by adding the 
 * metallicities by mass of each element 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * 
 * Returns 
 * ======= 
 * A double pointer to the total metallicity by mass; NULL on failure 
 */ 
static double *Ztotal_by_element(HISTORY *hist) {

	/* for-looping */ 
	unsigned int i; 
	unsigned long j; 

	/* Start by calculating Z for each element */ 
	double **by_element = (double **) malloc ((*hist).n_elements * 
		sizeof(double *)); 
	for (i = 0; i < (*hist).n_elements; i++) {
		by_element[i] = Z_element(hist, (*hist).elements[i]); 
		if (by_element[i] == NULL) { 
			free(by_element); 	/* error */ 
			return NULL; 
		} else { 
			continue; 
		} 
	} 

	/* Allocate memory for the equivalent number of rows ... */ 
	double *total = (double *) malloc ((*hist).n_rows * sizeof(double)); 
	for (j = 0l; j < (*hist).n_rows; j++) {
		total[j] = 0; 
		/* ... and add up the metallicities of each element */ 
		for (i = 0; i < (*hist).n_elements; i++) { 
			total[j] += by_element[i][j]; 
		} 
	} 
	free(by_element); 
	return total; 

} 

/* 
 * Determine the total solar abundance by summing the solar abundances of each 
 * element in the history object. 
 * 
 * Parameters 
 * ========== 
 * hist: 		The history object itself 
 * 
 * Returns 
 * ======= 
 * The calculated total solar metallicity by mass counting only the elements 
 * from the simulation. 
 */ 
static double Zsolar_by_element(HISTORY *hist) { 

	return sum((*hist).solar, (unsigned long) (*hist).n_elements); 

}

