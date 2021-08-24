
Stellar Lifetimes 
-----------------
As a default, VICE adopts a single power law to describe the relationship 
between a star's mass and its lifetime (i.e. the 
*mass-lifetime relationship*, hereafter MLR): 

.. math:: \tau_\text{MS} = \tau_\odot m^{-\alpha} 

where :math:`\tau_\odot` is the sun's main sequence lifetime and :math:`\alpha` 
is the power-law index of the mass-lifetime relationship. 
The constants ``SOLAR_LIFETIME`` and ``MASS_LIFETIME_PLAW_INDEX``, both 
declared in ``vice/src/ssp.h``, assign the values of :math:`\tau_\odot` = 10 
Gyr and :math:`\alpha` = 3.5, respectively. 
Motivated by a popular exercise in undergradaute astronomy courses, this form 
follows from an assumed single-power law relating the mass and luminosity of 
stars: :math:`L \sim M^{1 + \alpha}`. 
Because the lifetime of a star scales with its luminosity per unit mass, the 
power-law then follows trivially: :math:`\tau \sim M/L \sim M/M^{1 + \alpha} 
\sim M^{-\alpha}`. 

VICE generalizes this form to describe the *total lifetime* of a star of mass 
:math:`m` by simply amplifying the main sequence lifetime by a factor of 
:math:`1 + p_\text{MS}`: 

.. math:: \tau_\text{total} = (1 + p_\text{MS})\tau_\odot m^{-\alpha} 

where :math:`p_\text{MS}` is the ratio of a star post main sequence lifetime 
to its main sequence lifetime (e.g. if the post main sequence lifetime is 
10% of the main sequence lifetime, then :math:`p_\text{MS}` = 0.1). 
As a consequence, this quantity describes the time interval between a star's 
formation and when it produces a remnant. 

By interpreting :math:`\tau_\text{total}` as lookback time, VICE solves for the 
mass of "remnant-producing" stars from a stellar population of known age: 

.. _mlr_m_postMS: 

.. math:: m_\text{postMS} = \left(\frac{\tau_\text{lookback}}{
	(1 + p_\text{MS})\tau_\odot}\right)^{-1/\alpha} 

Since these are the stars that are at the ends of the lifetimes, VICE adopts 
:math:`m_\text{postMS}` as written here as the mass of AGB stars enriching the 
interstellar medium at a given timestep. 
This equation also allows the solution of the *main sequence turnoff mass* by 
simply taking :math:`p_\text{MS}` = 0. 

The scaling of :math:`\tau_\text{MS} \sim m^{-3.5}` fails for higher mass stars 
(:math:`\gtrsim 4 M_\odot`). 
However, these stars generally have lifetimes that are short compared to the 
relevant timescales of galactic chemical evolution (:math:`\lesssim` 100 Myr 
compared to :math:`\sim` few Gyr). 
Regardless of its accuracy for low mass stars (:math:`\lesssim 0.5 M_\odot`), 
their lifetimes are considerably longer than the age of the universe anyway, 
and VICE does not support simulations on timescales longer than 15 Gyr. 
Consequently, this approximation generally suffices for galactic chemical 
evolution models. 

The important exception to this rule is that an accurate MLR for 
:math:`M \gtrsim 4 M_\odot` stars is necessary when considering elements with 
significant nucleosynthetic yields from these stars (e.g. nitrogen, Johnson 
et al. 2021 [1]_). 
Beginning with version 1.3.0, VICE recognizes a handful of additional forms of 
the MLR in order to fill this need: 

	- Larson (1974) [2]_ 

		This form is a metallicity-independent parabola in 
		:math:`\log\tau-\log m` space describing the main sequence lifetimes 
		only: 

		.. math:: \log_{10}\tau = \alpha + \beta\log_{10}m + \gamma 
			(\log_{10}m)^2 

		where the original values of :math:`\alpha` = 1.02, :math:`\beta` = 
		-3.57, and :math:`\gamma` = 0.90 were derived from a fit to the 
		compilation of evolutionary lifetimes presented in Tinsley (1972) [3]_. 
		VICE however adopts the updated values of :math:`\alpha` = 1.0, 
		:math:`\beta` = -3.42, and :math:`\gamma` = 0.88 from Kobayashi (2004) 
		[4]_ and David, Forman & Jones (1990) [5]_. 
		In detail, the value of :math:`\alpha` directly quantifies the log of 
		the main sequence lifetime of the sun :math:`\log_{10}\tau_\odot` in 
		whatever units :math:`\tau` is in (:math:`\alpha` = 1.0 for 
		:math:`\tau_\odot` = 10 Gyr; :math:`\alpha` = 10.0 for 
		:math:`\tau_\odot = 10^{10}` yr). 

		Solutions to the inverse function (i.e. mass as a function of lifetime) 
		follow directly from the quadratic formula: 
		:math:`\log_{10}m = (-\beta \pm \sqrt{\beta^2 - 4\gamma(\alpha - 
		\log_{10}\tau)}) / (2\gamma)`. 
		The correct solution comes when choosing subtraction in the numerator 
		as this corresponds to increasing lifetimes with decreasing stellar 
		mass. 

	- Maeder & Meynet (1989) [6]_ 

		This form is a metallicity-independent broken power-law quantifying 
		only the main sequence lifetimes: 

		.. math:: \tau = \Bigg \lbrace {
			10^{\alpha\log_{10}m + \beta}\ (m < 60 M_\odot) 
			\atop 
			1.2m^{-1.85} + 3\ \text{Myr}\ (m \geq 60 M_\odot) 
			} 

		where the values of :math:`\alpha` and :math:`\beta` are given by: 

		+------------------------------+------------------+------------------+ 
		| Mass Range                   | :math:`\alpha`   | :math:`\beta`    | 
		+------------------------------+------------------+------------------+ 
		| :math:`m \leq 1.3`           | -0.6545          | 1                | 
		+------------------------------+------------------+------------------+ 
		| :math:`1.3 < m \leq 3`       | -3.7             | 1.35             | 
		+------------------------------+------------------+------------------+ 
		| :math:`3 < m \leq 7`         | -2.51            | 0.77             | 
		+------------------------------+------------------+------------------+ 
		| :math:`7 < m \leq 15`        | -1.78            | 0.17             | 
		+------------------------------+------------------+------------------+ 
		| :math:`15 < m \leq 60`       | -0.86            | -0.94            | 
		+------------------------------+------------------+------------------+ 

		In detail, the values of :math:`\beta` shift linearly depending on the 
		choice of units for :math:`\tau`; those listed here are appropriate for 
		:math:`\tau` in Gyr. For a shift to :math:`\tau` in yr, all values 
		should increase by 9 (e.g. :math:`\beta` = 10.35 for masses between 
		1.3 and 3 :math:`M_\odot`). 

		Though this form was originally published in Maeder & Meynet (1989), 
		the exact form as written here was taken from Romano et al. (2005) [7]_. 
		While analytic solutions to the inverse function (i.e. mass as a 
		function of lifetime) are possible, VICE takes a numerical approach, 
		implementing a recursive version of the bisection algorithm described 
		in chapter 9 of Press, Teukolsky, Vetterling & Flannery (2007) [8]_. 

	- Padovani & Matteucci (1993) [9]_ 

		This form is a metallicity-independent curve describing the 
		main-sequence lifetime only: 

		.. math:: \log_{10}\tau = \frac{\alpha - \sqrt{\beta - \gamma 
			\left(\eta - \log_{10}m\right)}}{\mu} 

		The values of the coefficients are given by: 

		+------------------------+----------------+  
		| Coefficient            | Value          | 
		+------------------------+----------------+ 
		| :math:`\alpha`         | 0.334          | 
		+------------------------+----------------+ 
		| :math:`\beta`          | 1.790          | 
		+------------------------+----------------+ 
		| :math:`\gamma`         | 0.2232         | 
		+------------------------+----------------+ 
		| :math:`\eta`           | 7.764          | 
		+------------------------+----------------+ 
		| :math:`\mu`            | 0.1116         | 
		+------------------------+----------------+ 

		These values are appropriate for :math:`\tau` in units of Gyr. 
		Solutions to the inverse function (i.e. mass as a function of lifetime) 
		follow analytically. 
		Though this form was originally published in Padovani & Matteucci 
		(1993), the form as written here was taken from Romano et al. (2005). 

	- Kodama & Arimoto (1997) [10]_ 

		Using the stellar evolution code presented in Iwamoto & Saio (1999) 
		[11]_, Kodama & Arimoto tabulate the *total* lifetimes (i.e. including 
		post main sequence evolution) of stars as a function of both initial 
		mass and metallicity. 
		VICE stores internal data at 41 initial masses and 9 metallicities, 
		using 2-dimensional linear interpolation to approximate a smooth 
		function based on these discrete points. 

		Because of the necessary interpolation, solutions to the inverse 
		function (i.e. mass as a function of lifetime and metallicity) follow 
		numerically, for which VICE implements a recursive version of the 
		bisection algorithm described in chapter 9 of Press, Teukolsky, 
		Vetterling & Flannery (2007). 

	- Hurley, Pols & Tout (2000) [12]_ 

		This is a metallicity-dependent characterization of the main sequence 
		lifetimes of stars given by: 

		.. math:: \tau = \text{max}(\mu, x) t_\text{BGB} 

		where :math:`t_\text{BGB}` is the time required for a star to reach the 
		base of the giant branch on the Hertzsprung-Russell diagram: 

		.. math:: t_\text{BGB} = \frac{
			a_1 + a_2 m^4 + a_3 m^{5.5} + m^7 
			}{
			a_4 m^2 + a_5 m^7 
			}

		The coefficients :math:`a_n` vary with metallicity according to: 

		.. math:: a_n = \alpha_n + \beta_n \zeta + \gamma_n \zeta^2 + 
			\eta_n\zeta^3 

		VICE stores the values of :math:`\alpha`, :math:`\beta`, :math:`\gamma`, 
		and :math:`\eta` for the coefficients :math:`a_n` as internal data, and 
		the quantity :math:`\zeta` is related to the metallicity by mass 
		:math:`Z` by :math:`\zeta = \log_{10}(Z / 0.02)`. 
		The value of 0.02 corresponds to the metallicity of the sun; although 
		there has been some evolution in the accepted value of :math:`Z_\odot`, 
		VICE takes this value of 0.02 *always* when calculating lifetimes 
		according to the Hurley, Pols & Tout (2000) parameterization regardless 
		of the user's setting in a chemical evolution model. 

		The coefficients :math:`\mu` and :math:`x` are given by: 

		.. math:: \mu = \text{max}\left(0.5, 
			1.0 - 0.01 \text{max}\left(
			\frac{a_6}{m^{a_7}}, a_8 + \frac{a_9}{m^{a_{10}}} 
			\right)
			\right) 

		.. math:: x = \text{max}\left(0.95, 
			\text{min}\left[
			0.95 - 0.03\left(\zeta + 0.30103\right) 
			\right] 
			\right) 

		Solutions to the inverse function (i.e. mass as a function of lifetime 
		and metallicity) are numerical, for which VICE implements a recursive 
		version of the bisection algorithm described in chapter 9 of Press, 
		Teukolsky, Vetterling & Flannery (2007). 

	- Vincenzo et al. (2016) [13]_ 

		This form characterizes the total lifetimes of stars (i.e. including 
		the post main sequence evolution) as a function of stellar mass and 
		metallicity according to: 

		.. math:: \tau = A \exp(B m^{-C}) 

		where the coefficients :math:`A`, :math:`B`, and :math:`C` depend on 
		metallicity. 
		VICE stores their values sampled at 299 values of the metallicity 
		:math:`Z` as internal data, interpolating linearly between them to 
		approximate smooth functions out of the discrete points. 
		With their values known at a given metallicity, the inverse function 
		(i.e. mass as a function of lifetime) follows analytically from the 
		above equation. 

		Vincenzo et al. (2016) determined the values of these coefficients by 
		using isochrones computed using the PARSEC stellar evolution code 
		(Bressan et al. 2012 [14]_; Tang et al. 2014 [15]_; Chen et al. 2015 
		[16]_) in combination with a one-zone chemical evolution model to 
		reproduce the color-magnitude diagram of the Sculptor dwarf galaxy. 

:ref:`Here <fig_mlr>` we plot stellar lifetime as a function of progenitor mass 
according to each of these forms along with the single power-law described 
above; its failure at high masses compared to the other, more sophisticated 
parameterizations is quite clear. 
VICE affords users the ability to evaluate these functions using the 
``vice.mlr`` module (e.g. ``vice.mlr.hpt2000`` correspond to the Hurley, Pols 
& Tout (2000) form, and ``vice.mlr.ka1997`` to the Kodama & Arimoto (1997) 
form). 
The form to be adopted in all chemical evolution models and single stellar 
population calculations is assigned via a global setting stored at 
``vice.mlr.setting``. 


Relevant source code: 

	- ``vice/core/mlr.py`` 
	- ``vice/src/ssp.h`` 
	- ``vice/src/ssp/mlr.c`` 
	- ``vice/src/ssp/mlr/powerlaw.c`` 
	- ``vice/src/ssp/mlr/vincenzo2016.c`` 
	- ``vice/src/ssp/mlr/hpt2000.c`` 
	- ``vice/src/ssp/mlr/ka1997.c`` 
	- ``vice/src/ssp/mlr/pm1993.c`` 
	- ``vice/src/ssp/mlr/mm1989.c`` 
	- ``vice/src/ssp/mlr/larson1974.c`` 
	- ``vice/src/ssp/mlr/root.c`` 

.. [1] Johnson et al. (2021), in prep 
.. [2] Larson (1974), MNRAS, 166, 585 
.. [3] Tinsley (1972), A&A, 20, 383 
.. [4] Kobayashi (2004), MNRAS, 347, 74 
.. [5] David, Forman & Jones (1990), ApJ, 359, 29 
.. [6] Maeder & Meynet (1989), A&A, 210, 155 
.. [7] Romano et al. (2005), A&A, 430, 491 
.. [8] Press, Teukolsky, Vetterling & Flannery (2007), Numerical Recipes, 
	Cambridge University Press 
.. [9] Padovani & Matteucci (1993), ApJ, 416, 26 
.. [10] Kodama & Arimoto (1997), A&A, 320, 41 
.. [11] Iwamoto & Saio (1999), ApJ, 521, 297 
.. [12] Hurley, Pols & Tout (2000), MNRAS, 315, 543 
.. [13] Vincenzo et al. (2016), MNRAS, 460, 2238 
.. [14] Bressan et al. (2012), MNRAS, 427, 127 
.. [15] Tang et al. (2014), MNRAS, 445, 4287 
.. [16] Chen et al. (2015), MNRAS, 452, 1068 

