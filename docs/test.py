"""
The following runs every history from the example and template files ensuring 
that there are no errors. 
"""

from __future__ import print_function
try:
	import numpy as np
	times = np.linspace(0, 10, 1001)
except ImportError:
	times = 1001 * [0.]
	for i in range(1001):
		times[i] = 0. + 0.001 * i

try:
	import vice
except ImportError:
	message = "Vice is not installed. Please see <https//github.com/giganano/"
	message += "VICE> for installation instructions. If you have followed "
	message += "the proper steps to install and are still receiving this " 
	message += "message, please submit a bug report to James Johnson, the "
	message += "primary author, at <giganano9@gmail.com>."
	raise SystemError(message)

try:
	first = vice.integrator(name = "example1_1")
	out1 = first.run(times, capture = True)
	print("First integration: Success")
except: 
	print("First integration: Failed")

try:
	second = vice.integrator(name = "example1_2")
	second.func = lambda t: np.exp( -t / 3 )
	second.Mg0 = 1.
	out2 = second.run(times, capture = True)
	print("Second integration: Success")
except:
	print("Second integration: Failed")

try:
	third = vice.integrator(name = "example1_3", schmidt = True)
	third.func = lambda t: np.exp( -t / 3 )
	third.Mg0 = 1.
	out3 = third.run(times, capture = True)
	print("Third integration: Success")
except:
	print("Third integration: Failed")




