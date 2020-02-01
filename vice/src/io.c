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
	double *unretained = singlezone_unretained(sz); 
	for (i = 0; i < sz.n_elements; i++) { 
		/* outflow metallicity = enhancement factor x ISM metallicity */ 
		fprintf(sz.history_writer, "%e\t", 
			// (*sz.ism).enh[sz.timestep] * (*sz.elements[i]).Z[sz.timestep]); 
			(*sz.ism).enh[sz.timestep] * (*sz.elements[i]).Z[sz.timestep] + 
			unretained[i] / get_outflow_rate(sz)); 
	} 
	free(unretained); 
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

