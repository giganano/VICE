/*
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
*/

#ifndef UTILS_H
#define UTILS_H

extern int setup_Zin(INTEGRATION run, MODEL *m, double *arr, long num_times);
extern int setup_elements(INTEGRATION *run, char **symbols, double *solars);
extern void clean_structs(INTEGRATION *run, MODEL *m);

#endif /* UTILS_H */

