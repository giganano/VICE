
cdef extern from "io.h":
	double **read_output(char *file)
	long num_lines(char *file)
	int dimension(char *file, int hlength)

