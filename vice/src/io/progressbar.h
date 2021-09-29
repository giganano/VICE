
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
 * value: 	The string to assign 
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
 * value: 	The string to assign 
 * 
 * source: progressbar.c 
 */ 
extern void progressbar_set_right_hand_side(PROGRESSBAR *pb, char *value); 

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
 * source: progressbar.c 
 */ 
extern void progressbar_update(PROGRESSBAR *pb, unsigned long value); 

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

#ifdef __cpluscplus 
} 
#endif /* __cplusplus */ 

#endif /* IO_PROGRESSBAR_H */ 
