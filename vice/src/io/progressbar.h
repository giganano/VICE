
#ifndef IO_PROGRESSBAR_H
#define IO_PROGRESSBAR_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

typedef struct progressbar {

	/*
	 * start_time : system time in milliseconds when the progressbar started
	 * maxval : The number of iterations where the operation is complete
	 * current : The current number of iterations
	 * left_hand_side : The string to print on the left of the progressbar
	 * right_hand_side : The string to print on the right of the progressbar
	 * custom_left_hand_side : Boolean describing whether or not the default
	 * 		string to the left of the progressbar is overridden.
	 * custom_right_hand_side : Boolean describing whether or not the default
	 * 		string to the right of the progressbar is overridden.
	 * eta_mode : either 635 for "linear" or 875 for "timestep" depending on
	 * 		how computing time scales with the number of iterations.
	 * testing : boolean int describing whether or not the progressbar features
	 * 		are being tested. In this case, the progressbar will not actually
	 * 		print to the console.
	 *
	 * By default, the progressbar will print the current number of iterations
	 * and the ETA on the left and right, respectively, but this can be
	 * overridden by setting the strings directly and setting the custom_*
	 * booleans to 1.
	 */

	unsigned long start_time;
	unsigned long maxval;
	unsigned long current;
	char *left_hand_side;
	char *right_hand_side;
	unsigned short custom_left_hand_side;
	unsigned short custom_right_hand_side;
	unsigned short eta_mode;
	unsigned short testing;

} PROGRESSBAR;

/*
 * Allocate memory for and return a pointer to a progressbar object.
 *
 * Parameters
 * ==========
 * maxval: 		The total number of iterations before the operation using the
 * 				progressbar is complete.
 *
 * source: progressbar.c
 */
extern PROGRESSBAR *progressbar_initialize(unsigned long maxval);

/*
 * Free up the memory stored by a progressbar object.
 *
 * source: progressbar.c
 */
extern void progressbar_free(PROGRESSBAR *pb);

/*
 * Assign the string to be printed on the left hand side of the progressbar.
 * Switches the attribute 'custom_left_hand_side' to 1 if it wasn't already.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the progressbar to assign the string for
 * value: 	The string to assign. NULL to revert to default.
 *
 * source: progressbar.c
 */
extern void progressbar_set_left_hand_side(PROGRESSBAR *pb, char *value);

/*
 * Assign the string to be printed on the right hand side of the progressbar.
 * Switches the attribute 'custom_right_hand_side' to 1 if it wasn't already.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the progressbar to assign the string for
 * value: 	The string to assign. NULL to revert to default.
 *
 * source: progressbar.c
 */
extern void progressbar_set_right_hand_side(PROGRESSBAR *pb, char *value);

/*
 * Updates the progressbar with a value of 0 and prints to the console.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the current progressbar.
 *
 * source: progressbar.c
 */
extern void progressbar_start(PROGRESSBAR *pb);

/*
 * Let the progressbar "finish" by setting the current value equal to the
 * maximum value and starting a new line in the terminal.
 *
 * Parameters
 * ==========
 * pb: 		The progressbar to finish
 *
 * source: progressbar.c
 */
extern void progressbar_finish(PROGRESSBAR *pb);

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
 * source: progressbar.c
 */
extern void progressbar_update(PROGRESSBAR *pb, unsigned long value);

/*
 * Refresh the progressbar -> updates with the current value to capture any
 * changes to the right or left hand side and updates the console.
 *
 * Parameters
 * ==========
 * pb: 		A pointer to the current progressbar
 *
 * source: progressbar.c
 */
extern void progressbar_refresh(PROGRESSBAR *pb);

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
 * source: progressbar.c
 */
extern char *progressbar_string(PROGRESSBAR *pb);

#ifdef __cpluscplus
}
#endif /* __cplusplus */

#endif /* IO_PROGRESSBAR_H */
