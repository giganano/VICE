/* 
 * This file implements the functionality of the tracers subclass of the VICE 
 * dataframe. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <math.h> 
#include "../dataframe.h" 
#include "../utils.h" 
#include "fromfile.h" 
#include "tracers.h" 
#include "utils.h" 

/* ---------- static function comment headers not duplicated here ---------- */ 
static double *tracers_log_abundance(FROMFILE *ff, char *element, 
	char **elements, unsigned int n_elements, double *solar); 
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements, 
	char **elements); 


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
 * header: tracers.h 
 */ 
extern double *tracers_ages(FROMFILE *ff) {

	unsigned long i; 
	double *formation_time = fromfile_column(ff, "formation_time"); 
	double max_formation_time = max(formation_time, (*ff).n_rows); 
	double *ages = (double *) malloc ((*ff).n_rows * sizeof(double)); 
	for (i = 0ul; i < (*ff).n_rows; i++) {
		ages[i] = max_formation_time - formation_time[i]; 
	} 
	free(formation_time); 
	return ages; 

}


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
 * header: tracers.h 
 */ 
extern double *tracers_Z_element(FROMFILE *ff, char *element) {

	/* 
	 * Unlike history outputs, tracer outputs have Z(x) directly in the file, 
	 * allowing lookup with fromfile_column directly. 
	 */ 
	char label[4 + strlen(element)]; 
	strcpy(label, "z("); 
	strcat(label, element); 
	strcat(label, ")\0"); 
	return fromfile_column(ff, label); 

}


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
 * header: tracers.h 
 */ 
extern double *tracers_log_abundance_ratio(FROMFILE *ff, char *element1, 
	char *element2, char **elements, unsigned int n_elements, double *solar) {

	if (!strcmp(element2, "h")) {
		/* return simply [X/H] */ 
		return tracers_log_abundance(ff, element1, elements, n_elements, solar); 
	} else {
		/* Determine the abundances of [X/H] and [Y/H] independently */ 
		double *XonH = tracers_log_abundance(ff, element1, elements, n_elements, 
			solar); 
		double *YonH = tracers_log_abundance(ff, element2, elements, n_elements, 
			solar); 
		if (XonH != NULL && YonH != NULL) {
			/* If both elements were found in the output */ 
			unsigned long i; 
			double *ratio = (double *) malloc ((*ff).n_rows * sizeof(double)); 
			for (i = 0ul; i < (*ff).n_rows; i++) {
				ratio[i] = XonH[i] - YonH[i]; 
			} 
			free(XonH); 
			free(YonH); 
			return ratio; 
		} else {
			if (XonH != NULL) free(XonH); 
			if (YonH != NULL) free(YonH); 
			return NULL; 
		}
	}

}


/* 
 * Determine the logarithmic abundance [X/H] for a given element X in each 
 * tracer particle. 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object holding the tracer particle data 
 * element: 	The (lower-case) symbol of the element to calculate the 
 * 				log-scaled abundance for 
 * solar: 		The abundance by mass of the element X in the sun 
 * 
 * Returns 
 * ======= 
 * [X/H] for each tracer particle. NULL if the element is not in the output. 
 */ 
static double *tracers_log_abundance(FROMFILE *ff, char *element, 
	char **elements, unsigned int n_elements, double *solar) { 

	double *onH = tracers_Z_element(ff, element); 
	if (onH != NULL) { 
		unsigned long i; 
		int index = get_element_index(elements, element, n_elements); 
		switch(index) {

			case -1: 
				free(onH); 
				return NULL; 

			default: 
				for (i = 0ul; i < (*ff).n_rows; i++) {
					onH[i] = log10(onH[i] / solar[index]); 
				} 
				return onH; 

		} 

	} else {
		return NULL; 
	}


} 


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
 * header: tracers.h 
 */ 
extern double *tracers_Zscaled(FROMFILE *ff, unsigned int n_elements, 
	char **elements, double *solar, double Z_solar) {

	double solar_by_element = Zsolar_by_element(solar, n_elements, elements); 
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
 * header: tracers.h 
 */ 
extern double *tracers_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements, 
	char **elements, double *solar) {

	double solar_by_element = Zsolar_by_element(solar, n_elements, elements); 
	double *total_by_element = Ztotal_by_element(ff, n_elements, elements); 
	if (total_by_element != NULL) {
		unsigned long i; 
		double *scaled = (double *) malloc ((*ff).n_rows * sizeof(double)); 
		for (i = 0ul; i < (*ff).n_rows; i++) {
			scaled[i] = log10(total_by_element[i] / solar_by_element); 
		} 
		free(total_by_element); 
		return scaled; 
	} else {
		return NULL; 
	}

}


/* 
 * Calculate the sum total metallicity of the stars by mass by adding the 
 * metallicities of each simulated element 
 * 
 * Parameters 
 * ========== 
 * ff: 			The fromfile object holding the tracer particle data 
 * n_elements: 	The number of simulated elements 
 * elements: 	The (lower-case) symbols of the simulated elements 
 * 
 * Returns 
 * ======= 
 * A double to the total metallicity by mass of each star particle. 
 */ 
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements, 
	char **elements) {

	unsigned int i; 
	unsigned long j; 

	/* Start by calculating Z for each element */ 
	double **by_element = (double **) malloc (n_elements * sizeof(double *)); 
	for (i = 0u; i < n_elements; i++) {
		if (strcmp(elements[i], "he")) { 
			/* If this isn't helium */ 
			by_element[i] = tracers_Z_element(ff, elements[i]); 
		} else {
			by_element[i] = (double *) malloc ((*ff).n_rows * sizeof(double)); 
			for (j = 0ul; j < (*ff).n_rows; j++) {
				by_element[i][j] = 0; 
			} 
		} 
		if (by_element[i] == NULL) {
			free(by_element); 
			return NULL; 
		} else {} 
	} 

	/* Allocate memory for the equivalent number of rows ... */ 
	double *total = (double *) malloc ((*ff).n_rows * sizeof(double)); 
	for (j = 0ul; j < (*ff).n_rows; j++) {
		/* ... and add up the metallicities of each element */ 
		total[j] = 0.0; 
		for (i = 0u; i < n_elements; i++) {
			total[j] += by_element[i][j]; 
		} 
	} 
	free(by_element); 
	return total; 

}






