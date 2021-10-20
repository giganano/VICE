
#ifndef IO_MULTIZONE_H
#define IO_MULTIZONE_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../objects.h"

/*
 * Writes history output for each zone in a multizone simulation
 *
 * Parameters
 * ==========
 * mz: 		The multizone object to write output from
 *
 * source: multizone.c
 */
extern void write_multizone_history(MULTIZONE mz);

/*
 * Writes the stellar MDFs to all output files.
 *
 * Parameters
 * ==========
 * mz: 		The multizone object to write the MDF from
 *
 * source: multizone.c
 */
extern void write_multizone_mdf(MULTIZONE mz);

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
 * source: multizone.c
 */
extern unsigned short multizone_open_tracer_file(MULTIZONE *mz);

/*
 * Writes the header to the tracers output file at the end of a multizone
 * simulation
 *
 * Parameters
 * ==========
 * mz: 			The multizone object
 *
 * source: multizone.c
 */
extern void write_tracers_header(MULTIZONE mz);

/*
 * Writes the tracer data to the output file at the end of a multizone
 * simulation
 *
 * Parameters
 * ==========
 * mz: 			The multizone object
 *
 * source: multizone.c
 */
extern void write_tracers_output(MULTIZONE mz);

/*
 * Closes the tracer output file at the end of a multizone simulation
 *
 * Parameters
 * ==========
 * mz: 			A pointer to the multizone object
 *
 * source: multizone.c
 */
extern void multizone_close_tracer_file(MULTIZONE *mz);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IO_MULTIZONE_H */
