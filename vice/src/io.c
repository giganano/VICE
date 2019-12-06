/* 
 * This file implements all of VICE's input/output. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include <stdio.h> 
#include <ctype.h> 
#include <math.h> 
#include "singlezone.h" 
#include "ism.h" 
#include "mdf.h" 
#include "ssp.h" 
#include "io.h" 

/* 
 * Reads in a square ascii file given the name of the file. 
 * 
 * Parameters 
 * ========== 
 * file: 		The name of the file 
 * 
 * Returns 
 * ======= 
 * Type double**. The data stored in the file as a 2D array indexed via 
 * data[row_number][column_number]. NULL upon failure to read the input file. 
 * 
 * header: io.h 
 */ 
extern double **read_square_ascii_file(char *file) {

	/* 
	 * Initialize important variables for reading the file. See docstrings of 
	 * called functions for details on these quantities 
	 */ 
	long length = line_count(file); 
	if (length == -1l) return NULL; 		/* error handling */ 
	int h_length = header_length(file); 
	if (h_length == -1) return NULL; 
	int dimension = file_dimension(file); 
	if (dimension == -1) return NULL; 
	FILE *in = fopen(file, "r"); 
	if (in == NULL) return NULL; 

	/* Read passed the header */ 
	int i; 
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	for (i = 0; i < h_length; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in); 
			free(line); 
			return NULL; 
		} else {} 
	} 
	free(line); 

	/* 
	 * Assume that all lines beneath the header have data, then read the 
	 * data in as a 2D array
	 */ 
	long j; 
	double **data = (double **) malloc ( (unsigned) (length - h_length) * 
		sizeof(double *)); 
	for (j = 0l; j < length - h_length; j++) { 
		data[j] = (double *) malloc ( (unsigned) dimension * sizeof(double)); 
		for (i = 0; i < dimension; i++) { 
			if (fscanf(in, "%lf", &data[j][i])) {
				continue; 
			} else {
				fclose(in); 
				free(data); 
				return NULL; 
			}
		}
	} 
	fclose(in); 
	return data; 

}

/* 
 * Determine the length of the header at the top of a data file assuming all 
 * header lines begin with #. 
 * 
 * Parameters 
 * ========== 
 * file: 	The name of the file 
 * 
 * Returns 
 * ======= 
 * The length of the header; -1 on failure to read from the file. 
 * 
 * header: io.h 
 */ 
extern int header_length(char *file) {

	/* Open the file and check for error opening the file */ 
	FILE *in = fopen(file, "r"); 
	if (in == NULL) return -1; 

	/* Store a line in memory, check for error reading the first line */  
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	if (fgets(line, LINESIZE, in) == NULL) { 
		fclose(in); 
		free(line); 
		return -1; 
	} else {} 

	/* Add up the number of lines at the beginning of file that start with # */ 
	int n = 0; 
	while (line[0] == '#') { 
		n++; 
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in); 
			free(line); 
			return -1; 
		} else {
			continue; 
		} 
	} 

	fclose(in); 
	free(line); 
	return n; 

} 

/* 
 * Determine the dimensionality of a data file off of the first line passed the 
 * header, assuming the header is commented out with '#'. 
 * 
 * Parameters 
 * ========== 
 * file: 		The file to determine the dimensionality of 
 * 
 * Returns 
 * ======= 
 * The number of quantities on one line of the file. -1 on failure to read 
 * from the file 
 * 
 * header: io.h 
 */ 
extern int file_dimension(char *file) {

	/* Need to read past header first, find out how many lines that is */ 
	int hlen = header_length(file); 
	if (hlen == -1) return -1; 		/* error checking */ 

	FILE *in = fopen(file, "r"); 
	if (in == NULL) return -1; 		/* error checking */ 

	/* Store a line in memory, read passed the header */ 
	int i; 
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	for (i = 0; i <= hlen; i++) {
		if (fgets(line, LINESIZE, in) == NULL) { 
			fclose(in); 
			free(line); 
			return -1; 				/* error checking */ 
		} else {
			continue; 
		} 
	} 

	/* 
	 * For any character in the line that is not whitespace, if the following 
	 * character is whitespace, increment the dimensionality. 
	 */ 
	int dimension = 0; 
	unsigned int j; 
	for (j = 0; j < strlen(line) - 1; j++) { 
		if (isspace(line[j + 1]) && !isspace(line[j])) {
			dimension++; 
		} else {
			continue; 
		} 
	} 
	fclose(in); 
	free(line); 
	return dimension; 

} 

/* 
 * Determine the number of lines in an text file 
 * 
 * Parameters 
 * ========== 
 * file: 		The name of the file 
 * 
 * Returns 
 * ======= 
 * The number of total lines, counting comment headers and blank lines. -1l on 
 * failure to read from the file 
 * 
 * header: io.h 
 */ 
extern long line_count(char *file) {

	FILE *in = fopen(file, "r"); 
	if (in == NULL) return -1l; 		/* error checking */ 

	/* 
	 * Start reading in lines, count them, and don't stop until fgets returns 
	 * NULL. 
	 */ 
	long n = 0l; 
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	while (fgets(line, LINESIZE, in) != NULL) {
		n++; 
	} 
	fclose(in); 
	free(line); 
	return n; 

}

/* 
 * Import a built-in AGB star yields grid. 
 * 
 * Parameters 
 * ========== 
 * e: 		A pointer to the element struct to import the grid into 
 * file: 	The name of the file containing the AGB yield grid. These are 
 * 			include in VICE's data directory, and direct user access to them 
 * 			is strongly discouraged. 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on failure 
 * 
 * header: io.h 
 */ 
extern unsigned short import_agb_grid(ELEMENT *e, char *file) {

	/* 
	 * Initialize important variables for reading the file. See docstrings of 
	 * called functions for details on these quantities. 
	 * 
	 * Note: The change in error handing check to require that AGB yield grids 
	 * be 3-dimensional. All AGB yield data files stored internally in VICE 
	 * are of this format. 
	 */ 
	long length = line_count(file); 
	if (length == -1l) return 1; 		/* error handling */ 
	int h_length = header_length(file); 
	if (h_length == -1) return 2; 
	int dimension = file_dimension(file); 
	if (dimension != 3) return 3; 
	FILE *in = fopen(file, "r"); 
	if (in == NULL) return 4; 

	/* 
	 * first keeps track of the first occurrence of a given mass in the 
	 * table 
	 * 
	 * line keeps track of the line that was just read in 
	 */ 
	double *first = (double *) malloc (3 * sizeof(double)); 
	double *line = (double *) malloc (3 * sizeof(double)); 
	if (!fscanf(in, "%lf %lf %lf", &first[0], &first[1], &first[2])) {
		fclose(in); 
		free(first); 
		free(line); 
		return 5; 
	} else {} 

	e -> agb_grid -> n_z = 0l; 		/* start counting metallicities */ 
	do {
		if (fscanf(in, "%lf %lf %lf", &line[0], &line[1], &line[2])) { 
			/* Count metallicities while the mass stays the same */ 
			e -> agb_grid -> n_z++; 
			continue; 
		} else {
			fclose(in); 
			free(first); 
			free(line); 
			return 6; 
		} 
	} while (line[0] == first[0]); 

	/* Free up memory, start over, and read the whole thing in */ 
	free(first); 
	free(line); 
	fclose(in); 

	/* 
	 * The length of the file must be divisible by the number of sampled 
	 * massed and metallicities. Otherwise assume that the file is formatted 
	 * correctly, with mass and metallicity increasing line by line. Current 
	 * supported versions of VICE do not support user constructed AGB tables, 
	 * so this is not a source of error. 
	 * 
	 * The grid files are designed such that the metallicites go up at 
	 * constant mass, then the mass increases, and both increase monotonically 
	 * with the line number. These lines are explicitly designed to read in 
	 * that format. 
	 */ 
	switch ( (unsigned) length % (*(*e).agb_grid).n_z ) { 
		unsigned int i, j; 

		case 0: 
			/* 
			 * The switch must be equal to zero, or else the data file has 
			 * been tampered with. 
			 */ 
			e -> agb_grid -> n_m = (unsigned) length / (*(*e).agb_grid).n_z; 
			in = fopen(file, "r"); 
			if (in == NULL) return 1; 
			e -> agb_grid -> m = (double *) malloc (
				(*(*e).agb_grid).n_m * sizeof(double)); 
			e -> agb_grid -> z = (double *) malloc (
				(*(*e).agb_grid).n_z * sizeof(double)); 
			e -> agb_grid -> grid = (double **) malloc (
				(*(*e).agb_grid).n_m * sizeof(double)); 
			for (i = 0; i < (*(*e).agb_grid).n_m; i++) { 
				e -> agb_grid -> grid[i] = (double *) malloc (
					(*(*e).agb_grid).n_z * sizeof(double)); 
				for (j = 0; j < (*(*e).agb_grid).n_z; j++) {
					if (fscanf(
						in, "%lf %lf %lf", 
						&(e -> agb_grid -> m[i]), 
						&(e -> agb_grid -> z[j]), 
						&(e -> agb_grid -> grid[i][j])
					)) {
						continue; 
					} else {
						free(e -> agb_grid -> grid); 
						free(e -> agb_grid -> m); 
						free(e -> agb_grid -> z); 
						fclose(in); 
						return 7; 
					}
				} 
			} 
			fclose(in); 
			return 0; 		/* error handling: success */ 

		default: 
			return 8; 		/* error handling: failure */ 

	} 

}

/* 
 * Read a yield table for CCSNe. 
 * 
 * Parameters 
 * ========== 
 * file: 		The name of the file, passed from python. 
 * 
 * Returns 
 * ======= 
 * Type **double: 
 * 		returned[i][0]: initial stellar mass 
 * 		returned[i][1]: total mass yield of the element 
 * NULL on failure to read from the file 
 * 
 * header: io.h 
 */ 
extern double **cc_yield_grid(char *file) {

	/* 
	 * The number of masses and isotopes on the grid can be determined from 
	 * the length and dimensionality of the data file 
	 */ 
	int n_masses = line_count(file) - header_length(file); 
	if (n_masses == 0) return NULL; 
	int dimension = file_dimension(file); 
	if (dimension == -1) return NULL; 			/* error handling */ 

	int i, j; 
	double **raw = read_square_ascii_file(file); 
	double **grid = (double **) malloc ( (unsigned) n_masses * 
		sizeof(double *)); 
	for (i = 0; i < n_masses; i++) { 
		/* Convert to a stellar mass - total isotope mass yield grid */ 
		grid[i] = (double *) malloc (2 * sizeof(double)); 
		grid[i][0] = raw[i][0]; 
		grid[i][1] = 0; 
		for (j = 1; j < dimension; j++) {
			grid[i][1] += raw[i][j]; 
		} 
	} 
	free(raw); 
	return grid; 

} 

/* 
 * Lookup the mass yield of a given element from type Ia supernovae 
 * 
 * Parameters 
 * ========== 
 * file: 		The name of the yield file, passed from python 
 * 
 * Returns 
 * ======= 
 * The total mass yield in Msun of the given element reported by the built-in 
 * study's data. -1 on failure to read from the data file 
 * 
 * header: io.h 
 */ 
extern double single_ia_mass_yield_lookup(char *file) {

	int h_length = header_length(file); 
	if (h_length == -1) return -1; 				/* error handling */ 
	/* -1 because these files have a blank line on the end */ 
	int n_isotopes = line_count(file) - h_length - 1; 
	FILE *in = fopen(file, "r"); 
	if (in == NULL) return -1; 

	int i; 
	char *line = (char *) malloc (LINESIZE * sizeof(char)); 
	for (i = 0; i < h_length; i++) {
		if (fgets(line, LINESIZE, in) == NULL) {
			fclose(in); 
			free(line); 
			return -1; 
		} else { 
			continue; 
		} 
	} 

	double yield = 0; 
	for (i = 0; i < n_isotopes; i++) {
		double x; 
		if (fscanf(in, "%s %le", line, &x)) {
			yield += x; 
		} else {
			fclose(in); 
			free(line); 
			return -1; 
		} 
	} 

	fclose(in); 
	free(line); 
	return yield; 

}

/* 
 * Open the history.out and mdf.out output files associated with a SINGLEZONE 
 * object. 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: io.h 
 */ 
extern unsigned short singlezone_open_files(SINGLEZONE *sz) {

	char *history_file = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	char *mdf_file = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 

	strcpy(history_file, (*sz).name); 
	strcpy(mdf_file, (*sz).name); 
	strcat(history_file, "/history.out"); 
	strcat(mdf_file, "/mdf.out"); 

	sz -> history_writer = fopen(history_file, "w"); 
	sz -> mdf_writer = fopen(mdf_file, "w"); 

	free(history_file); 
	free(mdf_file); 

	if ((*sz).history_writer == NULL || (*sz).mdf_writer == NULL) {
		return 1; 
	} else {
		return 0; 
	}

} 

/* 
 * Close the history.out and mdf.out output files associated with a SINGLEZONE 
 * object and sets their values back to NULL. 
 * 
 * header: io.h 
 */ 
extern void singlezone_close_files(SINGLEZONE *sz) {

	if ((*sz).history_writer != NULL) {
		fclose(sz -> history_writer); 
		sz -> history_writer = NULL; 
	} else {} 
	if ((*sz).mdf_writer != NULL) {
		fclose(sz -> mdf_writer); 
		sz -> mdf_writer = NULL; 
	} else {} 

} 

/* 
 * Writes the header to the history file 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * 
 * header: io.h 
 */ 
extern void write_history_header(SINGLEZONE sz) {

	/* 
	 * Change Notes 
	 * ============ 
	 * Calculation of ISM metallicities now moved to output handling functions. 
	 * The primary motivation for this was to remove overhead from calculating 
	 * and recording every [X/Y] combination of abundance ratios. VICE still 
	 * does this automatically, but from the output instead of during 
	 * simulation. This significantly improves the speed of simulations with 
	 * high n_elements. 
	 */ 

	fprintf(sz.history_writer, "# COLUMN NUMBERS: \n"); 
	fprintf(sz.history_writer, "#\t0: time [Gyr]\n"); 
	fprintf(sz.history_writer, "#\t1: mgas [Msun]\t\t\tISM gas mass\n"); 
	fprintf(sz.history_writer, "#\t2: mstar [Msun]\t\t\tStellar mass\n"); 
	fprintf(sz.history_writer, "#\t3: sfr [Msun/yr]\t\tStar formation rate\n"); 
	fprintf(sz.history_writer, "#\t4: ifr [Msun/yr]\t\tInfall rate\n"); 
	fprintf(sz.history_writer, "#\t5: ofr [Msun/yr]\t\tOutfow rate\n"); 
	fprintf(sz.history_writer, "#\t6: eta_0\t\t\tMass-loading factor\n"); 
	fprintf(sz.history_writer, "#\t7: r_eff\t\t\tEffective recycilng rate\n"); 
	
	// unsigned int i, j, n = 8; 
	unsigned int i, n = 8; 
	for (i = 0; i < sz.n_elements; i++) { 
		/* Inflow metallicity for each element */ 
		fprintf(sz.history_writer, 
			"#\t%d: z_in(%s)\t\t\tInflow %s metallicity\n", 
			n, (*sz.elements[i]).symbol, (*sz.elements[i]).symbol); 
		n++; 
	} 
	for (i = 0; i < sz.n_elements; i++) { 
		/* Outflow metallicity for each element */ 
		fprintf(sz.history_writer, 
			"#\t%d: z_out(%s)\t\t\tOutflow %s metallicity\n", 
			n, (*sz.elements[i]).symbol, (*sz.elements[i]).symbol); 
		n++; 
	} 
	for (i = 0; i < sz.n_elements; i++) { 
		/* ISM mass of each element in Msun */ 
		fprintf(sz.history_writer, 
			"#\t%d: mass(%s) [Msun]\t\tmass of element %s in ISM\n", 
			n, (*sz.elements[i]).symbol, (*sz.elements[i]).symbol); 
		n++; 
	} 

} 

/* 
 * Write output to the history.out file at the current timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE struct for the current simulation 
 * 
 * header: io.h 
 */ 
extern void write_history_output(SINGLEZONE sz) {

	/* 
	 * Change Notes 
	 * ============ 
	 * Calculation of ISM metallicities now moved to output handling functions. 
	 * The primary motivation for this was to remove overhead from calculating 
	 * and recording every [X/Y] combination of abundance ratios. VICE still 
	 * does this automatically, but from the output instead of during 
	 * simulation. This significantly improves the speed of simulations with 
	 * high n_elements. 
	 */ 

	/* 
	 * Write the evolutionary parameters 
	 * 
	 * Notes 
	 * ===== 
	 * Factor of 1e9 on star formation rate, infall rate, and outflow rate 
	 * converts from Msun/Gyr to Msun/yr to report quantities in conventional 
	 * units. 
	 * 
	 * mass_recycled expected a second argument of type ELEMENT *, but 
	 * determines the total ISM mass recycled in the case of NULL. 
	 */ 
	fprintf(sz.history_writer, "%e\t", sz.current_time); 
	fprintf(sz.history_writer, "%e\t", (*sz.ism).mass); 
	fprintf(sz.history_writer, "%e\t", get_stellar_mass(sz)); 
	fprintf(sz.history_writer, "%e\t", (*sz.ism).star_formation_rate / 1e9); 
	fprintf(sz.history_writer, "%e\t", (*sz.ism).infall_rate / 1e9); 
	fprintf(sz.history_writer, "%e\t", get_outflow_rate(sz) / 1e9); 
	fprintf(sz.history_writer, "%e\t", (*sz.ism).eta[sz.timestep]); 
	if ((*sz.ssp).continuous) { 
		/* effective recycling factor in case of continuous recycling */ 
		fprintf(sz.history_writer, "%e\t", mass_recycled(sz, NULL) / 
			((*sz.ism).star_formation_rate * sz.dt)); 
	} else { 
		/* instantaneous recycling parameter otherwise */ 
		fprintf(sz.history_writer, "%e\t", (*sz.ssp).R0); 
	} 
	unsigned int i;
	for (i = 0; i < sz.n_elements; i++) {
		/* infall metallicity */ 
		fprintf(sz.history_writer, "%e\t", (*sz.elements[i]).Zin[sz.timestep]); 
	} 
	for (i = 0; i < sz.n_elements; i++) { 
		/* outflow metallicity = enhancement factor x ISM metallicity */ 
		fprintf(sz.history_writer, "%e\t", 
			(*sz.ism).enh[sz.timestep] * (*sz.elements[i]).Z[sz.timestep]); 
	} 
	for (i = 0; i < sz.n_elements; i++) {
		/* total ISM mass of each element */ 
		fprintf(sz.history_writer, "%e\t", (*sz.elements[i]).mass); 
	} 
	fprintf(sz.history_writer, "\n"); 

} 

/* 
 * Writes the header to the mdf output file. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * header: io.h 
 */ 
extern void write_mdf_header(SINGLEZONE sz) { 

	/* 
	 * The first two columns are the bin edges. Subsequent columns are the 
	 * probability densities of stars in that [X/H] logarithmic abundance, and 
	 * subsequent columns thereafter are the probability densities of stars in 
	 * that [X/Y] logarithmic abundance ratio for each combination of elements. 
	 */ 

	unsigned int i, j; 
	fprintf(sz.mdf_writer, "# bin_edge_left\tbin_edge_right\t"); 
	for (i = 0; i < sz.n_elements; i++) {
		fprintf(sz.mdf_writer, "dN/d[%s/H]\t", (*sz.elements[i]).symbol); 
	} 
	for (i = 1; i < sz.n_elements; i++) {
		for (j = 0; j < i; j++) {
			fprintf(sz.mdf_writer, "dN/d[%s/%s]\t", 
				(*sz.elements[i]).symbol, (*sz.elements[j]).symbol); 
		} 
	} 
	fprintf(sz.mdf_writer, "\n"); 

}

/* 
 * Write to the mdf.out output file at the final timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * header: io.h 
 */ 
extern void write_mdf_output(SINGLEZONE sz) {
 
 	/* n: The number of abundance ratios reported */ 
	unsigned int j;
	unsigned long i, n = (unsigned long) (sz.n_elements * 
		(sz.n_elements - 1) / 2); 
	for (i = 0l; i < (*sz.mdf).n_bins; i++) { 
		fprintf(sz.mdf_writer, "%e\t%e\t", (*sz.mdf).bins[i], 
			(*sz.mdf).bins[i + 1l]); 
		for (j = 0; j < sz.n_elements; j++) {
			fprintf(sz.mdf_writer, "%e\t", 
				(*sz.mdf).abundance_distributions[j][i]); 
		} 
		for (j = 0; j < n; j++) {
			fprintf(sz.mdf_writer, "%e\t", 
				(*sz.mdf).ratio_distributions[j][i]); 
		} 
		fprintf(sz.mdf_writer, "\n"); 
	} 

} 

/* 
 * Opens the tracers output file at the end of a multizone simulation. 
 * 
 * Parameters 
 * ========== 
 * mz: 			A pointer to the multizone object 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: io.h 
 */ 
extern unsigned short multizone_open_tracer_file(MULTIZONE *mz) {

	if ((*(*mz).mig).tracers_output == NULL) {
		char filename[MAX_FILENAME_SIZE]; 
		strcpy(filename, (*mz).name); 
		strcat(filename, "/tracers.out"); 
		mz -> mig -> tracers_output = fopen(filename, "w"); 
	} else {} 
	return (*(*mz).mig).tracers_output == NULL; 

} 

/* 
 * Writes the header to the tracers output file at the end of a multizone 
 * simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object 
 * 
 * header: io.h 
 */ 
extern void write_tracers_header(MULTIZONE mz) {

	/* 
	 * Change Notes 
	 * ============ 
	 * Tracer output expanded to contain the mass and metallicity of each 
	 * tracer particle along with the formation time and initial and final 
	 * zone numbers. 
	 */ 

	fprintf((*mz.mig).tracers_output, "# COLUMN NUMBERS: \n"); 
	fprintf((*mz.mig).tracers_output, "#\t0: Formation_time [Gyr]\n"); 
	fprintf((*mz.mig).tracers_output, "#\t1: Zone_origin\n"); 
	fprintf((*mz.mig).tracers_output, "#\t2: Zone_final\n"); 
	fprintf((*mz.mig).tracers_output, "#\t3: Mass [Msun]\n"); 

	unsigned int i, n = 4; 
	for (i = 0; i < (*mz.zones[0]).n_elements; i++) {
		fprintf((*mz.mig).tracers_output, "#\t%d: Z(%s)\n", n, 
			(*(*mz.zones[0]).elements[i]).symbol); 
		n++; 
	} 

} 

/* 
 * Writes the tracer data to the output file at the end of a multizone 
 * simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 			The multizone object 
 * 
 * header: io.h 
 */ 
extern void write_tracers_output(MULTIZONE mz) {

	/* 
	 * Change Notes 
	 * ============ 
	 * Tracer output expanded to contain the mass and metallicity of each 
	 * tracer particle along with the formation time and initial and final 
	 * zone numbers. 
	 */ 

	if (mz.verbose) printf("Saving tracer particle data....\n"); 
	unsigned long i; 
	for (i = 0l; i < (*mz.mig).tracer_count; i++) { 
		FILE *out = (*mz.mig).tracers_output; 
		TRACER t = *(*mz.mig).tracers[i]; 
		SINGLEZONE origin = *(mz.zones[t.zone_origin]); 

		/* Formation time, final and origin zones, and mass in Msun */ 
		fprintf(out, "%e\t", t.timestep_origin * origin.dt); 
		fprintf(out, "%u\t", t.zone_origin); 
		fprintf(out, "%u\t", t.zone_current); 
		fprintf(out, "%e\t", t.mass); 

		/* Metallicity by mass of each element in the simulation */ 
		unsigned int j; 
		for (j = 0; j < origin.n_elements; j++) {
			fprintf(out, "%e\t", (*origin.elements[j]).Z[t.timestep_origin]); 
		} 
		fprintf(out, "\n"); 

		if (mz.verbose) {
			printf("Progress: %.1f%%\r", 
				100.0 * (i + 1) / (*mz.mig).tracer_count); 
		} 
	} 
	if (mz.verbose) printf("\n"); 

} 

/* 
 * Closes the tracer output file at the end of a multizone simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 			A pointer to the multizone object 
 * 
 * header: io.h 
 */ 
extern void multizone_close_tracer_file(MULTIZONE *mz) {

	if ((*(*mz).mig).tracers_output != NULL) {
		fclose(mz -> mig -> tracers_output); 
		mz -> mig -> tracers_output = NULL; 
	} else {} 

} 

