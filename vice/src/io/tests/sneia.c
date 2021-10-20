/*
 * This file implements testing of the type Ia supernova yield lookup
 * at vice/src/io/sneia.h
 */

#include <stdio.h>
#include "../../io/sneia.h"
#include "sneia.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short spawn_test_file(void);
static unsigned short destroy_test_file(void);

static unsigned short TEST_N_ISOTOPES = 3;
static char TEST_FILE_NAME[] = "vice_test_sneia_yield_file.txt";


/*
 * Test the function which looks up the mass yield from a single SN Ia
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: sneia.h
 */
extern unsigned short test_single_ia_mass_yield_lookup(void) {

	if (spawn_test_file()) {
		double result = single_ia_mass_yield_lookup(TEST_FILE_NAME);
		destroy_test_file();
		return result == TEST_N_ISOTOPES;
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
		unsigned short i;
		fprintf(test, "# Test header\n");
		for (i = 0u; i < TEST_N_ISOTOPES; i++) {
			fprintf(test, "test%u\t1\n", i + 1u);
		}
		fprintf(test, "\n");
		fclose(test);
		return 1u;
	} else {
		return 0u;
	}

}


/*
 * Destroys the test file
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 */
static unsigned short destroy_test_file(void) {

	return !remove(TEST_FILE_NAME);

}

