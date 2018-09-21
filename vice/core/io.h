
#ifndef IO_H
#define IO_H

#include "specs.h"

extern int open_files(INTEGRATION *run, char *name);
extern void close_files(INTEGRATION run);
extern void write_history_header(INTEGRATION run, MODEL m);
extern void write_history_output(INTEGRATION run, MODEL m);
extern void write_mdf_header(INTEGRATION run);
extern void write_mdf_output(INTEGRATION run, MODEL m);
extern void write_breakdown_header(INTEGRATION run);
extern void write_breakdown_output(INTEGRATION run);
extern int read_agb_grid(INTEGRATION *run, char *file, int index);
extern double **read_output(char *file);
extern long num_lines(char *file);
extern int header_length(char *file);
extern int dimension(char *file, int hlength);
// extern int test_agb_reader(INTEGRATION *run);

#endif /* IO_H */
 