
#ifndef IO_UTILS_H
#define IO_UTILS_H

#ifdef __cpluslus
extern "C" {
#endif /* __cplusplus */

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
 * source: utils.c
 */
extern double **read_square_ascii_file(char *file);

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
 * source: utils.c
 */
extern int header_length(char *file);

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
 * source: utils.c
 */
extern int file_dimension(char *file);

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
 * source: utils.c
 */
extern long line_count(char *file);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_UTILS_H */
