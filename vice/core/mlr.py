
from ._mlr import (_get_setting, _set_setting, _powerlaw, _vincenzo2016, 
	_hpt2000, _ka1997, _pm1993, _mm1989, _larson1974) 

__POWERLAW__ = _powerlaw() 
__VINCENZO2016__ = _vincenzo2016() 
__HPT2000__ = _hpt2000() 
__KA1997__ = _ka1997() 
__PM1993__ = _pm1993() 
__MM1989__ = _mm1989() 
__LARSON1974__ = _larson1974() 


class mlr: 

	r""" 
	The Mass-Lifetime Relationship (MLR) for Stars: VICE provides several 
	functional forms available for individual calculations as well as for use 
	in chemical evolution models. 

	.. versionadded:: 1.3.0 

	Contents 
	--------
	setting : ``str`` 
		A string denoting which of the following functional forms is to 
		describe the MLR in all chemical evolution models. 
	powerlaw : <function> 
		The MLR parameterized by a single power-law, a popular exercise in 
		undergraduate astronomy courses. 
	vincenzo2016 : <function> 
		The MLR as characterized by Vincenzo et al. (2016) [1]_. 
	hpt2000 : <function> 
		The MLR as described in Hurley, Pols & Tout (2000) [2]_. 
	ka1997 : <function> 
		The MLR as tabulated in Kodama & Arimoto (1997) [3]_. 
	pm1993 : <function> 
		The MLR as formulated by Padovani & Matteucci (1993) [4]_. 
	mm1989 : <function> 
		The MLR as characterized by Maeder & Meynet (1989) [5]_. 
	larson1974 : <function> 
		The MLR as parameterized by Larson (1974) [6]_. 

	.. note:: For reasons relating to the implementation, this set of functions 
		is not a module but an object. Consequently, importing them with 
		``from vice import mlr`` will work fine, but for example 
		``from vice.mlr import vincenzo2016`` will produce a 
		``ModuleNotFoundError``. If necessary, new variables can always be 
		assigned to map to these functions (e.g. 
		``vincenzo2016 = vice.mlr.vincenzo2016``). 

	.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238 
	.. [2] Hurley, Pols & Tout (2000), MNRAS, 315, 543 
	.. [3] Kodama & Arimoto (1997), A&A, 320, 41 
	.. [4] Padovani & Matteucci (1993), ApJ, 416, 26 
	.. [5] Maeder & Meynet (1989), A&A, 210, 155 
	.. [6] Larson (1974), MNRAS, 166, 585 
	""" 

	def __init__(self): 
		self._powerlaw = _powerlaw() 
		self._vincenzo2016 = _vincenzo2016() 
		self._hpt2000 = _hpt2000() 
		self._ka1997 = _ka1997() 
		self._pm1993 = _pm1993() 
		self._mm1989 = _mm1989() 
		self._larson1974 = _larson1974() 

	@property 
	def setting(self): 
		r""" 
		Type : str [assignment is case-insensitive] 

		Default : "powerlaw" 

		.. versionadded:: 1.3.0 

		A keyword denoting which functional form of the mass-lifetime relation 
		to adopt in chemical evolution models. Allowed keywords and the 
		journal references for them: 

		- "powerlaw" : N/A 
		- "vincenzo2016": Vincenzo et al. (2016) [1]_ 
		- "hpt2000": Hurley, Pols & Tout (2000) [2]_ 
		- "ka1997": Kodama & Arimoto (1997) [3]_ 
		- "pm1993": Padovani & Matteucci (1993) [4]_ 
		- "mm1989": Maeder & Meynet (1989) [5]_ 
		- "larson1974": Larson (1974) [6]_ 

		.. seealso:: 

			- vice.mlr.powerlaw 
			- vice.mlr.vincenzo2016 
			- vice.mlr.hpt2000 
			- vice.mlr.ka1997 
			- vice.mlr.pm1993 
			- vice.mlr.mm1989 
			- vice.mlr.larson1974 

		Example Code 
		------------
		>>> import vice 
		>>> vice.mlr.setting 
		"powerlaw" 
		>>> vice.mlr.setting = "KA1997" 
		>>> vice.mlr.setting 
		"ka1997" 
		>>> vice.mlr.setting = "hpt2000" 
		>>> vice.mlr.setting 
		"hpt2000" 

		.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238 
		.. [2] Hurley, Pols & Tout (2000), MNRAS, 315, 543 
		.. [3] Kodama & Arimoto (1997), A&A, 320, 41 
		.. [4] Padovani & Matteucci (1993), ApJ, 416, 26 
		.. [5] Maeder & Meynet (1989), A&A, 210, 155 
		.. [6] Larson (1974), MNRAS, 166, 585 
		""" 
		return _get_setting() 

	@setting.setter 
	def setting(self, value): 
		_set_setting(value) 

	@staticmethod 
	def powerlaw(qty, postMS = 0.1, which = "mass"): # metallicity independent 
		r""" 
		Compute either the lifetime or the mass of a dying star according to a 
		single power-law relationship between the two. 

		**Signature**: vice.mlr.powerlaw(qty, postMS = 0.1, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretation set by the keyword 
			argument ``which``. 
		postMS : float [default : 0.1] 
			The ratio of a star's post main sequence lifetime to its main 
			sequence lifetime. Zero to compute the main sequence lifetime 
			alone, or the main sequence turnoff mass when ``which == "age"``. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass in Gyr 
			according to the single power law. 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		This power-law is of the following form: 

		.. math:: \tau = (1 + \alpha_\text{MS}) \tau_\odot 
			\left(\frac{M}{M_\odot}\right)^{-\gamma} 

		where :math:`\tau_\odot` is the main sequence lifetime of the sun 
		(taken to be 10 Gyr), :math:`\alpha_\text{MS}` is the parameter 
		``postMS``, and :math:`\gamma` is the power-law index, taken to be 3.5. 

		This form of the mass-lifetime relation can be derived from the scaling 
		relation: 

		.. math:: \frac{\tau}{\tau_\odot} \sim \frac{M/M_\odot}{L/L_\odot} 

		where :math:`L` is the luminosity of a star assuming 
		:math:`L \sim M^{4.5}`, a popular exercise in undergraduate astronomy 
		courses. 
		""" 
		return __POWERLAW__(qty, postMS = postMS, which = which)  

	@staticmethod 
	def vincenzo2016(qty, Z = 0.014, which = "mass"): # total lifetime 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Vincenzo et al. (2016) [1]_. 

		**Signature**: vice.mlr.vincenzo2016(qty, Z = 0.014, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		Z : float [default : 0.014] 
			The metallicity by mass of the stellar population. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to the Vincenzo et al. (2016) 
			relation. 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		This relation is of the following functional form: 

		.. math:: \tau = A \exp(B m^{-C}) 

		where :math:`A`, :math:`B`, and :math:`C` are functions of metallicity. 
		Vincenzo et al. (2016) computed the values of these coefficients 
		using the PARSEC stellar evolution code (Bressan et al. 2012 [2]_; 
		Tang et al. 2014 [3]_; Chen et al. 2015 [4]_) which were then used in 
		combination with a one-zone chemical evolution model to reproduce the 
		color-magnitude diagram of the Sculptor dwarf galaxy. 

		.. [1] Vincenzo et al. (2016), MNRAS, 460, 2238 
		.. [2] Bressan et al. (2012), MNRAS, 427, 127 
		.. [3] Tang et al. (2014), MNRAS, 445, 4287 
		.. [4] Chen et al. (2015), MNARS, 452, 1068 
		""" 
		return __VINCENZO2016__(qty, Z = Z, which = which)  

	@staticmethod 
	def hpt2000(qty, postMS = 0.1, Z = 0.014, which = "mass"): 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Hurley, Pols & Tout (2000) [1]_. 

		**Signature**: vice.mlr.hpt2000(qty, postMS = 0.1, Z = 0.014, 
		which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		postMS : float [default : 0.1] 
			The ratio of a star's post main sequence lifetime to its main 
			sequence lifetime. Zero to compute the main sequence lifetime 
			alone, or the main sequence turnoff mass when ``which == "age"``. 
		Z : float [default : 0.014] 
			The metallicity by mass of the stellar population. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to the Hurley, Pols & Tout (2000) 
			relation. 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		The Hurley, Pols & Tout (2000) relation quantifies the main sequence 
		lifetime according to (see their section 5.1): 

		.. math:: t_\text{MS} = t_\text{BGB} \text{max}(\mu, x) 

		where :math:`t_\text{BGB}` is the time required for the star to reach 
		the base of the giant branch (BGB), given by: 

		.. math:: t_\text{BGB} = \frac{
				a_1 + a_2 M^4 + a_3 M^{5.5} + M^7 
			}{
				a_4 M^2 + a_5 M^7 
			} 

		where :math:`M` is the mass of the star in solar masses and the 
		coefficients :math:`a_n` depend on metallicity in a manner described in 
		their Appendix A. The quantities :math:`\mu` and :math:`x` are given by 

		.. math:: \mu = \text{max}\left(0.5, 1.0 - 0.01\text{max}\left(
			\frac{a_6}{M^{a_7}}, a_8 + \frac{a_9}{M^{a_{10}}}\right)\right) 

		and 

		.. math:: x = \text{max}(0.95, \text{min}(0.95 - 0.03(\zeta + 0.30103), 
			0.99)) 

		where :math:`\zeta` is calculated from the metallicity by mass 
		:math:`Z` according to :math:`\zeta = \log_{10}(Z / 0.02)`. 

		In calculating stellar masses from ages (i.e. when ``which == "age"``), 
		the equation must be solved numerically. For this, VICE makes use of 
		the bisection root-finding algorithm described in chapter 9 of Press, 
		Teukolsky, Vetterling & Flannery (2007) [2]_. 

		.. [1] Hurley, Pols & Tout (2000), MNRAS, 315, 543 
		.. [2] Press, Teukolsky, Vetterling & Flannery (2007), Numerical 
			Recipes, Cambridge University Press 
		""" 
		return __HPT2000__(qty, postMS = postMS, Z = Z, which = which) 

	@staticmethod 
	def ka1997(qty, Z = 0.014, which = "mass"): # total lifetime 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Kodama & Arimoto (1997) [1]_. 

		**Signature**: vice.mlr.ka1997(qty, Z = 0.014, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		Z : float [default : 0.014] 
			The metallicity by mass of the stellar population. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to Kodama & Arimoto (1997). 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		Kodama & Arimoto (1997) quantified their mass-lifetime relation using 
		stellar evolution tracks computed with the code presented in Iwamoto & 
		Saio (1999) [2]_. They report lifetimes on a table of stellar mass and 
		metallicity, which VICE stores as internal data. To compute lifetimes 
		at any mass and metallicity, it runs a 2-dimensional linear 
		interpolation function between the appropriate elements of the 
		mass-metallicity grid, linearly extrapolating to higher or lower masses 
		or metallicities as needed. 

		Because an interpolation scheme is used to compute lifetimes, inverting 
		the relationship to compute masses from ages must be done numerically. 
		For this, VICE makes use of the bisection root-finding algorithm 
		described in chapter 9 of Press, Teukolsky, Vetterling & Flannery 
		(2007) [3]_. 

		.. [1] Kodama & Arimoto (1997), A&A, 320, 41 
		.. [2] Iwamoto & Saio (1999), ApJ, 521, 297 
		.. [3] Press, Teukolsky, Vetterling & Flannery (2007), Numerical 
			Recipes, Cambridge University Press 
		""" 
		return __KA1997__(qty, Z = Z, which = which)  

	@staticmethod 
	def pm1993(qty, postMS = 0.1, which = "mass"): # metallicity independent 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Padovani & Matteucci (1993) [1]_. 

		**Signature**: vice.mlr.pm1993(qty, postMS = 0.1, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		postMS : float [default : 0.1] 
			The ratio of a star's post main sequence lifetime to its main 
			sequence lifetime. Zero to compute the main sequence lifetime 
			alone, or the main sequence turnoff mass when ``which == "age"``. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to Padovani & Matteucci (1993). 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		Padovani & Matteucci (1993) parameterize the mass-lifetime relation 
		according to: 

		.. math:: \tau = 10^{(\alpha - \sqrt{\beta - \gamma(\eta - 
			\log_{10}(M/M_\odot))})/\mu}\text{ Gyr} 

		for stellar masses below 6.6 :math:`M_\odot` and 

		.. math:: \tau = 1.2(M/M_\odot)^{-1.85} + 0.003\text{ Gyr} 

		for masses above 6.6 :math:`M_\odot`. Below 0.6 :math:`M_\odot`, the 
		lifetime flattens off at 160 Gyr. The coefficients :math:`\alpha`, 
		:math:`\beta`, :math:`\gamma`, :math:`\eta`, and :math:`\mu` are given 
		below: 

		+------------------+----------+
		| :math:`\alpha`   | 0.334    | 
		+------------------+----------+
		| :math:`\beta`    | 1.790    | 
		+------------------+----------+
		| :math:`\gamma`   | 0.2232   | 
		+------------------+----------+
		| :math:`\eta`     | 7.764    | 
		+------------------+----------+
		| :math:`\mu`      | 0.1116   | 
		+------------------+----------+

		Though this form was originally published in Padovani & Matteucci 
		(1993), in detail the form here is taken from Romano et al. (2005) [2]_. 

		.. [1] Padovani & Matteucci (1993), ApJ, 416, 26 
		.. [2] Romano et al. (2005), A&A, 430, 491 
		""" 
		return __PM1993__(qty, postMS = 0.1, which = "mass")  

	@staticmethod 
	def mm1989(qty, postMS = 0.1, which = "mass"): # metallicity independent 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Maeder & Meynet (1989) [1]_. 

		**Signature**: vice.mlr.mm1989(qty, postMS = 0.1, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		postMS : float [default : 0.1] 
			The ratio of a star's post main sequence lifetime to its main 
			sequence lifetime. Zero to compute the main sequence lifetime 
			alone, or the main sequence turnoff mass when ``which == "age"``. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to Maeder & Meynet (1989). 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		The mass-lifetime relation of Maeder & Meynet (1989) is given by: 

		.. math:: \tau = 10^{\alpha \log_{10}(M/M_\odot) + \beta} 

		for stellar masses below 60 :math:`M_\odot`. Above this mass, the 
		lifetime is given by: 

		.. math:: \tau = 1.2\left(\frac{M}{M_\odot}\right)^{-1.85} + 0.003 

		and in both cases, :math:`\tau` is in Gyr. 

		Though this form was originally published in Maeder & Meynet (1989), 
		in detail the form here is taken from Romano et al. (2005) [2]_. 

		.. [1] Maeder & Meynet (1989), A&A, 210, 155 
		.. [2] Romano et al. (2005), A&A, 430, 491 
		""" 
		return __MM1989__(qty, postMS = postMS, which = which)  

	@staticmethod 
	def larson1974(qty, postMS = 0.1, which = "mass"): # metallicity independent 
		r""" 
		Compute either the lifetime or the mass of a dying star according to 
		the mass-lifetime relation of Larson (1974) [1]_. 

		**Signature**: vice.mlr.larson1974(qty, postMS = 0.1, which = "mass") 

		.. versionadded:: 1.3.0 

		Parameters 
		----------
		qty : float 
			Either the mass of a star in :math:`M_\odot` or the age of a 
			stellar population in Gyr. Interpretion set by the keyword 
			argument ``which``. 
		postMS : float [default : 0.1] 
			The ratio of a star's post main sequence lifetime to its main 
			sequence lifetime. Zero to compute the main sequence lifetime 
			alone, or the main sequence turnoff mass when ``which == "age"``. 
		which : str [case-insensitive] [default : "mass"] 
			The interpretation of ``qty``: either ``"mass"`` or ``"age"`` 
			(case-insensitive). If ``which == "mass"``, then ``qty`` represents 
			a stellar mass in :math:`M_\odot` and this function will compute a 
			lifetime in Gyr. Otherwise, ``qty`` represents the age of a stellar 
			population and the mass of a star with the specified lifetime will 
			be calculated. 

		Returns 
		-------
		x : float 
			If ``which == "mass"``, the lifetime of a star of that mass and 
			metallicity in Gyr according to Larson (1974). 
			If ``which == "age"``, the mass of a star in :math:`M_\odot` with 
			the specified lifetime in Gyr. 

		Notes 
		-----
		Larson (1974) present the following fit to the compilation of 
		evolutionary lifetimes presented in Tinsley (1972) [2]_: 

		.. math:: \log_{10} \tau = \alpha + \beta \log_{10}(M/M_\odot) + 
			\gamma (\log_{10}(M/M_\odot))^2 

		where :math:`\alpha` = 1 for :math:`\tau` measured in Gyr, 
		:math:`\beta` = -3.42, and :math:`\gamma` = 0.88. 

		Though this form was originally presented in Larson (1974), the values 
		of the coefficients were taken from David, Forman & Jones (1990) [3]_ 
		and Kobayashi (2004) [4]_. 

		.. [1] Larson (1974), MNRAS, 166, 585 
		.. [2] Tinsley (1972), A&A, 20, 383 
		.. [3] David, Forman & Jones (1990), ApJ, 359, 29 
		.. [4] Kobayashi (2004), MNRAS, 347, 74 
		""" 
		return __LARSON1974__(qty, postMS = postMS, which = which)  


mlr = mlr() 

