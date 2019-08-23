/* 
 * This file implements the core routines of the fromfile object. 
 */ 

#include <stdlib.h> 
#include <string.h> 
#include "fromfile.h" 
#include "io.h" 

/* ---------- static function comment headers not duplicated here ---------- */
static int fromfile_column_number(FROMFILE *ff, char *label); 

/* 
 * Allocate memory and return a pointer to a fromfile object. Automatically 
 * allocates memory for the name of the file. 
 * 
 * header: fromfile.h 
 */ 
extern FROMFILE *fromfile_initialize(void) {

	FROMFILE *ff = (FROMFILE *) malloc (sizeof(FROMFILE)); 
	ff -> name = (char *) malloc (MAX_FILENAME_SIZE * sizeof(char)); 
	ff -> n_rows = 0l; 
	ff -> n_cols = 0; 
	ff -> labels = NULL; 
	ff -> data = NULL; 
	return ff; 

} 

/* 
 * Free up the memory stored in a fromfile object. 
 * 
 * header: fromfile.h 
 */ 
extern void fromfile_free(FROMFILE *ff) {

	if (ff != NULL) {

		if ((*ff).name != NULL) {
			free(ff -> name); 
			ff -> name = NULL; 
		} else {} 

		if ((*ff).labels != NULL) { 
			/* Each label has memory that likely needs freed */ 
			unsigned int i; 
			for (i = 0; i < (*ff).n_cols; i++) {
				if ((*ff).labels[i] != NULL) {
					free(ff -> labels[i]); 
					ff -> labels[i] = NULL; 
				} else {
					continue; 
				} 
			} 
			free(ff -> labels); 
			ff -> labels = NULL; 
		} else {}

		if ((*ff).data != NULL) {
			free(ff -> data); 
			ff -> data = NULL; 
		} else {} 

		free(ff); 
		ff = NULL; 

	} else {} 

} 

/* 
 * Read in the data in a file into the fromfile object 
 * 
 * Parameters 
 * ========== 
 * ff: 		A pointer to the fromfile object 
 * 
 * Returns 
 * ======= 
 * 0 on success from reading the file; 1 on failure 
 * 
 * header: fromfile.h 
 */ 
extern unsigned short fromfile_read(FROMFILE *ff) {

	/* Use file I/O subroutines in io.h to error check the file */ 
	int dimension = file_dimension((*ff).name); 

	switch (dimension) {

		case -1: 
			return 1; 

		default: 
			ff -> n_cols = (unsigned) dimension; 
			ff -> n_rows = (unsigned long) (
				line_count((*ff).name) - header_length((*ff).name)
			); 

			switch ((*ff).n_rows) {
				case 0: 
					ff -> n_cols = 0; 
					return 1; 
				default: 
					ff -> data = read_square_ascii_file((*ff).name); 
					return 0; 
			}

	}

	#if 0
	if (dimension == -1) {
		return 1; 
	} else { 
		ff -> n_cols = (unsigned) dimension; 
		ff -> n_rows = (unsigned long) (
			line_count((*ff).name) - header_length((*ff).name)
		); 
		if ((*ff).n_rows == 0) {
			ff -> n_cols = 0; 
			return 1; 
		} else { 
			ff -> data = read_square_ascii_file((*ff).name); 
			return 0; 
		} 
	} 
	#endif 

}

/* 
 * Pull a column from the fromfile object based on its label. 
 * 
 * Parameters 
 * ========== 
 * ff: 		The fromfile object itself 
 * label: 	The label of the column to pull 
 * 
 * Returns 
 * ======= 
 * A double pointer to that column of the data; NULL if the label is not found. 
 * 
 * header: fromfile.h 
 */ 
extern double *fromfile_column(FROMFILE *ff, char *label) {

	int col = fromfile_column_number(ff, label); 
	unsigned long i; 
	double *column; 

	switch (col) {

		case -1: 
			return NULL; 

		default: 
			column = (double *) malloc ((*ff).n_rows * sizeof(double)); 
			for (i = 0l; i < (*ff).n_rows; i++) {
				column[i] = (*ff).data[i][col]; 
			} 
			return column; 

	}

	#if 0
	int col = fromfile_column_number(ff, label); 
	if (col != -1) { 
		unsigned long i; 
		double *column = (double *) malloc ((*ff).n_rows * sizeof(double)); 
		for (i = 0l; i < (*ff).n_rows; i++) { 
			column[i] = (*ff).data[i][col]; 
		} 
		return column; 
	} else { 
		return NULL; 
	}
	#endif 

} 

/* 
 * Modify a column of the data in a fromfile object 
 * 
 * Parameters 
 * ========== 
 * ff: 		A pointer to the fromfile object 
 * label: 	The label of the column to modify 
 * arr: 	The new array to put in place of the old column. Assumed to be of 
 * 			length (*ff).n_rows. 
 * 
 * Returns 
 * ======= 
 * 0 on success, 1 on failure 
 * 
 * header: fromfile.h 
 */ 
extern unsigned short fromfile_modify_column(FROMFILE *ff, char *label, 
	double *arr) {

	int column = fromfile_column_number(ff, label); 
	unsigned long i; 

	switch (column) {

		case -1: 
			/* automatically make a new column */ 
			return fromfile_new_column(ff, label, arr); 

		default: 
			for (i = 0l; i < (*ff).n_rows; i++) {
				ff -> data[i][column] = arr[i]; 
			} 
			return 0; 

	}

	#if 0 
	int column = fromfile_column_number(ff, label); 
	if (column != -1) {
		unsigned long i; 
		for (i = 0l; i < (*ff).n_rows; i++) {
			ff -> data[i][column] = arr[i]; 
		} 
		return 0; 
	} else { 
		/* Automatically make a new column */ 
		return fromfile_new_column(ff, label, arr); 
	} 
	#endif 

} 

/* 
 * Add a column to the data in a fromfile object. 
 * 
 * Parameters 
 * ========== 
 * ff: 		A pointer to the fromfile object 
 * label: 	The label to let the new column have 
 * arr: 	The new column itself 
 * 
 * Returns 
 * ======= 
 * 0 on success; 1 on failure 
 * 
 * header: fromfile.h 
 */ 
extern unsigned short fromfile_new_column(FROMFILE *ff, char *label, 
	double *arr) {

	unsigned long i; 
	switch (fromfile_column_number(ff, label)) {

		case -1: 
			/* Only assigned the new column if the label isn't recognized */ 
			ff -> labels = (char **) realloc (ff -> labels, 
				((*ff).n_cols + 1) * sizeof(char *)); 
			ff -> labels[(*ff).n_cols] = (char *) malloc ((strlen(label) + 1) * 
				sizeof(char)); 
			strcpy(ff -> labels[(*ff).n_cols], label); 
			for (i = 0l; i < (*ff).n_rows; i++) {
				ff -> data[i] = (double *) realloc (ff -> data[i], 
					((*ff).n_cols + 1) * sizeof(double)); 
				ff -> data[i][(*ff).n_cols] = arr[i]; 
			} 
			ff -> n_cols++; 
			return 0; 

		default: 
			return 1; 

	}

	#if 0
	if (fromfile_column_number(ff, label) == -1) {
		/* Only assign the new column if the label is not yet recognized */ 
		ff -> labels = (char **) realloc (ff -> labels, 
			((*ff).n_cols + 1) * sizeof(char *)); 
		ff -> labels[(*ff).n_cols] = (char *) malloc ((strlen(label) + 1) * 
			sizeof(char)); 
		strcpy(ff -> labels[(*ff).n_cols], label); 
		unsigned long i; 
		for (i = 0l; i < (*ff).n_rows; i++) {
			ff -> data[i] = (double *) realloc (ff -> data[i], 
				((*ff).n_cols + 1) * sizeof(double)); 
			ff -> data[i][(*ff).n_cols] = arr[i]; 
		} 
		ff -> n_cols++; 
		return 0; 
	} else {
		return 1; 
	} 
	#endif 

}

/* 
 * Obtain the column number of a given label in the data. Used for keying the 
 * data from a VICE dataframe wrapper. 
 * 
 * Parameters 
 * ========== 
 * ff: 		The fromfile object itself 
 * label: 	The label to key on 
 */ 
static int fromfile_column_number(FROMFILE *ff, char *label) {

	unsigned int i; 
	for (i = 0; i < (*ff).n_cols; i++) { 
		if (!strcmp((*ff).labels[i], label)) return (signed) i; 
	} 
	return -1; 

} 

/* 
 * Pull a row from the fromfile object based on its row number 
 * 
 * Parameters 
 * ========== 
 * ff: 		The fromfile object itself 
 * row: 	The row number of the data to pull 
 * 
 * Returns 
 * ======= 
 * A double pointer to that row of the data; NULL if the row number is outside 
 * the allowed range. 
 * 
 * header: fromfile.h 
 */ 
extern double *fromfile_row(FROMFILE *ff, unsigned long row) { 

	if (row < (*ff).n_rows) { 
		unsigned int i; 
		double *data = (double *) malloc ((*ff).n_cols * sizeof(double)); 
		for (i = 0; i < (*ff).n_cols; i++) { 
			data[i] = (*ff).data[row][i]; 
		} 
		return data; 
	} else { 
		return NULL; 
	}

} 

