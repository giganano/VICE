
#ifndef IO_SINGLEZONE_H
#define IO_SINGLEZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cpluslus */

#include "../objects.h"

/*
 * Open the history.out and mdf.out output files associated with a SINGLEZONE
 * object.
 *
 * Returns
 * =======
 * 0 on success, 1 on failure
 *
 * source: singlezone.c
 */
extern unsigned short singlezone_open_files(SINGLEZONE *sz);

/*
 * Close the history.out and mdf.out output files associated with a SINGLEZONE
 * object.
 *
 * source: singlezone.c
 */
extern void singlezone_close_files(SINGLEZONE *sz);

/*
 * Writes the header to the history file
 *
 * Parameters
 * ==========
 * sz: 		The SINGLEZONE object for the current simulation
 *
 * source: singlezone.c
 */
extern void write_history_header(SINGLEZONE sz);

/*
 * Write output to the history.out file at the current timestep.
 *
 * Parameters
 * ==========
 * sz: 		The SINGLEZONE struct for the current simulation
 *
 * source: singlezone.c
 */
extern void write_singlezone_history(SINGLEZONE sz);

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
 * source: singlezone.c
 */
extern void write_zone_history(SINGLEZONE sz, double mstar,
	double mass_recycled, double *unretained);

/*
 * Writes the header to the mdf output file.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * source: singlezone.c
 */
extern void write_mdf_header(SINGLEZONE sz);

/*
 * Write to the mdf.out output file at the final timestep.
 *
 * Parameters
 * ==========
 * sz: 		The singlezone object for the current simulation
 *
 * source: singlezone.c
 */
extern void write_mdf_output(SINGLEZONE sz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_SINGLEZONE_H */
