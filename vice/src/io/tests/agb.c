/*
 * This file implements testing of the AGB star file I/O functions at
 * vice/src/io/agb.h
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../../io.h"
#include "agb.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short spawn_test_file(void);
static unsigned short destroy_test_file(void);

/*
 * TEST_N_M: 		The number of masses on the test AGB file
 * TEST_N_Z: 		The number of metallicities on the test AGB grid
 * TEST_FILE_NAME: 	The name of the test AGB grid file
 */
static unsigned short TEST_N_M = 5;
static unsigned short TEST_N_Z = 10;
static char TEST_FILE_NAME[] = "vice_test_agb_yield_file.txt";

/*
 * Test the import_agb_grid function at vice/src/io/agb.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: agb.h
 */
extern unsigned short test_import_agb_grid(void) {

	ELEMENT *test = element_initialize();
	if (test != NULL) {
		if (spawn_test_file()) {

			if (!import_agb_grid(test, TEST_FILE_NAME)) {

				INTERP_SCHEME_2D is2d = *(*(*test).agb_grid).interpolator;
				if (is2d.n_x_values == TEST_N_M &&
					is2d.n_y_values == TEST_N_Z &&
					is2d.xcoords != NULL &&
					is2d.ycoords != NULL &&
					is2d.zcoords != NULL) {

					unsigned short i, j, result = 1u;
					for (i = 0u; i < TEST_N_M; i++) {
						result &= is2d.xcoords[i] == i + 1u;
						if (!result) break;
					}
					for (i = 0u; i < TEST_N_Z; i++) {
						result &= is2d.ycoords[i] == 0.01 * i;
						if (!result) break;
					}
					for (i = 0u; i < TEST_N_M; i++) {
						for (j = 0u; j < TEST_N_Z; j++) {
							result &= is2d.zcoords[i][j] == 0.001;
							if (!result) break;
						}
					}

					element_free(test);
					if (result) return destroy_test_file();
					return 0u;

				} else {
					element_free(test);
					destroy_test_file();
					return 0u;
				}

			} else {
				element_free(test);
				destroy_test_file();
				return 0u;
			}
		} else {
			element_free(test);
			return 0u;
		}
	} else {
		return 0u;
	}

}


/*
 * Spawns the test yield file
 *
 * Returns
 * =======
 * 1 on success, 0 on failure to create the test file
 */
static unsigned short spawn_test_file(void) {

	FILE *test = fopen(TEST_FILE_NAME, "w");
	if (test == NULL) {
		return 0u;
	} else {
		unsigned short i, j;
		for (i = 0u; i < TEST_N_M; i++) {
			for (j = 0u; j < TEST_N_Z; j++) {
				fprintf(test, "%u\t%lf\t0.001\n", i + 1, 0.01 * j);
			}
		}
		fclose(test);
		return 1u;
	}

}


/*
 * Destroy the test file
 *
 * Returns
 * =======
 * 1 on success, 0 on failure to destroy the test file
 */
static unsigned short destroy_test_file(void) {

	return !remove(TEST_FILE_NAME);

}

