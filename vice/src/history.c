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
static double *logarithmic_abundance(FROMFILE *ff, char *element, 
	char **elements, unsigned int n_elements, double *solar); 
static int get_element_index(char **elements, char *element, 
	unsigned int n_elements); 
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements, 
	char **elements); 
static double Zsolar_by_element(double *solar, unsigned int n_elements); 

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
 * header: history.h 
 */ 
extern double *history_row(FROMFILE *ff, unsigned long row, char **elements, 
	unsigned int n_elements, double *solar, double Z_solar) {

	/* Allowed range of row number */ 
	if (row >= (*ff).n_rows) return NULL; 

	/* 
	 * One for each column already there, another two for each z(x) and [x/h] 
	 * measurement, then n chose 2 cross combinations of [X/Y] abundance 
	 * ratios, and one for Z and [M/H] 
	 */ 
	unsigned int length = row_length(ff, n_elements); 

	/* Pull the columns already there and resize */ 
	double *data = fromfile_row(ff, row); 
	if (data != NULL) {
		data = (double *) realloc(data, length * sizeof(double)); 
	} else { 
		return NULL; 
	} 

	/* Append the metallicity by mass of each element */ 
	unsigned int i, n = (*ff).n_cols; 
	for (i = 0; i < n_elements; i++) {
		double *Z = Z_element(ff, elements[i]); 
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
	for (i = 0; i < n_elements; i++) {
		double *onH = logarithmic_abundance(ff, elements[i], elements, 
			n_elements, solar); 
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
	for (i = 1; i < n_elements; i++) {
		unsigned int j; 
		for (j = 0; j < i; j++) {
			double *XonY = logarithmic_abundance_ratio(ff, elements[i], 
				elements[j], elements, n_elements, solar); 
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
	double *scaled = Zscaled(ff, n_elements, elements, solar, Z_solar); 
	double *MonH = logarithmic_scaled(ff, n_elements, elements, solar); 
	data[n] = scaled[row]; 
	data[n + 1] = MonH[row]; 
	free(scaled); 
	free(MonH); 
	return data; 

} 

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
 * header: history.h 
 */ 
extern unsigned int row_length(FROMFILE *ff, unsigned int n_elements) {

	return 2 + (*ff).n_cols + (2 * n_elements) + (
		n_elements * (n_elements - 1) / 2 
	); 

}

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
 * header: history.h 
 */ 
extern double *Z_element(FROMFILE *ff, char *element) {

	/* Pull the mass of the element using fromfile_column */ 
	char label[7 + strlen(element)]; 
	strcpy(label, "mass("); 
	strcat(label, element); 
	strcat(label, ")\0"); 
	double *element_mass = fromfile_column(ff, label); 
	if (element_mass != NULL) {
		/* Allocate memory and pull the ISM mass using fromfile_column */ 
		unsigned long i; 
		double *Z = (double *) malloc ((*ff).n_rows * sizeof(double)); 
		double *ism_mass = fromfile_column(ff, "mgas"); 
		for (i = 0l; i < (*ff).n_rows; i++) {
			/* Z(x) = M_x / Mgas */ 
			Z[i] = element_mass[i] / ism_mass[i]; 
		} 
		free(element_mass); 
		free(ism_mass); 
		return Z; 
	} else{
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
 * header: history.h 
 */ 
extern double *logarithmic_abundance_ratio(FROMFILE *ff, char *element1, 
	char *element2, char **elements, unsigned int n_elements, double *solar) {

	if (!strcmp(element2, "h")) {
		/* Return simply [X/H] */ 
		return logarithmic_abundance(ff, element1, elements, n_elements, 
			solar); 
	} else {
		/* Determine the abundances of [X/H] and [Y/H] independently */ 
		double *log_abundance1 = logarithmic_abundance(ff, element1, elements, 
			n_elements, solar); 
		double *log_abundance2 = logarithmic_abundance(ff, element2, elements, 
			n_elements, solar); 
		if (log_abundance1 != NULL && log_abundance2 != NULL) {
			/* If both elements were found in the output */ 
			unsigned long i; 
			double *ratio = (double *) malloc ((*ff).n_rows * sizeof(double)); 
			for (i = 0l; i < (*ff).n_rows; i++) {
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
 * ff: 				A pointer to the fromfile object 
 * element: 		The element to calculate the log abundance for 
 * elements: 		The symbols of all of the elements 
 * n_elements: 		The number of elements tracked by the simulation 
 * solar: 			The solar abundances of each element 
 * 
 * Returns 
 * ======= 
 * A double pointer to [X/H] at all output times; NULL if the element is not 
 * found in the output 
 */ 
static double *logarithmic_abundance(FROMFILE *ff, char *element, 
	char **elements, unsigned int n_elements, double *solar) {

	/* Start w/the metallicity by mass of the element */ 
	double *onH = Z_element(ff, element); 
	if (onH != NULL) {
		unsigned long i; 
		int index = get_element_index(elements, element, n_elements); 
		if (index != -1) {
			for (i = 0l; i < (*ff).n_rows; i++) {
				/* [X/H] = log10(Z(x) / Z_sun(x)) */ 
				onH[i] = log10(onH[i] / solar[index]); 
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
 * elements: 	The element symbols themselves 
 * element: 	The symbol of the element to get the index for 
 * n_elements: 	The number of elements tracked by the simulation 
 * 
 * Returns 
 * ======= 
 * The element's index: the integer such that hist.elements[index] is the 
 * same symbol as char *element. -1 if the element is not found in the history 
 * object. 
 */ 
static int get_element_index(char **elements, char *element, 
	unsigned int n_elements) {

	unsigned int i; 
	for (i = 0; i < n_elements; i++) {
		if (!strcmp(elements[i], element)) return (signed) i; 
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
 * header: history.h 
 */ 
extern double *Zscaled(FROMFILE *ff, unsigned int n_elements, char **elements, 
	double *solar, double Z_solar) {

	double solar_by_element = Zsolar_by_element(solar, n_elements); 
	double *total_by_element = Ztotal_by_element(ff, n_elements, elements); 
	if (total_by_element != NULL) {
		unsigned long i; 
		double *scaled = (double *) malloc ((*ff).n_rows * sizeof(double)); 
		for (i = 0l; i < (*ff).n_rows; i++) {
			scaled[i] = Z_solar * total_by_element[i] / solar_by_element; 
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
	char **elements, double *solar) {

	double solar_by_element = Zsolar_by_element(solar, n_elements); 
	double *total_by_element = Ztotal_by_element(ff, n_elements, elements); 
	if (total_by_element != NULL) {
		unsigned long i; 
		double *scaled = (double *) malloc ((*ff).n_rows * sizeof(double)); 
		for (i = 0l; i < (*ff).n_rows; i++) {
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
 * ff: 				A pointer to the fromfile object 
 * n_elements: 		The number of elements in the simulation 
 * elements: 		The symbols of each element 
 * 
 * Returns 
 * ======= 
 * A double pointer to the total metallicity by mass; NULL on failure 
 */ 
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements, 
	char **elements) {

	/* for-looping */ 
	unsigned int i; 
	unsigned long j; 

	/* Start by calculate Z for each element */ 
	double **by_element = (double **) malloc (n_elements * sizeof(double *)); 
	for (i = 0; i < n_elements; i++) {
		by_element[i] = Z_element(ff, elements[i]); 
		if (by_element[i] == NULL) {
			free(by_element); 
			return NULL; 
		} else {
			continue; 
		} 
	} 

	/* Allocate memory for the equivalent number of row ... */ 
	double *total = (double *) malloc ((*ff).n_rows * sizeof(double)); 
	for (j = 0l; j < (*ff).n_rows; j++) {
		total[j] = 0.0; 
		/* ... and add up the metallicities of each element */ 
		for (i = 0; i < n_elements; i++) {
			total[j] += by_element[i][j]; 
		} 
	} 
	free(by_element); 
	return total; 

}

/* 
 * Determine the total solar abundance by summing the solar abundances of 
 * each element in the history object. 
 * 
 * Parameters 
 * ========== 
 * solar: 			A double pointer to the solar abundances 
 * n_elements: 		The number of elements in the history object 
 * 
 * Returns 
 * ======= 
 * The calculated total solar metallicity by mass conting only the elements 
 * from the simulation. 
 */ 
static double Zsolar_by_element(double *solar, unsigned int n_elements) { 

	return sum(solar, (unsigned long) n_elements); 

}

