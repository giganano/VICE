/* 
 * This file implements a progressbar for VICE's terminal I/O. 
 */ 

#include <sys/ioctl.h> 
#include <sys/time.h> 
#include <stdlib.h> 
#include <string.h> 
#include <unistd.h> 
#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "progressbar.h" 
#include "../utils.h" 

/* ---------- Static function comment headers not duplicated here ---------- */ 
static void progressbar_print(PROGRESSBAR pb); 
static unsigned long progressbar_eta(PROGRESSBAR pb); 
static unsigned short window_width(void); 
static char *format_time(unsigned long seconds); 
static unsigned short n_digits(double value); 


/* 
 * Allocate memory for and return a pointer to a progressbar object. 
 * 
 * Parameters 
 * ==========
 * maxval: 		The total number of iterations before the operation using the 
 * 				progressbar is complete. 
 * 
 * header: progressbar.h 
 */ 
extern PROGRESSBAR *progressbar_initialize(unsigned long maxval) {

	PROGRESSBAR *pb = (PROGRESSBAR *) malloc (sizeof(PROGRESSBAR)); 
	pb -> left_hand_side = NULL; 
	pb -> right_hand_side = NULL; 
	pb -> custom_left_hand_side = 0u; 
	pb -> custom_right_hand_side = 0u; 
	pb -> eta_mode = 635u; 
	pb -> maxval = maxval; 

	struct timeval tv; 
	gettimeofday(&tv, NULL); 
	pb -> start_time = (unsigned) (tv.tv_sec * 1000l + tv.tv_usec / 1000l); 

	return pb; 

} 


/* 
 * Free up the memory stored by a progressbar object. 
 * 
 * header: progressbar.h 
 */ 
extern void progressbar_free(PROGRESSBAR *pb) {

	if (pb != NULL) {

		if ((*pb).left_hand_side != NULL) {
			free(pb -> left_hand_side); 
			pb -> left_hand_side = NULL; 
		} else {} 

		if ((*pb).right_hand_side != NULL) {
			free(pb -> right_hand_side); 
			pb -> right_hand_side = NULL; 
		} else {} 

		free(pb); 
		pb = NULL; 

	} else {} 

} 


/* 
 * Assign the string to be printed on the left hand side of the progressbar. 
 * Switches the attribute 'custom_left_hand_side' to 1 if it wasn't already. 
 * 
 * Parameters 
 * ==========
 * pb: 		A pointer to the progressbar to assign the string for 
 * value: 	The string to assign 
 * 
 * header: progressbar.h 
 */ 
extern void progressbar_set_left_hand_side(PROGRESSBAR *pb, char *value) {

	if ((*pb).left_hand_side != NULL) free(pb -> left_hand_side); 
	pb -> left_hand_side = (char *) malloc ((strlen(value) + 1u) * 
		sizeof(char)); 
	strcpy(pb -> left_hand_side, value); 
	pb -> left_hand_side[strlen(value)] = '\0'; 
	if (!(*pb).custom_left_hand_side) pb -> custom_left_hand_side = 1u; 

}


/* 
 * Assign the string to be printed on the right hand side of the progressbar. 
 * Switches the attribute 'custom_right_hand_side' to 1 if it wasn't already. 
 * 
 * Parameters 
 * ==========
 * pb: 		A pointer to the progressbar to assign the string for 
 * value: 	The string to assign 
 * 
 * header: progressbar.h 
 */ 
extern void progressbar_set_right_hand_side(PROGRESSBAR *pb, char *value) {

	if ((*pb).right_hand_side != NULL) free(pb -> right_hand_side); 
	pb -> right_hand_side = (char *) malloc ((strlen(value) + 1u) * 
		sizeof(char)); 
	strcpy(pb -> right_hand_side, value); 
	pb -> right_hand_side[strlen(value)] = '\0'; 
	if (!(*pb).custom_right_hand_side) pb -> custom_right_hand_side = 1u; 

}

/* 
 * Update the progressbar's current value and refresh what's printed on the 
 * terminal window. 
 * 
 * Parameters 
 * ==========
 * pb: 		A pointer to the progressbar to update 
 * value: 	The value to update the progressbar with. Assumed to be less than 
 * 			the attribute 'maxval,' though this is not enforced. 
 * 
 * header: progressbar.h 
 */ 
extern void progressbar_update(PROGRESSBAR *pb, unsigned long value) {

	pb -> current = value; 

	if (!(*pb).custom_left_hand_side) {
		/* 
		 * Set the default string to print on the left hand side of the 
		 * progressbar, unless the user has overridden it. Default is how many 
		 * of the maximum iterations have passed. 
		 */ 
		if (pb -> left_hand_side != NULL) free(pb -> left_hand_side); 
		pb -> left_hand_side = (char *) malloc ((4u + 
			(unsigned int) n_digits((*pb).current) + 
			(unsigned int) n_digits((*pb).maxval)) * sizeof(char)); 
		sprintf(pb -> left_hand_side, "%ld of %ld", (*pb).current, 
			(*pb).maxval); 
	} else {} 

	if (!(*pb).custom_right_hand_side) {
		/* 
		 * Set the default string to print on the right hand side of the 
		 * progressbar, unless the user has overridden it. Default is a message 
		 * with an approximate ETA. 
		 */ 
		if (pb -> right_hand_side != NULL) free(pb -> right_hand_side); 
		char *eta = format_time(progressbar_eta(*pb)); 
		pb -> right_hand_side = (char *) malloc ((5u + strlen(eta)) * 
			sizeof(char)); 
		sprintf(pb -> right_hand_side, "ETA: %s", eta); 
		free(eta); 
	} else {} 

	/* refresh the terminal window */ 
	progressbar_print(*pb); 

} 


/* 
 * Let the progressbar "finish" by setting the current value equal to the 
 * maximum value and starting a new line in the terminal. 
 * 
 * Parameters 
 * ==========
 * pb: 		The progressbar to finish 
 * 
 * header: progressbar.h 
 */ 
extern void progressbar_finish(PROGRESSBAR *pb) {

	progressbar_update(pb, (*pb).maxval); 
	printf("\n"); 
	fflush(stdout); 

} 


/* 
 * Refresh the terminal window by re-printing the progressbar. 
 * 
 * Parameters 
 * ==========
 * pb: 		The progressbar object controlling what's printed. 
 */ 
static void progressbar_print(PROGRESSBAR pb) {

	/* how many characters fit on 1 line in the terminal */ 
	unsigned short n_cols = window_width(); 

	/* 
	 * Make space for the strings on the left and right hand sides as well as 
	 * whitespace between the strings and the bar itself. 
	 */ 
	short bar_width = (signed) (n_cols - strlen(pb.left_hand_side) - 
		strlen(pb.right_hand_side) - 4u); 

	if (bar_width > 0) {
		unsigned short i, n_chars; 
		n_chars = (double) (pb.current) / pb.maxval * bar_width; 
		printf("\r%s [", pb.left_hand_side); 
		for (i = 0u; i <= n_chars; i++) printf("="); 
		if (pb.current < pb.maxval) printf(">"); 
		for (i = 0u; i < bar_width - n_chars - 1; i++) printf(" "); 
		printf("] %s", pb.right_hand_side); 
		fflush(stdout); 
	} else {
		/* 
		 * Not enough space for the progressbar => terminal window is small. 
		 * Do nothing in this case. 
		 */ 
	} 

} 


/* 
 * Estimate the time remaining for the progressbar. 
 * 
 * Parameters 
 * ==========
 * pb: 		The current progressbar object. 
 * 
 * Returns 
 * =======
 * The ETA in seconds. 0 if <1 millisecond has passed since it started. 
 */ 
static unsigned long progressbar_eta(PROGRESSBAR pb) {

	/* get time elapsed in milliseconds */ 
	struct timeval tv; 
	gettimeofday(&tv, NULL); 
	unsigned long elapsed = (unsigned) (tv.tv_sec * 1000l + tv.tv_usec / 1000l); 
	elapsed -= pb.start_time; 

	if (pb.current && elapsed) {
		double frac; 
		double prefactor; 

		switch (pb.eta_mode) {

			case 635u: /* ETA scales linearly with the number of operations */ 
				frac = (double) (pb.current) / pb.maxval; 
				prefactor = (1 - frac) / frac; 
				break; 

			case 875u: /* ETA scales as it would in a timestep model */ 
				prefactor = -1 + (double) (pow(pb.maxval, 2) + pb.maxval) / (
					pow(pb.current, 2) + pb.current); 
				break; 

			default: /* error handling */ 
				return 0ul; 

		} 

		return prefactor * elapsed / 1000l; 

	} else {
		/* Not yet enough information with which to calculate an ETA. */ 
		return 0u; 
	} 

}


/* 
 * Obtain the number of characters that fit in one line on the current 
 * terminal window. 
 * 
 * Returns 
 * =======
 * The total number of columns in the window minus 1 to make room for the 
 * cursor on the same line. 
 */ 
static unsigned short window_width(void) {

	/* 
	 * Subtract 1 from the window width to make room for the cursor on the 
	 * far right side of the progressbar. 
	 */ 
	struct winsize w; 
	ioctl(STDOUT_FILENO, TIOCGWINSZ, &w); 
	return w.ws_col - 1u; 

} 


/* 
 * Construct a string denoting the ETA of the progressbar of the format 
 * (hours)h(minutes)m(seconds)s. 
 * 
 * Returns 
 * =======
 * The string itself. 
 */ 
static char *format_time(unsigned long seconds) {

	unsigned long days = seconds / (24l * 3600l); 
	seconds %= 24l * 3600l; 
	unsigned short hours = seconds / 3600l; 
	seconds %= 3600l; 
	unsigned short minutes = seconds / 60l; 
	seconds %= 60l; 

	char *eta; 
	if (days) {
		eta = (char *) malloc ( (unsigned long) (15u + n_digits(days)) * 
			sizeof(char)); 
		sprintf(eta, "%ld days %02uh%02um%02lds", days, hours, minutes, 
			seconds); 
	} else {
		eta = (char *) malloc (10u * sizeof(char)); 
		sprintf(eta, "%02uh%02um%02lds", hours, minutes, seconds); 
	} 
	return eta; 

} 


/* 
 * Determine how many digits are in a number. 
 */ 
static unsigned short n_digits(double value) {

	return 1u + (unsigned short) log10(absval(value)); 

}

