
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False


if not __VICE_SETUP__:

	import sys
	outfilename = "test_%s_py%d%d.log" % (sys.platform, sys.version_info[0],
		sys.version_info[1])

	import vice
	vice.test(outfile = outfilename)

else:
	pass

