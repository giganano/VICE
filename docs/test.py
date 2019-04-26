"""
The following runs every history from the example and template files ensuring 
that there are no errors. 
"""

from __future__ import print_function
import math as m
try:
	import numpy as np
	times = np.linspace(0, 10, 1001)
except ImportError:
	times = 1001 * [0.]
	for i in range(1001):
		times[i] = 0. + 0.001 * i
import warnings 
warnings.filterwarnings("ignore")

try:
	import vice
except ImportError:
	message = "VICE is not installed. Please see <https://github.com/giganano/"
	message += "VICE> for installation instructions. If you have followed " 
	message += "the proper steps to install and are still receiving this " 
	message += "message, please open an issue at the linked web page." 
	raise ImportError(message)

message = "Running tests on the integration features, output reader, and "
message += "yield-weighted IMF-integrator. This may take a few minutes, "
message += "depending on the processing speed of the system."
print(message)
send = False 

try:
	for i in vice._RECOGNIZED_ELEMENTS_: 
		a = vice.agb_yield_grid(i)
		a = vice.fractional_cc_yield(i)
		a = vice.fractional_cc_yield(i, study = "WW95")
		a = vice.fractional_ia_yield(i, model = "N1")
		a = vice.fractional_ia_yield(i, model = "N100")
		a = vice.fractional_ia_yield(i, model = "N5")
		a = vice.fractional_ia_yield(i, study = "iwamoto99", model = "W70")
		a = vice.fractional_ia_yield(i, study = "iwamoto99", model = "WDD1") 
	print("IMF-integration of stellar yields: Success")
except:
	send = True
	print("IMF-integration of stellar yields: Failed")
	
try:
	for i in vice._RECOGNIZED_ELEMENTS_:
		a = vice.single_stellar_population(i)
		a = vice.single_stellar_population(i, Z = 0.001)
	print("Single Stellar Population Enrichment: Success")
except:
	send = True
	print("Single Stellar Population Enrichment: Failed")

try:
	first = vice.singlezone(name = "example1_1", dt = 0.005)
	out1 = first.run(times, capture = True, overwrite = True)
	print("First integration: Success")
except: 
	send = True
	print("First integration: Failed")

try:
	second = vice.singlezone(name = "example1_2", dt = 0.005)
	second.func = lambda t: m.exp( -t / 3 )
	second.Mg0 = 1.
	out2 = second.run(times, capture = True, overwrite = True)
	print("Second integration: Success")
except:
	send = True
	print("Second integration: Failed")

try:
	third = vice.singlezone(name = "example1_3", schmidt = True, dt = 0.005)
	third.func = lambda t: m.exp( -t / 3 )
	third.Mg0 = 1.
	out3 = third.run(times, capture = True, overwrite = True)
	print("Third integration: Success")
except:
	send = True
	print("Third integration: Failed")

try:
	bolus = vice.singlezone(name = "bolus", dt = 0.005)
	def f(t):
		if 5 <= t < 5.001:
			return 5000
		else:
			return 9.1
	bolus.func = f
	out1 = bolus.run(times, capture = True, overwrite = True)
	print("Fourth integration: Success")
except:
	send = True
	print("Fourth integration: Failed")

try: 
	ifrboost = vice.singlezone(name = "ifrboost", schmidt = True, dt = 0.005)
	def f(t):
		if 5 <= t <= 6:
			return 14.1
		else:
			return 9.1
	ifrboost.func = f
	out2 = ifrboost.run(times, capture = True, overwrite = True)
	print ("Fifth integration: Success")
except:
	send = True
	print("Fifth integration: Failed")

try:
	sfeboost = vice.singlezone(name = "sfeboost", dt = 0.005)
	sfeboost.func = lambda t: m.exp( -t / 3 )
	def f(t):
		if 5 <= t <= 6:
			return 1.
		else:
			return 2.
	sfeboost.tau_star = f
	sfeboost.Mg0 = 1.
	out3 = sfeboost.run(times, capture = True, overwrite = True)
	print("Sixth integration: Success")
except:
	send = True
	print("Sixth integration: Failed")

try:
	sfe_schmidt = vice.singlezone(name = "sfe_schmidt", schmidt = True, 
		dt = 0.005)
	sfe_schmidt.func = lambda t: m.exp( -t / 3 )
	sfe_schmidt.tau_star = f
	sfe_schmidt.Mg0 = 1.
	out4 = sfe_schmidt.run(times, capture = True, overwrite = True)
	print("Seventh integration: Success")
except:
	send = True
	print("Seventh integration: Failed")

try:
	custom_dtd = vice.singlezone(name = "custom_dtd", dt = 0.005)
	def f(t):
		if t < 1:
			return 10
		else:
			return 125.89254 * t**(-1.1)
	custom_dtd.ria = f
	out = custom_dtd.run(times, capture = True, overwrite = True)
	print("Eighth integration: Success")
except:
	send = True
	print("Eighth integration: Failed")

try:
	custom_ria = vice.singlezone(name = "custom_ria", dt = 0.005)
	custom_ria.ria = lambda t: (t - custom_ria.delay) * m.exp( -(t - 
		custom_ria.delay) / 2 )
	custom_ria.elements = ['o', 'fe']
	custom_ria.zin = len(custom_ria.elements) * [0]
	custom_ria.zin['fe'] = 0.1 * vice.solar_z['fe']
	custom_ria.zin['o'] = lambda t: 0.1 * vice.solar_z['o'] * (t / 10.0)
	vice.ccsne_yields['fe'] /= 2
	out5 = custom_ria.run(times, capture = True, overwrite = True)
	print("Ninth integration: Success")
except:
	send = True
	print("Ninth integration: Failed")

try: 
	custom_sfr = vice.singlezone(name = "custom_sfr", 
		func = lambda t: 3 * m.exp( -t / 4.), 
		dt = 0.005) 
	out = custom_sfr.run(times, capture = True, overwrite = True)
	print("Tenth integration: Success") 
except: 
	print("Tenth Integration: Failed") 
	send = True 

try: 
	fixed_gas = vice.singlezone(name = "fixed_gas", 
		func = lambda t: 6.0e9, dt = 0.005) 
	out = fixed_gas.run(times, capture = True, overwrite = True) 
	print("Eleventh Integration: Success") 
except: 
	print("Eleventh Integration: Failed") 
	send = True 

try: 
	out = vice.output("example1_1")
	print("Reader: Success")
except:
	send = True
	print("Reader: Failed")

try: 
	mir = vice.mirror(vice.output("example1_1")) 
	print("Mirror: Success") 
except: 
	print("Mirror: Failed")

if send:
	message = "At least one test failed. Please log which tests did not pass "
	message += "and either submit a bug report to James Johnson at <giganano9@"
	message += "gmail.com> or open an issue at https://github.com/giganano/"
	message += "VICE.git. Please also use 'BUG in VICE' as a subject if you "
	message += "choose to send an email. Thank you. "
	print(message)
else:
	print("All tests passed.")

try: 
	import dill 
except ImportError: 
	print("""\
================================================================================
Package 'dill' not found. This package is required for encoding functional 
attributes with VICE outputs. It is recommended that VICE users install this 
package to make use of these features. This can be done via 'pip install dill'. 
================================================================================\
""")




