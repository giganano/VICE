/*
 * This file implements file I/O for the singlezone object.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../singlezone.h"
#include "../utils.h"
#include "../ism.h"
#include "../ssp.h"
#include "../io.h"
#include "singlezone.h"

/*
 * Open the history.out and mdf.out output files associated with a SINGLEZONE
 * object.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * header: singlezone.h
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
 * header: singlezone.h
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
 * header: singlezone.h
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
 * mstar: 	The stellar mass in the zone. This will differ between singlezone
 * 			and multizone simulations due to stellar migration.
 *
 * header: singlezone.h
 */
extern void write_singlezone_history(SINGLEZONE sz) {

	double *unretained = singlezone_unretained(sz);
	write_zone_history(sz, singlezone_stellar_mass(sz), mass_recycled(sz, NULL),
		unretained);
	free(unretained);

}

/*
 * Write a zone's history output, either in a singlezone simulation or
 * embedded in a multizone object.
 *
 * Parameters
 * ==========
 * sz: 				The singlezone object associated with the zone
 * mstar: 			The stellar mass in the zone
 * mass_recycled: 	The recycled mass in the zone
 * unretained: 		The amount of mass unretained in the given zone for each
 * 					element
 *
 * header: singlezone.h
 */
extern void write_zone_history(SINGLEZONE sz, double mstar,
	double mass_recycled, double *unretained) {

	/*
	 * Change Notes
	 * ============
	 * Calculation of ISM metallicities now moved to output handling functions.
	 * The primary motivation for this was to remove overhead from calculating
	 * and recording every [X/Y] combination of abundance ratios. VICE still
	 * does this automatically, but from the output instead of during
	 * simulation. This significantly improves the speed of simulations with
	 * high n_elements.
	 *
	 * This function has been generalized to write the output for a given zone
	 * in both singlezone and multizone models. The parameters which may be
	 * different between the two not already accessible via their structs are
	 * accepted as parameters here.
	 */

	/*
	 * Write the evolutionary parameters
	 *
	 * Notes
	 * =====
	 * Factor of 1e9 on star formation rate, infall rate, and outflow rate
	 * converts from Msun/Gyr to Msun/yr to report quantities in conventional
	 * units.
	 */

	if (sz.current_time < sz.output_times[sz.n_outputs - 1l] + sz.dt) {

		/*
		 * Only write output if the time is actually in the window the user
		 * specified. Although it's a minor issue, this will prevent extra
		 * timesteps from being written to the output file.
		 */

		fprintf(sz.history_writer, "%e\t", sz.current_time);
		fprintf(sz.history_writer, "%e\t", (*sz.ism).mass);
		fprintf(sz.history_writer, "%e\t", mstar);
		fprintf(sz.history_writer, "%e\t", (*sz.ism).star_formation_rate / 1e9);
		fprintf(sz.history_writer, "%e\t", (*sz.ism).infall_rate / 1e9);
		fprintf(sz.history_writer, "%e\t",
			(get_outflow_rate(sz) + sum(unretained, sz.n_elements)) / 1e9);
		fprintf(sz.history_writer, "%e\t", (*sz.ism).eta[sz.timestep]);
		if ((*sz.ssp).continuous) {
			/* effective recycling factor in case of continuous recycling */
			fprintf(sz.history_writer, "%e\t", mass_recycled /
				((*sz.ism).star_formation_rate * sz.dt));
		} else {
			/* instantaneous recycling parameter otherwise */
			fprintf(sz.history_writer, "%e\t", (*sz.ssp).R0);
		}
		unsigned int i;
		for (i = 0; i < sz.n_elements; i++) {
			/* infall metallicity */
			fprintf(sz.history_writer, "%e\t",
				(*sz.elements[i]).Zin[sz.timestep]);
		}
		for (i = 0; i < sz.n_elements; i++) {
			/* outflow metallicity = enhancement factor x ISM metallicity */
			fprintf(sz.history_writer, "%e\t",
				((*sz.ism).enh[sz.timestep] * (*sz.elements[i]).Z[sz.timestep] *
					get_outflow_rate(sz) + unretained[i]) /
				(get_outflow_rate(sz) + sum(unretained, sz.n_elements)));
		}
		for (i = 0; i < sz.n_elements; i++) {
			/* total ISM mass of each element */
			fprintf(sz.history_writer, "%e\t", (*sz.elements[i]).mass);
		}
		fprintf(sz.history_writer, "\n");

	} else {}

}

/*
 * Writes the header to the mdf output file.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * header: singlezone.h
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
 * header: singlezone.h
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

