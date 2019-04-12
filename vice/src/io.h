/*
 * This file, included with the VICE package, is protected under the terms of 
 * the associated MIT License, and any use or redistribution of this file in 
 * original or altered form is subject to the copyright terms therein. 
 * 
 * The header contains extern declarations for functions which handle 
 * VICE's file I/O. 
 */

#ifndef IO_H
#define IO_H

#include "specs.h" /* <------- Need INTEGRATION and MODEL structs */ 



/* --------------------- FILE UTILITY FUNCTIONS ----------------------- */

/* 
 * Opens the output files for writing throughout the execution 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for the current execution
 * file1:			The name of the file holding the history output
 * file2:			The name of the file holding the mdf output
 * file3:			The name of the file holding the breakdown output 
 * 
 * source: writers.c  
 */
extern int open_files(INTEGRATION *run, char *name);

/*
 * Closes all of the output files at the end of the INTEGRATION 
 * 
 * Args:
 * =====
 * run:				The INTEGRATION struct for the current execution. 
 * 
 * source: writers.c 
 */
extern void close_files(INTEGRATION *run);









/* ----------------- WRITING FUNCTIONS ------------------ */

/*
 * Writes the header to the history file 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution
 * m:			The MODEL struct for the current execution. 
 * 
 * source: writers.c 
 */
extern void write_history_header(INTEGRATION run, MODEL m);

/*
 * Writes output to the history file at the current timestep. 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for the current execution.
 * m:			The MODEL struct for the current execution. 
 * 
 * source: writers.c 
 */
extern void write_history_output(INTEGRATION run, MODEL m);

/*
 * Writes the header to the mdf output file. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution. 
 * 
 * source: writers.c
 */
extern void write_mdf_header(INTEGRATION run);

/*
 * Writes output to the mdf output file at the final timestep. 
 * 
 * Args:
 * =====
 * run:		The INTEGRATION struct for the current execution.
 * m:			The MODEL struct for the current execution. 
 * 
 * source: writers.c 
 */
extern void write_mdf_output(INTEGRATION run, MODEL m);










/* ------------------ READING FUNCTIONS ------------------- */

/*
 * Reads the AGB grid for further expansion based on timestepping in the 
 * subroutines in agb.c 
 * 
 * Args:
 * =====
 * run:			The INTEGRATION struct for this iteration of the code
 * file:			The name of the file holding the grid
 * index:			The index of the element 
 * 
 * source readers.c 
 */
extern int read_agb_grid(INTEGRATION *run, char *file, int index);

/*
 * Reads in a square output file given the destination pointer to store it at 
 * in the memory, the file name, the dimensionality of the output, and the 
 * number of lines in the header. All of these parameters will be determined 
 * in python and the user will only need to specify the name of the previous 
 * INTEGRATION. 
 * 
 * Args:
 * =====
 * file:				The file holding the history output 
 * 
 * source: readers.c 
 */
extern double **read_output(char *file);

/*
 * Returns the number of lines in an ascii text file. 
 * 
 * Args:
 * =====
 * file:		The name of the file 
 * 
 * source: readers.c 
 */
extern long num_lines(char *file);

/* 
 * Determines the length of the header of an output file assuming the 
 * commenting character is '#' 
 * 
 * Args:
 * =====
 * file:		A character pointer to the name of the output file. 
 * 
 * source: readers.c 
 */
extern int header_length(char *file);

/*
 * Determines the dimensionality of the file off of the first line passed the 
 * header. 
 * 
 * Args:
 * =====
 * file:					The name of the file
 * header_length:			The number of lines in the header 
 * 
 * source: readers.c 
 */
extern int file_dimension(char *file, int hlength);

/*
 * Pulls the total yields off of the data file and returns them as a 2-D array 
 * where the zeroth column is the masses and the first column is the total 
 * yields of all isotopes at that stellar mass. 
 * 
 * Args:
 * =====
 * file: 		The name of the file containing the yield grid 
 * 
 * source: readers.c 
 */
extern double **yields(char *file);

/* 
 * Determines the gridsize -> The number of masses on which the yield grid is 
 * sampled. It does this simply by opening the file and seeing how many lines 
 * there are. 
 * 
 * Args: 
 * =====
 * file: 				The name of the file 
 * 
 * source: readers.c  
 */ 
extern int gridsize(char *file);


#endif /* IO_H */


 