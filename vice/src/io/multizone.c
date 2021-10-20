/*
 * This file implements file I/O for the multizone object.
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../io.h"
#include "../multizone.h"
#include "../ssp.h"
#include "../ism.h"
#include "multizone.h"
#include "progressbar.h"

/*
 * Writes history output for each zone in a multizone simulation
 *
 * Parameters
 * ==========
 * mz: 		The multizone object to write output from
 *
 * header: multizone.h
 */
extern void write_multizone_history(MULTIZONE mz) {

	unsigned int i;
	double *mstar = multizone_stellar_mass(mz);
	double *recycled = gas_recycled_in_zones(mz);
	double **unretained = multizone_unretained(mz);
	for (i = 0u; i < (*mz.mig).n_zones; i++) {
		write_zone_history(*mz.zones[i], mstar[i], recycled[i], unretained[i]);
	}
	free(unretained);
	free(mstar);
	free(recycled);

}

/*
 * Writes the stellar MDFs to all output files.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object to write the MDF from
 *
 * header: multizone.h
 */
extern void write_multizone_mdf(MULTIZONE mz) {

	unsigned int i;
	for (i = 0u; i < (*mz.mig).n_zones; i++) {
		write_mdf_output(*mz.zones[i]);
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
 * header: multizone.h
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
 * header: multizone.h
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
 * header: multizone.h
 */
extern void write_tracers_output(MULTIZONE mz) {

	/*
	 * Change Notes
	 * ============
	 * Tracer output expanded to contain the mass and metallicity of each
	 * tracer particle along with the formation time and initial and final
	 * zone numbers.
	 */

	PROGRESSBAR *pb;
	if (mz.verbose) {
		printf("Saving star particle data....\n");
		pb = progressbar_initialize((*mz.mig).tracer_count);
	} else {}
	unsigned long i;
	for (i = 0l; i < (*mz.mig).tracer_count; i++) {
		FILE *out = (*mz.mig).tracers_output;
		TRACER t = *(*mz.mig).tracers[i];
		SINGLEZONE origin = *(mz.zones[t.zone_origin]);

		/*
		 * If the tracer particle formed **before** the user's specified
		 * final output time.
		 */
		if (t.timestep_origin * origin.dt <=
			origin.output_times[origin.n_outputs - 1l]) {

			/* Formation time, final and origin zones, and mass in Msun */
			fprintf(out, "%e\t", t.timestep_origin * origin.dt);
			fprintf(out, "%u\t", t.zone_origin);
			fprintf(out, "%u\t", t.zone_current);
			fprintf(out, "%e\t", t.mass);

			/* Metallicity by mass of each element in the simulation */
			unsigned int j;
			for (j = 0; j < origin.n_elements; j++) {
				fprintf(out, "%e\t",
					(*origin.elements[j]).Z[t.timestep_origin]);
			}
			fprintf(out, "\n");

		/*
		 * Otherwise don't include it in the output.
		 */
		} else {}

		if (mz.verbose) progressbar_update(pb, i + 1ul);
	}
	if (mz.verbose) {
		progressbar_finish(pb);
		progressbar_free(pb);
	} else {}

}

/*
 * Closes the tracer output file at the end of a multizone simulation
 *
 * Parameters
 * ==========
 * mz: 			A pointer to the multizone object
 *
 * header: multizone.h
 */
extern void multizone_close_tracer_file(MULTIZONE *mz) {

	if ((*(*mz).mig).tracers_output != NULL) {
		fclose(mz -> mig -> tracers_output);
		mz -> mig -> tracers_output = NULL;
	} else {}

}

