"""
This script runs two different smooth gas history models as examples. We 
recommend that the user read through template.py before running and inspecting 
this script.
"""

# __future__ is for python 3.x compatibility
from __future__ import print_function
try:
	"""
	NumPy is not necessary to use vice. Vice is NumPy- and Pandas- compatible, 
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
	# Vice either not installed or doesn't meet system requirements
	message = "Vice is not installed. Please see <https//github.com/giganano/"
	message += "VICE> for installation instructions. If you have followed "
	message += "the proper steps to install and are still receiving this " 
	message += "message, please submit a bug report to James Johnson, the "
	message += "primary author, at <giganano9@gmail.com>."
	raise SystemError(message)

times = np.linspace(0, 10, 1001)

# The default integrator, which is a constant infall history
message = "The default integrator is that of a constant infall history.\n"
message += "These are the default parameters, where _DEFAULT_FUNC is just "
message += "a python function that always returns the value 9.1. The mode "
message += "'ifr' means that this is specifying an infall rate of 9.1 Msun/yr "
message += "at all timesteps. Here are the complete parameter settings for "
message += "the default model. "
print(message) 
first = vice.integrator(name = "example1_1")
first.settings() # prints the settings 

# The code always writes to an output file, but capture = True tells it that 
# we want an output object from this iteration right now.
print("Running the integration....")
out1 = first.run(times, capture = True)

message = "By capturing the output within the script, we are able to "
message += "visualize some of its output. Here is the infall rate as a "
message += "function of time. This is what is specified by _DEFAULT_FUNC "
message += "returning 9.1 at all times and with mode = 'ifr'."
print(message)
out1.show("ifr")

message = "We can show any of the quantities in either history or mdf output "
message += "files with the output.show('arg') feature. We simply need to tell "
message += "it what we want to see. Unless an argument is given in the form "
message += "of y-x, it is always shown against time. For example, [O/Fe]:"
print(message)
out1.show("[O/Fe]")

message = "Now let's look at a slightly more complicated history. An "
message += "exponential infall history can be done just by changing the func "
message += "attribute to some exponential decay function. Let's also emualte "
message += "a linear-exponential gas history by letting the initial gas mass "
message += "be very small. Something on the order of 1 Msun will do. "
message += "The new settings look like this: "
print(message)
second = vice.integrator(name = "example1_2")
# An exponential decay with an e-folding timescale of 6 Gyr
second.func = lambda t: np.exp( -t / 3 )
second.Mg0 = 1. # A very small initial gas supply. 
second.settings()

print("Running the integration....")
out2 = second.run(times, capture = True)

message = "This gives us a linear exponential gas history that looks like "
message += "this: "
print(message)
out2.show("mgas")

message = "Output object history and mdf attributes can be indexed by calling "
message += "either the columns within the dataframe or the row number. For "
message += "example:"
print(message)
print("out2.history[\"mgas\"][:10] = ",out2.history["mgas"][:10])
print("out2.history[0] = ", out2.history[0])
message = "They can be indexed with the following strings (case-insensitive). "
message += "This is the attribute 'labels' for both history and mdf "
message += "dataframes:"
print(message)
print(out2.history.labels)
print(out2.mdf.labels)

message = "Calling abundance ratios [X/Y] within the history attribute is "
message += "coded dynamically, such that if the particular abundance ratio "
message += "is not in the dataframe, it calculates it. For example, [Sr/O]:"
print(message)
print("out2.history[\"Sr/O\"][:10] = ",out2.history["[Sr/O]"][:10])

message = "The user can also have the integrator exhibit Schmidt law "
message += "star-formation efficiency, where the efficiency is a power law in "
message += "the gas supply. In this case, the attribute tau_star simply sets "
message += "the overall normalization of the Schmidt law. The user also "
message += "can manipulate the attributes MgSchmidt, which is the overall "
message += "normalization in the gas supply, and schmidt_index, which is the "
message += "power law index. The star formation efficiency, mathematically "
message += "in terms of the attributes of the integrator class, is then "
message += "given by: SFE = 1/tau_star(t) * (Mgas / MgSchmidt)**schmidt_index."
message += "Let's revisit the linear-exponential gas history, but we'll turn "
message += "on Schmidt law efficiency. Note from the equation that the "
message += "overall normalization of the Schmidt Law 1/tau_star(t) can be a "
message += "function of time. The new settings:"
print(message)
third = vice.integrator(name = "example1_3", schmidt = True)
third.func = lambda t: np.exp( -t / 3 )
third.Mg0 = 1.
third.settings()
out3 = third.run(times, capture = True)

print("This gives a gas and star formation history that look like this: ")
out3.show("mgas")
out3.show("sfr")
print("and a time-dependent depletion time that looks like this: ")
out3.show("tau_star")

message = "We recommend that the user also inspect template.py and " 
message += "example2.py. Template.py will help them get their own " 
message += "integrations running, and example2.py will show them some "
message += "examples of slightly more sophisticated examples. However, "
message += "because the class attributes of an integrator can be callable "
message += "functions of time, Vice is built to integrate galactic chemical "
message += "evolution models with any degree of sophistication."
print(message)
