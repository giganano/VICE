/*
 * This file implements a progressbar for VICE's verbose terminal output.
 */

#if defined(_WIN32)
	#include <windows.h>
#else
	#include <sys/ioctl.h>
	#include <sys/time.h>
#endif
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include "progressbar.h"
#include "../utils.h"
#include "../io.h"
// #include "../debug.h"

/* ---------- Static function comment headers not duplicated here ---------- */
static void progressbar_print(PROGRESSBAR *pb);
static void progressbar_set_strings(PROGRESSBAR *pb);
static unsigned long progressbar_eta(PROGRESSBAR pb);
static unsigned short window_width(PROGRESSBAR pb);
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

	// trace_print();
	// debug_print("maxval = %lu\n", maxval);

	PROGRESSBAR *pb = (PROGRESSBAR *) malloc (sizeof(PROGRESSBAR));
	pb -> left_hand_side = NULL;
	pb -> right_hand_side = NULL;
	pb -> custom_left_hand_side = 0u;
	pb -> custom_right_hand_side = 0u;
	pb -> eta_mode = 635u;
	pb -> maxval = maxval;
	pb -> current = 0ul; /* start at 0 by default */
	pb -> testing = 0u;

	struct timeval tv;
	gettimeofday(&tv, NULL);
	pb -> start_time = (unsigned) (tv.tv_sec * 1000l + tv.tv_usec / 1000l);
	// debug_print("Progressbar address: %p\n", (void *) pb);

	return pb;

}


/*
 * Free up the memory stored by a progressbar object.
 *
 * header: progressbar.h
 */
extern void progressbar_free(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);

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
 * value: 	The string to assign. NULL to revert to default.
 *
 * header: progressbar.h
 */
extern void progressbar_set_left_hand_side(PROGRESSBAR *pb, char *value) {

	// trace_print();
	if ((*pb).left_hand_side != NULL) {
		free(pb -> left_hand_side);
		pb -> left_hand_side = NULL;
	} else {}
	if (value != NULL) {
		// debug_print("value = %s\n", value);
		pb -> left_hand_side = (char *) malloc ((strlen(value) + 1u) *
			sizeof(char));
		strcpy(pb -> left_hand_side, value);
		pb -> left_hand_side[strlen(value)] = '\0';
		if (!(*pb).custom_left_hand_side) pb -> custom_left_hand_side = 1u;
	} else {
		// debug_print("%s\n", "value is NULL");
		if ((*pb).custom_left_hand_side) pb -> custom_left_hand_side = 0u;
	}

}


/*
 * Assign the string to be printed on the right hand side of the progressbar.
 * Switches the attribute 'custom_right_hand_side' to 1 if it wasn't already.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the progressbar to assign the string for
 * value: 	The string to assign. NULL to revert to default.
 *
 * header: progressbar.h
 */
extern void progressbar_set_right_hand_side(PROGRESSBAR *pb, char *value) {

	// trace_print();
	if ((*pb).right_hand_side != NULL) {
		free(pb -> right_hand_side);
		pb -> right_hand_side = NULL;
	} else {}
	if (value != NULL) {
		// debug_print("value = %s\n", value);
		pb -> right_hand_side = (char *) malloc ((strlen(value) + 1u) *
			sizeof(char));
		strcpy(pb -> right_hand_side, value);
		pb -> right_hand_side[strlen(value)] = '\0';
		if (!(*pb).custom_right_hand_side) pb -> custom_right_hand_side = 1u;
	} else {
		// debug_print("%s\n", "value is NULL");
		if ((*pb).custom_right_hand_side) pb -> custom_right_hand_side = 0u;
	}

}


/*
 * Updates the progressbar with a value of 0 and prints to the console.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the current progressbar.
 *
 * header: progressbar.h
 */
extern void progressbar_start(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);
	progressbar_update(pb, 0ul);
	progressbar_print(pb);

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

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);
	progressbar_update(pb, (*pb).maxval);
	if (!(*pb).testing) printf("\n");
	fflush(stdout);

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
 * Notes
 * =====
 * The change will only be reflected if value is between 0 and (*pb).maxval
 * (inclusive). When called in C with this error, there is no change to the
 * current value and the result is the same as calling progressbar_refresh(pb).
 * In python, however, this results in a ValueError.
 *
 * header: progressbar.h
 */
extern void progressbar_update(PROGRESSBAR *pb, unsigned long value) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);
	// debug_print("value = %lu\n", value);

	/* No need to make sure an unsigned number is positive */
	if (value <= (*pb).maxval) pb -> current = value;
	progressbar_print(pb);

}


/*
 * Refresh the progressbar -> updates with the current value to capture any
 * changes to the right or left hand side and updates the console.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the current progressbar
 *
 * header: progressbar.h
 */
extern void progressbar_refresh(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);
	progressbar_print(pb);

}


/*
 * Get the current state of the progressbar as a string.
 *
 * Parameters
 * ==========
 * pb: 		The progressbar to get the current state of.
 *
 * Returns
 * =======
 * A char pointer to the string which would be printed on the terminal window.
 *
 * header: progressbar.h
 */
extern char *progressbar_string(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);

	/* how many characters fit on one line in the terminal */
	unsigned short n_cols = window_width(*pb);

	/*
	 * Allocate memory for the string. In practice, allocating memory for only
	 * the size of the string produces a memory error, so we allocate for a
	 * safely large number of characters.
	 * Here is also where the strings on the left and right hand sides of the
	 * bar get assigned, hence why this takes a pointer.
	 */
	char *current = (char *) malloc (LINESIZE * sizeof(char));
	progressbar_set_strings(pb);

	/*
	 * Make space for the strings on the left and right hand sides as well as
	 * whitespace between the strings and the bar itself.
	 */
	short bar_width = (signed) n_cols - 4;
	if ((*pb).left_hand_side != NULL) bar_width -= (signed) strlen(
		(*pb).left_hand_side);
	if ((*pb).right_hand_side != NULL) bar_width -= (signed) strlen(
		(*pb).right_hand_side);

	if (bar_width > 0) {
		/* n_chars : how full the progressbar is in its current state. */
		unsigned short i, n_chars;
		n_chars = (double) ((*pb).current) / (*pb).maxval * bar_width;
		if ((*pb).left_hand_side != NULL) strcpy(current,
			(*pb).left_hand_side);
		strcat(current, " [");
		for (i = 0u; i < n_chars; i++) strcat(current, "=");
		if ((*pb).current < (*pb).maxval) strcat(current, ">");
		for (i = 0u;
			i < (unsigned) bar_width - n_chars - (bar_width != n_chars) * 1u;
			i++) strcat(current, " ");
		strcat(current, "] ");
		if ((*pb).right_hand_side != NULL) strcat(current,
			(*pb).right_hand_side);
		strcat(current, "\0");
	} else {
		/*
		 * Not enough space for the progressbar -> terminal window is small.
		 * Return a blank string in this case.
		 */
		current[0] = '\0';
	}

	// debug_print("current = %s\n", current);
	return current;

}


/*
 * Refresh the terminal window by re-printing the progressbar.
 *
 * Parameters
 * ==========
 * pb: 		The progressbar object controlling what's printed.
 *
 * Notes
 * =====
 * This function accepts a pointer because it also calls the functions which
 * set up the string that gets printed, which in turn require the pointer.
 */
static void progressbar_print(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);
	char *current = progressbar_string(pb);
	if (!(*pb).testing) printf("\r%s", current); /* don't print if testing */
	free(current);
	fflush(stdout);

}


/*
 * Assign the strings that appear on the left and right hand sides of the
 * progressbar.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the progressbar to assign the strings for.
 */
static void progressbar_set_strings(PROGRESSBAR *pb) {

	// trace_print();
	// debug_print("Progressbar address: %p\n", (void *) pb);

	if (!(*pb).custom_left_hand_side) {
		/*
		 * Set the default string to print on the left hand side of the
		 * progressbar, unless the user has overridden it. Default is how many
		 * of the maximum iterations have passed. Add a null terminator to
		 * the end of the string to prevent the left and right hand sides from
		 * getting concatenated together since they're declared side by side.
		 * Forgetting this can lead to a seg fault as the memory blocks are
		 * often adjacent.
		 */
		if (pb -> left_hand_side != NULL) free(pb -> left_hand_side);
		pb -> left_hand_side = (char *) malloc ((5u +
			(unsigned int) n_digits((*pb).current) +
			(unsigned int) n_digits((*pb).maxval)) * sizeof(char));
		sprintf(pb -> left_hand_side, "%ld of %ld", (*pb).current,
			(*pb).maxval);
		strcat(pb -> left_hand_side, "\0");
	} else {}

	if (!(*pb).custom_right_hand_side) {
		/*
		 * Set the default string to print on the right hand side of the
		 * progressbar, unless the user has overridden it. Default is a message
		 * with an approximate ETA. Add a null terminator to the end of the
		 * string to prevent the left and right hand sides from getting
		 * concatenated together since they're declared side by side.
		 * Forgetting this can lead to a seg fault as the memory blocks are
		 * often adjacent.
		 */
		if (pb -> right_hand_side != NULL) free(pb -> right_hand_side);
		char *eta = format_time(progressbar_eta(*pb));
		pb -> right_hand_side = (char *) malloc ((6u + strlen(eta)) *
			sizeof(char));
		sprintf(pb -> right_hand_side, "ETA: %s", eta);
		strcat(pb -> right_hand_side, "\0");
		free(eta);
	} else {}

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

	// trace_print();

	/* get time elapsed in milliseconds */
	struct timeval tv;
	gettimeofday(&tv, NULL);
	unsigned long elapsed = (unsigned) (tv.tv_sec * 1000l + tv.tv_usec / 1000l);
	elapsed -= pb.start_time;
	// debug_print("elapsed = %lu\n", elapsed);

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

		unsigned long result = prefactor * elapsed / 1000l;
		// debug_print("result = %lu\n", result);
		return result;

	} else {
		/* Not yet enough information with which to calculate an ETA. */
		// debug_print("%s\n", "result = 0");
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
static unsigned short window_width(PROGRESSBAR pb) {

	// trace_print();
	if (pb.testing) {
		/*
		 * GitHub actions has a different ioctl than a Mac OS or Linux desktop,
		 * so the usual routine at the bottom of this function doesn't work.
		 * When GitHub actions runs this function, simply assume a window
		 * width of 100 for the sake of testing purposes.
		 * GitHub actions sets the environment variable GITHUB_ACTIONS="true"
		 */
		char *github_actions = getenv("GITHUB_ACTIONS");
		if (github_actions != NULL) {
			if (!strcmp(github_actions, "true")) {
				// debug_print("%s\n", "Within GitHub Actions.");
				return 100u;
			} else {}
		} else {}
	} else {}

	#if defined(_WIN32)
		/*
		 * This is an implementation of the solution at https://stackoverflow.com/questions/6812224/getting-terminal-size-in-c-for-windows
		 */
		CONSOLE_SCREEN_BUFFER_INFO csbi;
		GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi);
		unsigned int columns = (unsigned) (csbi.srWindow.Right -
			csbi.srWindow.Left);
		return columns;
	#else
		/*
		 * Subtract 1 from the window width to make room for the cursor on the
		 * far right side of the progressbar.
		 */
		struct winsize w;
		ioctl(0, TIOCGWINSZ, &w);
		// debug_print("Window width = %u\n", w.ws_col - 1u);
		return w.ws_col - 1u;
	#endif

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

	// trace_print();
	// debug_print("seconds = %lu\n", seconds);
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
	// debug_print("eta = %s\n", eta);
	return eta;

}


/*
 * Determine how many digits are in a number.
 */
static unsigned short n_digits(double value) {

	// trace_print();
	// debug_print("value = %.5e\n", value);
	unsigned short result = 1u + (unsigned short) log10(absval(value));
	// debug_print("result = %u\n", result);
	return result;

}

