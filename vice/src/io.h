
#ifndef IO_H 
#define IO_H 

#ifdef __cplusplus 
extern "C" {
#endif 

#ifndef LINESIZE 
#define LINESIZE 100000l 
#endif /* LINESIZE */ 

/* The maximum number of characters in the names of files */ 
#ifndef MAX_FILENAME_SIZE 
#define MAX_FILENAME_SIZE 10000l 
#endif /* MAX_FILENAME_SIZE */ 

#include "objects.h" 
#include "io/agb.h" 
#include "io/ccsne.h" 
#include "io/sneia.h" 
#include "io/utils.h" 

/* 
 * Open the history.out and mdf.out output files associated with a SINGLEZONE 
 * object. 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * source: io.c 
 */ 
extern unsigned short singlezone_open_files(SINGLEZONE *sz); 

/* 
 * Close the history.out and mdf.out output files associated with a SINGLEZONE 
 * object. 
 * 
 * source: io.c  
 */ 
extern void singlezone_close_files(SINGLEZONE *sz); 

/* 
 * Writes the header to the history file 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE object for the current simulation 
 * 
 * source: io.c 
 */ 
extern void write_history_header(SINGLEZONE sz); 

/* 
 * Write output to the history.out file at the current timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The SINGLEZONE struct for the current simulation 
 * 
 * source: io.c 
 */ 
extern void write_singlezone_history(SINGLEZONE sz); 

/* 
 * Writes history output for each zone in a multizone simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object to write output from 
 * 
 * source: io.c 
 */ 
extern void write_multizone_history(MULTIZONE mz); 

/* 
 * Writes the header to the mdf output file. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * source: io.c 
 */ 
extern void write_mdf_header(SINGLEZONE sz); 

/* 
 * Write to the mdf.out output file at the final timestep. 
 * 
 * Parameters 
 * ========== 
 * sz: 		The singlezone object for the current simulation 
 * 
 * source: io.c 
 */ 
extern void write_mdf_output(SINGLEZONE sz); 

/* 
 * Writes the stellar MDFs to all output files. 
 * 
 * Parameters 
 * ========== 
 * mz: 		The multizone object to write the MDF from 
 * 
 * source: io.c 
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
 * source: io.c 
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
 * source: io.c 
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
 * source: io.c 
 */ 
extern void write_tracers_output(MULTIZONE mz); 

/* 
 * Closes the tracer output file at the end of a multizone simulation 
 * 
 * Parameters 
 * ========== 
 * mz: 			A pointer to the multizone object 
 * 
 * source: io.c 
 */ 
extern void multizone_close_tracer_file(MULTIZONE *mz); 

#ifdef __cplusplus 
}
#endif 

#endif /* IO_H */ 

