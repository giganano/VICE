/*
 * This file implements testing of the CCSNe file I/O functions at
 * vice/src/io/ccsne.h
 */

#include <stdlib.h>
#include <stdio.h>
#include "../../io/ccsne.h"
#include "ccsne.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short spawn_test_file(void);
static unsigned short destroy_test_file(void);


static char TEST_FILE_NAME[] = "vice_test_cc_grid_file.txt";
static unsigned short TEST_N_MASSES = 6;
static unsigned short TEST_N_ISOTOPES = 3;
static double *MASSES;

/*
 * Test the CCSN yield grid reader at vice/src/io/ccsne.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: ccsne.h
 */
extern unsigned short test_cc_yield_grid(void) {

	if (spawn_test_file()) {
		double **test = cc_yield_grid(TEST_FILE_NAME);
		unsigned short i, result = 1u;
		for (i = 0u; i < TEST_N_MASSES; i++) {
			if (test[i][0] != MASSES[i] && test[i][1] != TEST_N_ISOTOPES) {
				result = 0u;
				break;
			} else {}
		}
		free(MASSES);
		free(test);
		destroy_test_file();
		return result;
	} else {
		return 0u;
	}

}


/*
 * Create the test file
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short spawn_test_file(void) {

	FILE *test = fopen(TEST_FILE_NAME, "w");
	if (test != NULL) {
		MASSES = (double *) malloc (TEST_N_MASSES * sizeof(double));
		unsigned short i, j;
		for (i = 0u; i < TEST_N_MASSES; i++) {
			MASSES[i] = 10 * (i + 1);
			fprintf(test, "%g\t", MASSES[i]);
			for (j = 0u; j < TEST_N_ISOTOPES; j++) {
				fprintf(test, "1\t");
			}
			fprintf(test, "\n");
		}
		fclose(test);
		return 1u;
	} else {
		return 0u;
	}

}


/*
 * Destroy the test file
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short destroy_test_file(void) {

	return !remove(TEST_FILE_NAME);

}

