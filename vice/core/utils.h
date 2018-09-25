
#ifndef UTILS_H
#define UTILS_H

extern int setup_Zin(INTEGRATION run, MODEL *m, double *arr, long num_times);
extern int setup_elements(INTEGRATION *run, char **symbols, double *solars);
extern void clean_structs(INTEGRATION *run, MODEL *m);

#endif /* UTILS_H */

