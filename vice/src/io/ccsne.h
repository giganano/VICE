
#ifndef IO_CCSNE_H
#define IO_CCSNE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

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
 * source: ccsne.c
 */
extern double **cc_yield_grid(char *file);

/*
 * Read a yield table for CCSNe for a specific isotope.
 *
 * Parameters
 * ==========
 * file: 		The name of the file, passed from python.
 * iso: 		The isotope in question
 *
 * Returns
 * =======
 * Type **double:
 * 		returned[i][0]: initial stellar mass
 * 		returned[i][1]: total mass yield of the isotope
 * NULL on failure to read from the file
 *
 * source: ccsne.c
 */
extern double **cc_yield_grid_iso(char *file, char *iso);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_CCSNE_H */

