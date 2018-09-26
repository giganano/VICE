"""
This runs a gas bolus, an IFR boost, and an SFE boost history. 

SEE USER'S WARNING in the vice.integrator class docstring on emulating 
delta functions in function attributes. 

We recommend the user read template.py and run example1.py prior to running 
and inspecting this script.
"""

import math as m
import os
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
	message += "primary author, at <giganano9@gmail.com> or open an issue in "
	message += "the git repository at <https://github.com/giganano/VICE.git"
	raise SystemError(message)

# Let's do the bolus on top an exponentially declining infall rate with 
# non-negligible initial gas mass.
bolus = vice.integrator(name = "bolus")
def f(t):
	if 5 <= t < 5.001:
		return 5000
	else:
		return 9.1 * m.exp( -t / 3 )
bolus.func = f
# capture the output and show the sfr, gas mass, and ifr as a function of time
out1 = bolus.run(times, capture = True)
out1.show("ifr")
out1.show("mgas")
out1.show("sfr")
out1.show("[O/Fe]-[Fe/H]")
out1.show("[O/Sr]-[Sr/H]")

"""
Let's do the infall boost on top of a constant infall rate, but let's do it 
with schmidt law efficiency
"""
ifrboost = vice.integrator(name = "ifrboost", schmidt = True)
def f(t):
	if 5 <= t <= 6:
		return 14.1
	else:
		return 9.1
ifrboost.func = f
out2 = ifrboost.run(times, capture = True)
out2.show("ifr")
out2.show("mgas")
out2.show("sfr")

"""
Let's do a star formation effieciency boost on top of a linear exponential 
gas history. This can be done by changing the function to an exponential 
decay, the initial gas mass to something small, and the depletion timescale 
to a function of time
"""
sfeboost = vice.integrator(name = "sfeboost")
sfeboost.func = lambda t: m.exp( -t / 3 )
def f(t):
	if 5 <= t <= 6:
		# A decrease in depletion time is the same as an increase in SFE
		return 1.
	else:
		return 2. 
# Initializing tau_star as a function instead of a numerical value
sfeboost.tau_star = f
sfeboost.Mg0 = 1. 
out3 = sfeboost.run(times, capture = True)
out3.show("tau_star")
out3.show("ifr")
out3.show("sfr")
out3.show("dN/d[O/Fe]")

"""
The user can also use Schmidt Law star formation efficiency by setting 
the integrator attribute schmidt = True. In this case, the attribute 
schmidt_index is the power law index the user wishes to use, MgSchmidt is 
the normalization of the gas supply, and tau_star is the overall 
normalization of the schmidt law itself. That is, at all timesteps, the 
star formation efficiency will be determined as:
SFE = 1/tau_star * (Mgas / MgSchmidt)**(schmidt_index)
Let's show what happens when we take the star formation efficiency boost 
from the last history and turn on Schmidt law behavior. This will correspond 
to a history where the schmidt law holds, but there is some dynamical event 
5 Gyr's after the onset of star formation that changes the overall 
normalization of the schmidt law and is in effect for 1 Gyr.
"""
sfe_schmidt = vice.integrator(name = "sfe_schmidt", schmidt = True)
sfe_schmidt.func = lambda t: m.exp( -t / 3 )
sfe_schmidt.tau_star = f # This is now the normalization of the Schmidt law, 
# and we're showing that the user can allow that to change in their model.
sfe_schmidt.Mg0 = 1.
out4 = sfe_schmidt.run(times, capture = True, overwrite = True)
out4.show("tau_star")
out4.show("mgas")
out4.show("sfr")
out4.show("dN/d[O/Fe]")

"""
Specifies a customized SNe Ia delay-time distribution according to a 
linear-exponential model along with inflow of iron that is 
10% of the solar abundance at all times, and an inflow of oxygen that 
increases linearly to 10% of solar at 10 Gyr. We will also neglect the 
strontium enrichment in this model by specifying the attribute 'elements'. For 
illustrative purposes, we're also going to decrement the iron yield from 
core-collapse supernovae by a factor of 2. 
"""
custom_ria = vice.integrator(name = "custom_ria")
custom_ria.dtd = lambda t: (t - custom_ria.delay) * m.exp( -(t - 
	custom_ria.delay) / 2 )
custom_ria.elements = ['o', 'fe']
custom_ria.Zin = len(custom_ria.elements) * [0]
custom_ria.Zin['fe'] = 0.1 * vice.solar_z['fe']
custom_ria.Zin['o'] = lambda t: 0.1 * vice.solar_z['o'] * (t / 10.0)
vice.ccsne_yields['fe'] /= 2
out5 = custom_ria.run(times, capture = True, overwrite = True)
out5.show("[O/Fe]-[Fe/H]")
out5.show("dN/d[O/Fe]")

"""
Here we also illustrate how an output object from a previously ran 
integration can be instanced by simply creating one. Here is an output 
object corresponding to the model ran in example1.py. When capture = False, 
onezone will not return an output object to the user, but they can still 
be instantiated as follows: 
"""
if "example1_1" in os.listdir('.'):
	out6 = vice.output("example1_1")
	out6.show("[O/Fe]")
	out6.show("dN/d[O/Fe]")
else:
	pass




