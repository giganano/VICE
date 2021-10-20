
try:
	__VICE_SETUP__
except NameError:
	__VICE_SETUP__ = False
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError


if not __VICE_SETUP__:
	from vice.cmdline import main
	main()
else:
	raise RuntimeError("""VICE cannot be ran from the command line during a \
source installation. Please wait until that process has finished.""")

