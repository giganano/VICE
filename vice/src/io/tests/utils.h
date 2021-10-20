
#ifndef TESTS_IO_UTILS_H
#define TESTS_IO_UTILS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * Test the square ascii file reader at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_read_square_ascii_file(void);

/*
 * Test the header length function at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_header_length(void);

/*
 * Test the file dimension function at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_file_dimension(void);

/*
 * Test the file line counter at vice/src/io/utils.h
 *
 * Returns
 * =======
 * 1 on success, 0 on failure
 *
 * source: utils.c
 */
extern unsigned short test_line_count(void);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* TESTS_IO_UTILS_H */
