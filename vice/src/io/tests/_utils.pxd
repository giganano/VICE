# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/io/tests/utils.h":
	unsigned short test_read_square_ascii_file()
	unsigned short test_header_length()
	unsigned short test_file_dimension()
	unsigned short test_line_count()
