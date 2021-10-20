"""
This script runs the simulations of starburst models analyzed in
Johnson & Weinberg (2020).
"""

from __future__ import division, print_function
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import vice
except ModuleNotFoundError:
	raise ModuleNotFoundError("Could not import VICE.")
import math as m
import sys
import os
_TIMESTEP_ = float(sys.argv[1])
try:
	import numpy as np
	_SLOWBURST_TIMES_ = np.linspace(0, 14, 1401).tolist()
	_ALL_TIMES_ = np.linspace(0, 10, 10001).tolist()
	_TIMES_ = np.linspace(0, 10, 1001).tolist()
	bins = np.linspace(-3, 1, 401).tolist()
except ModuleNotFoundError:
	_SLOWBURST_TIMES_ = [0.01 * i for i in range(1401)]
	_ALL_TIMES_ = [_TIMESTEP_ * i for i in range(int(10 / _TIMESTEP_) + 1)]
	_TIMES_ = [0.01 * i for i in range(1001)]
	bins = [-3 + 0.01 * i for i in range(401)]
import warnings
warnings.filterwarnings("ignore")
import math as m
import sys
import os


def reset_yields():
	"""
	Sets the yields according to those in Johnson & Weinberg (2020).
	"""
	vice.yields.ccsne.settings["o"] = 0.015
	vice.yields.ccsne.settings["sr"] = 3.5e-8
	vice.yields.ccsne.settings["fe"] = 0.0012
	vice.yields.ccsne.settings["mg"] = 0.00261
	vice.yields.sneia.settings["o"] = 0.0
	vice.yields.sneia.settings["sr"] = 0.0
	vice.yields.sneia.settings["fe"] = 0.0017
	vice.yields.sneia.settings["mg"] = 0.0



# -------------------------- STARBURST GENERATORS -------------------------- #
def gas_driven_generator(onset, duration, amount):
	"""
	Generates a function of time which will serve as the infall history
	in Msun yr^-1 onto the galaxy.

	Parameters
	==========
	onset :: real number
		The time at which the starburst should start in Gyr
	duration :: real number
		The length of the starburst in Gyr
	amount :: real number
		The amount of "extra" gas to be added to the ISM over this time
		interval

	Returns
	=======
	The function describing the infall rate with time in Msun yr^-1
	"""
	def infall(t):
		ifr = 9.1
		if onset <= t < onset + duration: ifr += (1.e-9 * amount) / duration
		return ifr
	return infall


def eff_driven_generator(onset, duration, factor):
	"""
	Generates a function of time which will serve as the star formation
	efficiency timescale in Gyr.

	Parameters
	==========
	onset :: real number
		The time at which the starburst should start in Gyr
	duration :: real number
		The length of the starburst in Gyr
	factor :: real number
		The factor by which the SFE should increase

	Returns
	=======
	The function describing the SFE timescale with time in Gyr
	"""
	def tstar(t):
		baseline = 2
		if onset <= t < onset + duration: baseline /= factor
		return baseline
	return tstar


def slow_gaussian_generator(background, peak, height, std):
	"""
	Superimposes a slow gaussian on another function

	Parameters
	==========
	background :: <function>
		The function to superimpose the gaussian onto
	peak :: real number
		The time at which the gaussian peaks
	height :: real number
		The height of the gaussian at the peak
	std :: real number
		The standard deviation of the gaussian
	"""
	def slow_burst(t):
		return background(t) + height / (std * m.sqrt(2 * m.pi)) * m.exp(
			-(t - peak)**2 / (2 * std)**2)
	return slow_burst




# ----------------- FUNCTIONS FOR RUNNING STARBURST MODELS ----------------- #
def oscillatory(mean, amplitude, period, which, **kwargs):
	"""
	Runs a simulation in which a singlezone parameter oscillates with time,
	emulating a series of minor episodic starbursts

	Parameters
	==========
	mean :: real number
		The mean of the function
	amplitude :: real number
		The amplitude of the oscillations
	period :: real number
		The period of the oscillations in Gyr
	which :: str
		either "func" or "tau_star" - the attribute to assign the function to
	kwargs :: varying types
		Other keywords to pass to vice.singlezone as attributes
	"""
	kwargs[which] = lambda t: mean + amplitude * m.sin(2 * m.pi * t / period)
	if which == "func": kwargs["mode"] = "sfr"
	sz = vice.singlezone(**kwargs)
	print(sz)
	sz.run(_ALL_TIMES_[:], overwrite = True) # output at all times needed


def single_burst(which, generator, *gen_args, **kwargs):
	"""
	Runs a gas- or efficiency driven starburst simulation given a generator,
	parameters to pass to that generator, and keyword args to pass as
	attributes to vice.singlezone

	Parameters
	==========
	which :: str
		Either "func" or "tau_star" - the attribute to assign the function to
	generator :: <function>
		One of the two generators to use
	gen_args :: real numbers
		The parameters to pass to the generator function
	kwargs :: varying types
		Other keyword args to pass as attributes to a vice.singlezone object
	"""
	kwargs[which] = generator(*gen_args)
	outtimes = _TIMES_[:]
	for i in range(9):
		"""
		Force output to be written for the next 9 timesteps. The 10th is
		taken care of automatically given how we're defining the timestep size
		and output times
		"""
		outtimes.append(gen_args[0] * (i + 1) * kwargs["dt"])
	sz = vice.singlezone(**kwargs)
	print(sz)
	sz.run(outtimes[:], overwrite = True)


def run_gas_driven_models():
	"""
	Runs all gas-driven models
	"""
	run_sudden_onset_gas_driven_models()
	run_prolonged_gas_driven_models()


def run_sudden_onset_gas_driven_models():
	"""
	Runs the gas-driven starburst models
	"""
	kwargs = {
		"dt": 		_TIMESTEP_,
		"bins": 	bins[:]
	}
	single_burst("func", gas_driven_generator, *(2, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_2Gyr_5e9Msun", **kwargs)
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_5Gyr_5e9Msun", **kwargs)
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_5Gyr_5e9Msun_ts0p5", smoothing = 0.5,
		**kwargs)
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_5Gyr_5e9Msun_ts1p0", smoothing = 1.0,
		**kwargs)
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_5Gyr_5e9Msun_schmidt", schmidt = True,
		**kwargs)
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/sudden_5Gyr_5e9Msun_ts1p0_schmidt",
		smoothing = 1.0, schmidt = True, **kwargs)


def run_prolonged_gas_driven_models():
	"""
	Runs the prolonged gas-driven models
	"""
	kwargs = {
		"dt": 		_TIMESTEP_,
		"bins": 	bins[:]
	}
	single_burst("func", gas_driven_generator, *(5, 0.5, 5.e9),
		name = "simulations/prolonged_5Gyr_5e9Msun_0p5Gyr", **kwargs)
	single_burst("func", gas_driven_generator, *(5, 1.0, 5.e9),
		name = "simulations/prolonged_5Gyr_5e9Msun_1p0Gyr", **kwargs)


def run_efficiency_driven_models():
	"""
	Runs the efficiency driven models
	"""
	kwargs = {
		"dt": 		_TIMESTEP_,
		"bins": 	bins[:]
	}
	single_burst("tau_star", eff_driven_generator, *(2, 1, 2),
		name = "simulations/SFEdriven_2Gyr", **kwargs)
	single_burst("tau_star", eff_driven_generator, *(5, 1, 2),
		name = "simulations/SFEdriven_5Gyr", **kwargs)
	single_burst("tau_star", eff_driven_generator, *(5, 1, 2),
		name = "simulations/SFEdriven_5Gyr_ts0p5", smoothing = 0.5, **kwargs)
	single_burst("tau_star", eff_driven_generator, *(5, 1, 2),
		name = "simulations/SFEdriven_5Gyr_ts1p0", smoothing = 1.0, **kwargs)


def run_burstless_model(name = "simulations/default"):
	"""
	Runs the fiducial burstless model by giving the gas-driven generator a
	time of onset that is after the ending time of the simulation

	Parameters
	==========
	name :: str
		The name of the simulation. This is a default because there are
		several simulations that will be ran with these same parameters but
		different strontium yields
	"""
	single_burst("func", gas_driven_generator, *(12, _TIMESTEP_, 5.e9),
		name = name, dt = _TIMESTEP_, bins = bins[:])


def run_alternate_sr_yield_models():
	"""
	Runs the smooth models with alternate Sr yields
	"""
	kwargs = {
		"dt": 		_TIMESTEP_,
		"bins": 	bins[:]
	}
	vice.yields.ccsne.settings["sr"] = 0
	run_burstless_model(name = "simulations/yccsr_zero")
	vice.yields.ccsne.settings["sr"] = lambda z: 3.5e-8 * (z / 0.014)
	run_burstless_model(name = "simulations/yccsr_linear")
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/yccsr_linear_sudden_5Gyr_5e9Msun", **kwargs)
	single_burst("tau_star", eff_driven_generator, *(5, 1, 2),
		name = "simulations/yccsr_linear_SFEdriven_5Gyr", **kwargs)
	vice.yields.ccsne.settings["sr"] = lambda z: 1.e-7 * (1 - m.exp(
		-10 * (z / 0.014)))
	single_burst("func", gas_driven_generator, *(5, _TIMESTEP_, 5.e9),
		name = "simulations/yccsr_1-exp_sudden_5Gyr_5e9Msun", **kwargs)
	single_burst("tau_star", eff_driven_generator, *(5, 1, 2),
		name = "simulations/yccsr_1-exp_SFEdriven_5Gyr", **kwargs)
	run_burstless_model(name = "simulations/yccsr_1-exp")
	reset_yields()


def oscillatory(mean, amplitude, period, which, **kwargs):
	"""
	Runs a simulation in which a singlezone parameter oscillates with time,
	emulating a series of minor episodic starbursts

	Parameters
	==========
	mean :: real number
		The mean of the function
	amplitude :: real number
		The amplitude of the oscillations
	period :: real number
		The period of the oscillations in Gyr
	which :: str
		either "func" or "tau_star" - the attribute to assign the function to
	kwargs :: varying types
		Other keywords to pass to vice.singlezone as attributes
	"""
	kwargs[which] = lambda t: mean + amplitude * m.sin(2 * m.pi * t / period)
	if which == "func": kwargs["mode"] = "sfr"
	sz = vice.singlezone(**kwargs)
	print(sz)
	sz.run(_ALL_TIMES_[:], overwrite = True) # output at all times needed


def run_oscillatory_models():
	"""
	Runs the oscillatory history simulations
	"""
	kwargs = {
		"dt": 		_TIMESTEP_,
		"bins": 	bins[:]
	}
	# minus signs in SFE models b/c tau_star scales inversely w/SFR
	oscillatory(3, 0.3, 2, "func", name = "simulations/SFRoscil_amp0p3_per2",
		**kwargs)
	oscillatory(3, 0.6, 2, "func", name = "simulations/SFRoscil_amp0p6_per2",
		**kwargs)
	oscillatory(3, 0.3, 4, "func", name = "simulations/SFRoscil_amp0p3_per4",
		**kwargs)
	oscillatory(2, 0.2, -2, "tau_star",
		name = "simulations/SFEoscil_amp0p2_per2",**kwargs)
	oscillatory(2, 0.4, -2, "tau_star",
		name = "simulations/SFEoscil_amp0p4_per2",**kwargs)
	oscillatory(2, 0.2, -4, "tau_star",
		name = "simulations/SFEoscil_amp0p2_per4",**kwargs)


def run_slow_burst_models():
	"""
	Runs the slow burst models.
	"""
	kwargs = {
		"schmidt": 			True,
		"schmidt_index": 	0.5,
		"dt": 				_TIMESTEP_,
		"bins": 			bins[:]
	}
	sz1 = vice.singlezone(name = "simulations/slowburst_episodic_infall",
		func = slow_gaussian_generator(lambda t: 10 * t**2 * m.exp(-t / 2.2),
			12, 60, 1),
		Mg0 = 0,
		**kwargs)
	print(sz1)
	sz1.run(_SLOWBURST_TIMES_[:], overwrite = True)
	sz1.name = "simulations/episodic_infall"
	sz1.func = lambda t: 10 * t**2 * m.exp(-t / 2.2)
	print(sz1)
	sz1.run(_SLOWBURST_TIMES_[:], overwrite = True)
	sz2 = vice.singlezone(name = "simulations/slowburst_constant",
		func = slow_gaussian_generator(lambda t: 5, 12, 15, 1),
		mode = "sfr",
		**kwargs)
	print(sz2)
	sz2.run(_SLOWBURST_TIMES_[:], overwrite = True)
	sz2.name = "simulations/constant"
	sz2.func = lambda t: 5
	print(sz2)
	sz2.run(_SLOWBURST_TIMES_[:], overwrite = True)


def run_kirby2010_comparisons():
	"""
	Runs the models intended for comparison with the Kirby et al. (2010)
	data in the Appendix of Johnson & Weinberg (2020).
	"""
	kwargs = {
		"dt": 			_TIMESTEP_,
		"bins": 		bins[:],
		"Mg0": 			0,
		"tau_star": 	10,
		"eta": 			30,
		"elements": 	["fe", "sr", "mg"],
		"enhancement": 	3
	}
	sz1 = vice.singlezone(name = "simulations/kirby2010_smooth",
		func = lambda t: 9.1 * m.exp(-t / 2),
		**kwargs)
	print(sz1)
	sz1.run(_TIMES_, overwrite = True)
	sz1.name = "simulations/kirby2010_smooth_enh1"
	sz1.enhancement = 1
	print(sz1)
	sz1.run(_TIMES_, overwrite = True)
	def exp_with_burst(t):
		if 5. <= t < 5. + _TIMESTEP_:
			return 5 / _TIMESTEP_
		else:
			return 9.1 * m.exp(-t / 2)
	sz2 = vice.singlezone(name = "simulations/kirby2010_burst",
		func = exp_with_burst,
		**kwargs)
	print(sz2)
	outtimes = _TIMES_[:]
	for i in range(10):
		outtimes.append(5. + (i + 1) * _TIMESTEP_)
	sz2.run(outtimes[:], overwrite = True)


if __name__ == "__main__":
	reset_yields()
	run_burstless_model()
	run_gas_driven_models()
	run_efficiency_driven_models()
	run_alternate_sr_yield_models()
	run_oscillatory_models()
	run_slow_burst_models()
	run_kirby2010_comparisons()

