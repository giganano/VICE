
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
 * source: io.c  
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
 * source: io.c 
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
 * source: io.c 
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
 * source: io.c  
 */ 
extern long line_count(char *file); 

/* 
 * Import a built-in AGB star yields grid. 
 * 
 * Parameters 
 * ========== 
 * e: 		A pointer to the element struct to import the grid into 
 * file: 	The name of the file containing the AGB yield grid. These are 
 * 			include in VICE's data directory, and direct user access to them 
 * 			is strongly discouraged. 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on failure 
 * 
 * source: io.c  
 */ 
extern int import_agb_grid(ELEMENT *e, char *file); 

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
 * source: io.c  
 */ 
extern double **cc_yield_grid(char *file); 

/* 
 * Lookup the mass yield of a given element from type Ia supernovae 
 * 
 * Parameters 
 * ========== 
 * file: 		The name of the yield file, passed from python 
 * 
 * Returns 
 * ======= 
 * The total mass yield in Msun of the given element reported by the built-in 
 * study's data 
 * 
 * source: io.c  
 */ 
extern double single_ia_mass_yield_lookup(char *file); 

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
extern int singlezone_open_files(SINGLEZONE *sz); 

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
extern void write_history_output(SINGLEZONE sz); 

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
extern int multizone_open_tracer_file(MULTIZONE *mz); 

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

