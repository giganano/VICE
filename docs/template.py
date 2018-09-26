"""
This is a template with commens on each line to guide the user how to 
set up a script to run their model. This initializes an integrator object 
with the same parameters as the default, with the exception of func, which 
has been switched to an exponential decay for illustrative purposes. We 
recommend that you start here before moving on to running and inspecing 
example1.py and example2.py.

The output will be found in your current working directory under a folder 
named "example". It contains two files - history.out, and mdf.out. The first 
contains the full set of abundance information at all output times, and the 
second contains the stellar metallicity distribution function at the final 
timestep. This is all the user needs to get the full power of the 
integration functions in this package. See example1.py and example2.py for 
tutorials on how to use the output object, which is there purely to make 
working with and plotting the output just as trivial. 

We refer the user to the class docstring of the integrator object for a user's 
note on how to properly set attributes as functions as well as building 
delta functions into those attributes. 

See the docstrings of individual object attributes in the event that more 
documentation than what is given here be needed.
"""

import math as m
try:
	"""
	NumPy is not necessary to use VICE. VICE is NumPy- and Pandas- compatible, 
	but neither NumPy- nor Pandas- dependent. It is independent of the user's 
	version of Anaconda. 
	"""
	import numpy as np
	times = np.linspace(0, 10, 1001)
except ImportError:
	# times is a python list from 0 to 10 in steps of 0.01
	times = 1001 * [0.]
	for i in range(1001):
		times[i] = 0. + 0.001 * i

try:
	import vice 
except ImportError:
	# VICE either not installed or doesn't meet system requirements
	message = "VICE is not installed. Please see <https//github.com/giganano/"
	message += "VICE> for installation instructions. If you have followed "
	message += "the proper steps to install and are still receiving this " 
	message += "message, please submit a bug report to James Johnson, the "
	message += "primary author, at <giganano9@gmail.com>."
	raise SystemError(message)

"""
No init args necessary - they're all keyword args and can be modified as 
attributes.
"""
example = vice.integrator()

"""
Whether or not to automatically recalculate the yields from CCSNe off of the 
current settings of example for lower mass limit on star formation, upper 
mass limit on star formation, imf, and rotating vs. nonrotating CCSNe model. 
The yields used to calculate the IMF-integrated fractional yields are 
derived from Chieffi & Limongi (2013), ApJ, 764, 21
"""
example.auto_recalc = False

"""
Track only iron and oxygen. 
"""
example.elements = ["fe", "o"]

"""
The name of your model, as a string. The output of the integration will be 
stored in a folder under this name. If you don't want the output in your 
current working directory, simply put the full path here. 
"""
example.name = "example"

"""
The func attribute - t is always in Gyr
See user's warning in integrator class docstring for user's note on why 
NumPy functions must be wrapped in a python function
"""
example.func = lambda t: m.exp( -t / 3. )

"""
The mode - this means that func is specifying an infall rate in Msun/yr. 
If we switched to "sfr", then it would represent the star formation rate 
at all times in units of Msun/yr. If we switched it to "gas", it would 
represent the gas mass at times in units of Msun.
"""
example.mode = "ifr"

"""
The imf to assume. In the current versions of the code, this affects the 
continuous recycling behavior and the rate of AGB enrichment.
"""
example.imf = "kroupa"

"""
Whether or not to use an implementation of Schmidt Law star formation 
efficiency. Mathematically, the star formation efficiency is determined 
at each timestep with the following attributes in this manner:
SFE = 1.0 / tau_star(t) * (Mgas / MgSchmidt)**(schmidt_index)
"""
example.schmidt = False

"""
The mass loading parameter. This can also be a callable Python function of 
time in Gyr. This is  the ratio between the outflow and star formation rates, 
although not necessarily the instantaneous ratio in the case of nonzero 
smoothing times.
"""
example.eta = 2.5

"""
The ratio of the outflow metallicity to the ISM metallicity. This can be 
either a single numerical value or a callable function of time. 
"""
example.enhancement = 1.

"""
The recycling specification. This can either be a numerical value between 0 
and 1, representing mass fraction of star formation that is immediately 
returned to the ISM after star formation. If specified "continuous," this is 
treated in a time-dependent manner given the IMF.
"""
example.recycling = "continuous"

"""
The bins in [X/Y] to sort the stellar metallicity distribution function into. 
It is assumed that they're in ascending order. 

We don't use NumPy to make this array because VICE isn't dependent on NumPy. 
"""
arr = 401 * [0.]
for i in range(401):
	arr[i] = -3 + 0.01 * i
example.binspace = arr

"""
The minimum time delay in Gyr between an episode of star formation rate and 
the onset of SNe Ia from that generation of stars. 
"""
example.delay = 0.15

"""
The delay-time distribution in SNe Ia. This is either "plaw" for a power 
law going as t^(-1.1) or "exp" for an exponential with timescale tau_ia 
(another attribute). The may also specify their own function of time here, and 
they needn't worry about its normalization. 
"""
example.dtd = "plaw"

# The initial gas mass in Msun. This is only required when mode == "ifr"
example.Mg0 = 6.0e9

"""
The smoothing timescale in Gyr. When this is larger than the timestep, the 
star formation rate will be averaged over this past time window at each 
timestep before being multiplied by eta to determine the outflow rate. 
"""
example.smoothing = 0.

"""
The e-folding timescale of SNe Ia. This is only relevant if the delay-time 
distribution (attribute "dtd") is set to "exp."
"""
example.tau_Ia = 1.5

"""
The depletion time in Gyr. This is the inverse of the star formation 
efficiency. In the case of Schmidt-Law efficiency, this value is used to 
set the overall normalization of the Schmidt-Law. It can also 
be a callable Python function of time with or without Schmidt-Law 
efficiency, just like eta.
"""
example.tau_star = 2.

# The timestep size to use in Gyr.
example.dt = 0.001

# The power law index on the Schmidt-Law if that setting is on. 
example.schmidt_index = 0.5

# The normalization on the gas supply if schmidt = True. 
example.MgSchmidt = 2.0e9

# The lower mass limit on star formation in Msun
example.m_lower = 0.08

# The upper mass limit on star formation in Msun
example.m_upper = 100

# Whether to adopt the rotatin vs. non-rotating model for CCSNe in the 
# Chieffi & Limongi (2013) yields
example.rotating_ccsne = True

# Runs the integration
example.run(times)







