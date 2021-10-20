# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/channel.h":
	unsigned short test_channel_initialize()
	unsigned short test_channel_free()

