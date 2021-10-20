/*
 * Implements testing of the file I/O utility functions at vice/src/io/utils.h
 */

#include <stdlib.h>
#include <stdio.h>
#include "../../io/utils.h"
#include "utils.h"

/* ---------- static function comment headers not duplicated here ---------- */
static unsigned short spawn_test_file(void);
static unsigned short destroy_test_file(void);
static unsigned short test_file_ijth_qty(unsigned short i, unsigned short j);

/*
 * TEST_FILE_LENGTH: 		The number of lines of output to put in a test file
 * TEST_FILE_DIMENSION: 	The number of columns of output to put in a test
 * 							file
 */
static unsigned short TEST_FILE_LENGTH = 10u;
static unsigned short TEST_FILE_DIMENSION = 5u;
static char TEST_FILE_NAME[] = "vice_test_file.txt";


/*
 * Test the square ascii file reader at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_read_square_ascii_file(void) {

	if (spawn_test_file()) {
		unsigned short i, j;
		double **test = read_square_ascii_file(TEST_FILE_NAME);
		for (i = 0u; i < TEST_FILE_LENGTH; i++) {
			for (j = 0u; j < TEST_FILE_DIMENSION; j++) {
				if (test[i][j] != test_file_ijth_qty(i, j)) {
					free(test);
					destroy_test_file();
					return 0u;
				} else {}
			}
		}
		free(test);
		return destroy_test_file();
	} else {
		return 0u;
	}

}


/*
 * Test the header length function at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_header_length(void) {

	if (spawn_test_file()) {
		if (header_length(TEST_FILE_NAME) == 1) {
			return destroy_test_file();
		} else {
			destroy_test_file();
			return 0u;
		}
	} else {
		return 0u;
	}

}


/*
 * Test the file dimension function at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_file_dimension(void) {

	if (spawn_test_file()) {
		if (file_dimension(TEST_FILE_NAME) == TEST_FILE_DIMENSION) {
			return destroy_test_file();
		} else {
			destroy_test_file();
			return 0u;
		}
	} else {
		return 0u;
	}

}


/*
 * Test the file line counter at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * header: utils.h
 */
extern unsigned short test_line_count(void) {

	if (spawn_test_file()) {
		if (line_count(TEST_FILE_NAME) == 1l + TEST_FILE_LENGTH) {
			return destroy_test_file();
		} else {
			destroy_test_file();
			return 0u;
		}
	} else {
		return 0u;
	}

}


/*
 * Create a test file
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
		fprintf(test, "# This is a test header\n");
		for (i = 0u; i < TEST_FILE_LENGTH; i++) {
			for (j = 0u; j < TEST_FILE_DIMENSION; j++) {
				fprintf(test, "%u\t", test_file_ijth_qty(i, j));
			}
			fprintf(test, "\n");
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
 * 1 on success, 0 on failure to remove the test file
 */
static unsigned short destroy_test_file(void) {

	return !remove(TEST_FILE_NAME);

}


/*
 * Generate dummy quantity to write as the ij'th quantity of a test file
 *
 * Parameters
 * ==========
 * i: 		The row number
 * j: 		The column number
 *
 * Returns
 * =======
 * A dummy quantity as a function of i and j
 */
static unsigned short test_file_ijth_qty(unsigned short i, unsigned short j) {

	return (i + 1) * (j + 1);

}

