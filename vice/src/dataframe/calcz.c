/*
 * This file implements calculations of the metallicity by mass Z for both
 * history and tracer particle output files. The functions are largely the
 * same, and for that reason are combined to not repeat code.
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "../dataframe.h"
#include "fromfile.h"
#include "calcz.h"
#include "utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *(*calc_Z_function)(FROMFILE *, char *));
static double *Zscaled(FROMFILE *ff, unsigned int n_elements, char **elements,
	double *solar, double Z_solar,
	double *(*Z_total_by_element)(FROMFILE *, unsigned int, char **));


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
 * header: calcz.h
 */
extern double *history_Z_element(FROMFILE *ff, char *element) {

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
 * header: calcz.h
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
 * Calculate the sum total metallicity of each element from output stored in a
 * fromfile object with history data.
 *
 * Parameters
 * ==========
 * ff: 				The fromfile object
 * n_elements: 		The number of elements with data in the file
 * elements: 		The (lower-case) symbols of the elements
 *
 * Returns
 * =======
 * The sum total metallicity of the ISM at each output time considering only
 * simulated elements.
 *
 * header: calcz.h
 */
extern double *history_Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements) {

	return Ztotal_by_element(ff, n_elements, elements, history_Z_element);

}


/*
 * Calculate the sum total metallicity of each element from output stored in a
 * fromfile object with tracer particle data.
 *
 * Parameters
 * ==========
 * ff: 				The fromfile object
 * n_elements: 		The number of elements with data in the file
 * elements: 		The (lower-case) symbols of the elements
 *
 * Returns
 * =======
 * The sum total metallicity of each star considering only simulated elements.
 *
 * header: calcz.h
 */
extern double *tracers_Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements) {

	return Ztotal_by_element(ff, n_elements, elements, tracers_Z_element);

}


/*
 * Calculate the sum total metallicity of each element whose output is
 * stored in a fromfile object.
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements whose data is stored
 * elements: 			The (lower-case) symbols of each element
 * calc_Z_function: 	A pointer to the function to use to calculate an
 * 						individual metallicity. For tracer particle data,
 * 						this should be tracers_Z_element, and
 * 						history_Z_element for history objects.
 *
 * Returns
 * =======
 * The sum of each metallicity by mass at each time or for each tracer
 * particle.
 */
static double *Ztotal_by_element(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *(*calc_Z_function)(FROMFILE *, char *)) {

	/* for-looping */
	unsigned int i;
	unsigned long j;

	/* Start by calculating Z for each element */
	double **by_element = (double **) malloc (n_elements * sizeof(double *));
	for (i = 0u; i < n_elements; i++) {
		if (strcmp(elements[i], "he")) {
			/* If this isn't helium */
			by_element[i] = calc_Z_function(ff, elements[i]);
		} else {
			/* Put in zeroes for helium */
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
		total[j] = 0;
		/* ... and add up the metallicities of each element */
		for (i = 0u; i < n_elements; i++) {
			total[j] += by_element[i][j];
		}
	}
	free(by_element);
	return total;

}


/*
 * Determine the scaled metallicity by mass at all output times according to:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements with data in the file
 * elements: 			The (lower-case) symbols of each element
 * solar: 				The solar abundance of each element
 * Z_solar: 			The adopted solar abundance from the simulation
 *
 * Returns
 * =======
 * The scaled metallicity of the ISM at all output times.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * header: calcz.h
 */
extern double *history_Zscaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar, double Z_solar) {

	return Zscaled(ff, n_elements, elements, solar, Z_solar,
		history_Ztotal_by_element);

}


/*
 * Determine the scaled metallicity by mass for all tracer particles according
 * to:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements with data in the file
 * elements: 			The (lower-case) symbols of each element
 * solar: 				The solar abundance of each element
 * Z_solar: 			The adopted solar abundance from the simulation
 *
 * Returns
 * =======
 * The scaled metallicity of each tracer particle.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 *
 * header: calcz.h
 */
extern double *tracers_Zscaled(FROMFILE *ff, unsigned int n_elements,
	char **elements, double *solar, double Z_solar) {

	return Zscaled(ff, n_elements, elements, solar, Z_solar,
		tracers_Ztotal_by_element);

}


/*
 * Determine the scaled metallicity by mass at all output times or for all
 * tracer particles according to:
 *
 * Z = Z_solar * sum(Z_i) / sum(Z_i_solar)
 *
 * Parameters
 * ==========
 * ff: 					The fromfile object containing the data
 * n_elements: 			The number of elements with data in the file
 * elements: 			The (lower-case) symbols of each element
 * solar: 				The solar abundance of each element
 * Z_solar: 			The adopted solar abundance from the simulation
 * Z_total_by_element:	A pointer to the function to be used to calculate the
 * 						total metallicity of each element. For tracer particle
 * 						data, this should be tracers_Ztotal_by_element, and
 * 						history_Ztotal_by_element for history data.
 *
 * Returns
 * =======
 * The scaled metallicity of the ISM at all output times, or the scaled
 * metallicity of each tracer particle.
 *
 * See Also
 * ========
 * Section 5.4 of Science Documentation
 */
static double *Zscaled(FROMFILE *ff, unsigned int n_elements, char **elements,
	double *solar, double Z_solar,
	double *(*Z_total_by_element)(FROMFILE *, unsigned int, char **)) {

	double solar_by_element = Zsolar_by_element(solar, n_elements, elements);
	double *total_by_element = Z_total_by_element(ff, n_elements, elements);
	if (total_by_element != NULL) {
		unsigned long i;
		double *scaled = (double *) malloc ((*ff).n_rows * sizeof(double));
		for (i = 0ul; i < (*ff).n_rows; i++) {
			scaled[i] = Z_solar * total_by_element[i] / solar_by_element;
		}
		free(total_by_element);
		return scaled;
	} else {
		return NULL;
	}

}

