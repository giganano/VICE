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

message = "Running tests on the integration features, output reader, and "
message += "yield-weighted IMF-integrator. This will take a few minutes, "
message += "depending on the processing speed of the system."
print(message)
send = False

try:
	first = vice.integrator(name = "example1_1", dt = 0.005)
	out1 = first.run(times, capture = True)
	print("First integration: Success")
except: 
	send = True
	print("First integration: Failed")

try:
	second = vice.integrator(name = "example1_2", dt = 0.005)
	second.func = lambda t: np.exp( -t / 3 )
	second.Mg0 = 1.
	out2 = second.run(times, capture = True)
	print("Second integration: Success")
except:
	send = True
	print("Second integration: Failed")

try:
	third = vice.integrator(name = "example1_3", schmidt = True, dt = 0.005)
	third.func = lambda t: np.exp( -t / 3 )
	third.Mg0 = 1.
	out3 = third.run(times, capture = True)
	print("Third integration: Success")
except:
	send = True
	print("Third integration: Failed")

try:
	bolus = vice.integrator(name = "bolus", dt = 0.005)
	def f(t):
		if 5 <= t < 5.001:
			return 5000
		else:
			return 9.1
	bolus.func = f
	out1 = bolus.run(times, capture = True)
	print("Fourth integration: Success")
except:
	send = True
	print("Fourth integration: Failed")

try: 
	ifrboost = vice.integrator(name = "ifrboost", schmidt = True, dt = 0.005)
	def f(t):
		if 5 <= t <= 6:
			return 14.1
		else:
			return 9.1
	ifrboost.func = f
	out2 = ifrboost.run(times, capture = True)
	print ("Fifth integration: Success")
except:
	send = True
	print("Fifth integration: Failed")

try:
	sfeboost = vice.integrator(name = "sfeboost", dt = 0.005)
	sfeboost.func = lambda t: np.exp( -t / 3 )
	def f(t):
		if 5 <= t <= 6:
			return 1.
		else:
			return 2.
	sfeboost.tau_star = f
	sfeboost.Mg0 = 1.
	out3 = sfeboost.run(times, capture = True)
	print("Sixth integration: Success")
except:
	send = True
	print("Sixth integration: Failed")

try:
	sfe_schmidt = vice.integrator(name = "sfe_schmidt", schmidt = True, 
		dt = 0.005)
	sfe_schmidt.func = lambda t: np.exp( -t / 3 )
	sfe_schmidt.tau_star = f
	sfe_schmidt.Mg0 = 1.
	out4 = sfe_schmidt.run(times, capture = True)
	print("Seventh integration: Success")
except:
	send = True
	print("Seventh integration: Failed")

try: 
	out = vice.output("example1_1")
	print("Reader: Success")
except:
	send = True
	print("Reader: Failed")

try:
	for i in vice.RECOGNIZED_ELEMENTS: 
		a = vice.integrated_cc_yield(i, rotating = True)
		a = vice.integrated_cc_yield(i, rotating = False)
		a = vice.integrated_cc_yield(i, IMF = "salpeter")
	print("IMF-integration of stellar yields: Success")
except:
	send = True
	print("IMF-integration of stellar yields: Failed")

if send:
	message = "At least one test failed. Please log which tests did not pass "
	message += "and submit a bug report to James Johnson at <giganano9@"
	message += "gmail.com>. Please also use 'BUG in VICE' as a subject. "
	message += "Thank you. "
	print(message)
else:
	print("All tests passed.")




