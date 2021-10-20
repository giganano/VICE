# cython: language_level = 3, boundscheck = False

cdef extern from "utils.h":
	unsigned short test_choose()
	unsigned short test_absval()
	unsigned short test_sign()
	unsigned short test_simple_hash()
	unsigned short test_rand_range()
	unsigned short test_interpolate()
	unsigned short test_interpolate2D()
	unsigned short test_interpolate_sqrt()
	unsigned short test_get_bin_number()
	unsigned short test_binspace()
	unsigned short test_bin_centers()
	unsigned short test_sum()
	unsigned short test_set_char_p_value()
	unsigned short test_max()
