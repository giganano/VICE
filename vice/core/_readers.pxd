"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 
"""

cdef extern from "io.h":
	double **read_output(char *file)
	long num_lines(char *file)
	int dimension(char *file, int hlength)

