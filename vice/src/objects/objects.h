/*
 * All of VICE's objects are declared in this header.
 */

#ifndef OBJECTS_OBJECTS_H
#define OBJECTS_OBJECTS_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include <stdio.h> /* for FILE object */


typedef struct callback_1arg {

	/*
	 * An object whose sole purpose is to call a python function via cython.
	 *
	 * callback: A function pointer to a cdef double function which will
	 * 		return the value returned by the python function itself
	 * assumed_constant: A value to return in the case that the user has not
	 * 		specified a function.
	 * user_func: A void pointer to the PyObject corresponding to the user's
	 * 		function defined in python
	 *
	 * Notes
	 * =====
	 * The attribute assumed_constant allows a callback function to be adopted
	 * for parameters which may be either a real number or a function.
	 */

	double (*callback)(double, void *);
	double assumed_constant;
	void *user_func;

} CALLBACK_1ARG;


typedef struct callback_2arg {

	/*
	 * An object whose sole purpose is to call a python function via cython.
	 *
	 * callback: A function pointer to a cdef double function which will
	 * 		return the value returned by the python function itself
	 * assumed_constant: A value to return in the case that the user has not
	 * 		specified a function.
	 * user_func: A void pointer to the PyObject corresponding to the user's
	 * 		function defined in python
	 * Notes
	 * =====
	 * The attribute assumed_constant allows a callback function to be adopted
	 * for parameters which may be either a real number or a function. This
	 * applies more to CALLBACK_1ARG in this iteration of VICE, but is
	 * retained here for consistency.
	 */
	double (*callback)(double, double, void *);
	double assumed_constant;
	void *user_func;

} CALLBACK_2ARG;


typedef struct interpolation_sceme_1d {

	/*
	 * This struct holds the necessary information for a 1-dimensional
	 * interpolation scheme, simply constructing a continuous function out of
	 * a series of (x, y) points and connecting them with lines.
	 *
	 * n_points: The number of points in the scheme.
	 * xcoords: The x-coordinates in arbitrary units.
	 * ycoords: The y-coordinates in arbitrary units.
	 *
	 * Notes
	 * =====
	 * Both xcoords and ycoords pointers always store n_points numbers, and are
	 * assumed to be sorted from least to greatest. This is enforced in Python.
	 */

	unsigned long n_points;
	double *xcoords;
	double *ycoords;

} INTERP_SCHEME_1D;


typedef struct interpolation_scheme_2d {

	/*
	 * This struct holds the necessary information for a 2-dimensional
	 * interpolation scheme, simply constructing a continuous function out of
	 * a series of (x, y, z) points and linearly interpolating between them.
	 *
	 * n_x_points: The number of x-coordinates in the scheme.
	 * n_y_points: The number of y-coordinates in the scheme.
	 * xcoords: The x-coordinates in arbitrary units.
	 * ycoords: The y-coordinates in arbitrary units.
	 * zcoords: The z-coordinates in arbitrary units.
	 *
	 * Notes
	 * =====
	 * Both xcoords and ycoords are assumed to be sorted from least to greatest,
	 * and this is enforced in Python. The zcoords array will have the
	 * x-coordinate as the first axis, and is thus n_x_points-by-n_y_points.
	 * This object as a result stores n_x_points times n_y_points total
	 * (x, y, z) coordinate combinations.
	 */

	unsigned long n_x_values;
	unsigned long n_y_values;
	double *xcoords;
	double *ycoords;
	double **zcoords;

} INTERP_SCHEME_2D;


typedef struct asymptotic_giant_branch_star_yield_grid {

	/*
	 * This struct holds the yield grid from asymptotic giant branch stars
	 * for a given element.
	 *
	 * custom_yield: A callback object for a function of mass and metallicity
	 * 		Z that the user constructed in python.
	 * interpolator: The mass-metallicity interpolation grid
	 * entrainment: The fraction of this element's yields that get mixed
	 * 		with the ISM.
	 */

	CALLBACK_2ARG *custom_yield;
	INTERP_SCHEME_2D *interpolator;
	double entrainment;

} AGB_YIELD_GRID;


typedef struct ccsne_yield_specs {

	/*
	 * This struct contains information on a given elements yields from core
	 * collapse supernovae (CCSNe).
	 *
	 * yield_: A callback object corresponding to the user's yield settings.
	 * 		Both functional values and constant values are stored there.
	 * entrainment: The fraction of the nucleosynthetic yield that is
	 * 		captured and retained by the interstellar medium
	 */

	CALLBACK_1ARG *yield_;
	double entrainment;

} CCSNE_YIELD_SPECS;


typedef struct sneia_yield_specs {

	/*
	 * This struct holds the yield specifications for type Ia supernovae
	 * (SNe Ia).
	 *
	 * yield_: A callback object corresponding to the user's yield settings.
	 * 		Both functionals values and constant values are stored there.
	 * RIa: The normed Ia rate itself
	 * dtd: A string denoting a built-in Ia delay-time distribution, if adopted
	 * 		by the user
	 * tau_ia: The e-folding timescale of SNe Ia, when dtd == "exp".
	 * t_d: The minimum delay time on SNe Ia in Gyr.
	 * entrainment: The fraction of the nucleosynthetic yield that is
	 * 		captured and retained by the interstellar medium
	 */

	CALLBACK_1ARG *yield_;
	double *RIa;
	char *dtd;
	double tau_ia;
	double t_d;
	double entrainment;


} SNEIA_YIELD_SPECS;


typedef struct arbitrary_channel {

	/*
	 * This struct holds the information and yield specifications for
	 * arbitrary channels of enrichment.
	 *
	 * yield_: A callback object corresponding the user's yield settings.
	 * grid: The grid of metallicities on which the yields themselves are
	 * 		sampled.
	 * rate: The delay-time distribution of the channel: its rate following the
	 * 		formation of a simple stellar population.
	 */

	CALLBACK_1ARG *yield_;
	double *rate;
	double entrainment;

} CHANNEL;


typedef struct element {

	/*
	 * This struct contains information on each individual element's abundance
	 * and yields.
	 *
	 * agb_grid: The struct holding this element's AGB star yield information
	 * ccsne_yield: The struct holding this element's CCSNe yield information
	 * SNEIA_YIELD: The struct holding this element's SNeIa yield information
	 * symbol: The symbol of the element from the periodic table (lower-case)
	 * Z: The metallicity by mass of this element at all previous timesteps
	 * Zin: The metallicity by mass of the infall rate at all timesteps
	 * primordial: The primordial abundance by mass due to big bang
	 * 		nucleosynthesis
	 * unretained: Unretained mass in the outflow at the current timestep.
	 * mass: The total mass in Msun of the element in the ISM
	 * solar: The abundance by mass of this element in the sun
	 */

	AGB_YIELD_GRID *agb_grid;
	CCSNE_YIELD_SPECS *ccsne_yields;
	SNEIA_YIELD_SPECS *sneia_yields;
	CHANNEL **channels;
	unsigned short n_channels;
	char *symbol;
	double *Z;
	double *Zin;
	double primordial;
	double unretained;
	double mass;
	double solar;

} ELEMENT;


typedef struct interstellar_medium {

	/*
	 * This struct contains user-specified information on the time-evolution of
	 * the interstellar medium (ISM) in their model galaxy.
	 *
	 * mode: A string denoting the meaning of the specified functions. Either
	 * 		"ifr" for infall rate, "gas" for gas supply, or "sfr" for star
	 * 		formation rate.
	 * specified: either the starformation history, infall history, or gas mass
	 * 		history of the ISM, depending on the mode that the singlezone object
	 * 		is running in.
	 * mass: The total mass in Msun of the ISM gas at the current timestep
	 * star_formation_rate: The star formation rate in Msun/Gyr.
	 * infall_rate: The infall rate of intergalactic gas into the ISM in
	 * Msun/Gyr.
	 * star_formation_history: The star formation rate in Msun/Gyr at all
	 * 		previous timesteps.
	 * eta: The mass loading factor at all previous timesteps.
	 * enh: The outflow enhancement factor at all previous timesteps.
	 * tau_star: The timescale relating the gas supply to the star formation
	 * 		rate at all timesteps.
	 * schmidt_index: The power law index on Kennicutt-Schmidt Law driven star
	 * 		formation efficiency, if applicable.
	 * mgschmidt: The normalization of the Kennicutt-Schmidt Law, if applicable
	 * smoothing_time: The outflow smoothing time
	 * schmidt: A boolean int describing whether or not to adopt
	 * 		Kennicutt-Schmidt law driven star formation efficiency.
	 */

	char *mode;
	double *specified;
	double mass;
	double star_formation_rate;
	double infall_rate;
	double *star_formation_history;
	double *eta;
	double *enh;
	double *tau_star;
	CALLBACK_2ARG *functional_tau_star;
	double schmidt_index;
	double mgschmidt;
	double smoothing_time;
	int schmidt;

} ISM;


typedef struct metallicity_distribution_function {

	/*
	 * This struct contains information on the resultant stellar metallicity
	 * distribution function from a singlezone simulation. Both mdfs are
	 * dereference by element index first, then by bin number.
	 *
	 * abundance_distributions: A pointer to the value of the distribution
	 * 		function for each [X/H] abundance in each bin.
	 * ratio_distributions: A pointer to the value of the distribution function
	 * 		for each [X/Y] abundance ratio in each bin.
	 * bins: The bin edges themselves.
	 * n_bins: The number of bins. This is always one less than the number of
	 * 		elements in the bins array.
	 */

	double **abundance_distributions;
	double **ratio_distributions;
	double *bins;
	unsigned long n_bins;

} MDF;


typedef struct initial_mass_function {

	/*
	 * This struct contains information on the user's specified stellar
	 * initial mass function. This is NOT a binspace; the values of the mass
	 * distribution are determined at the masses on the grid.
	 *
	 * spec: a description of the user's IMF prescription. Either "kroupa",
	 * 		"salpeter", or "custom"
	 * m_lower: The lower mass limit on star formation
	 * m_upper: The upper mass limit on star formation
	 * mass_distribution: The un-normalized value of the IMF at stellar masses
	 * 		in steps of IMF_STEPSIZE (declared in imf.h) from m_lower to
	 *		m_upper.
	 *
	 * Notes
	 * =====
	 * This object has a trailing _ to not produce namespace errors in
	 * functions that take a keyword argument "IMF" from python. Without the
	 * trailing underscore, the type identifier gets overridden by the keyword
	 * argument, producing compiler errors.
	 */

	char *spec;
	double m_lower;
	double m_upper;
	CALLBACK_1ARG *custom_imf;

} IMF_;


typedef struct single_stellar_population {

	/*
	 * This struct contains information relevant to single stellar populations
	 * (SSPs).
	 *
	 * imf: A string denoting the stellar initial mass function
	 * recycling: The cumulative return fraction at each timestep starting at
	 * 		t = 0
	 * msmf: The main sequence mass fraction at each timestep starting at t = 0
	 * postMS: The ratio of a star's post main-sequence lifetime to its main
	 * 		sequence lifetime.
	 * m_upper: The upper mass limit on star formation in Msun
	 * m_lower: The lower mass limit on star formation in Msun
	 * R0: The instantaneous recycling rate, if applicable.
	 * continuous: A boolean int describing whether or not to adopt
	 * 		continuous recycling.
	 */

	IMF_ *imf;
	double *crf;
	double *msmf;
	double postMS;
	double R0;
	int continuous;

} SSP;


typedef struct singlezone {

	/*
	 * This struct is the core implementation of the singlezone object in
	 * VICE, as the name would suggest.
	 *
	 * name: The name of the simulation
	 * history_writer: A FILE struct for the history.out output file
	 * mdf_writer: A FILE struct for the mdf.out output file
	 * dt: The timestep size in Gyr
	 * current_time: The current time in Gyr
	 * output_times: The times in Gyr at which to write output to the
	 * 		history.out file.
	 * timestep: The timestep number. The current time is also equal to this
	 * 		times the timestep size.
	 * n_outputs: The number of times in the output_times array
	 * Z_solar: The adopted metallicity by mass of the sun
	 * n_elements: The number of elements to track
	 * verbose: boolean int describing whether or not to print the time as the
	 * 		simulation evolves
	 * elements: The yield information for each element
	 * ism: The time evolution information for the interstellar medium (ISM)
	 * mdf: The stellar metallicity distribution function (MDF) information
	 * ssp: Information relevant to single stellar populations
	 */

	char *name;
	FILE *history_writer;
	FILE *mdf_writer;
	double dt;
	double current_time;
	double *output_times;
	unsigned long timestep;
	unsigned long n_outputs;
	double Z_solar;
	unsigned int n_elements;
	unsigned short verbose;
	ELEMENT **elements;
	ISM *ism;
	MDF *mdf;
	SSP *ssp;

} SINGLEZONE;


typedef struct tracer {

	/*
	 * This struct implements the tracer particle for multizone simulations
	 *
	 * mass: The initial mass of the tracer particle in Msun
	 * zone_origin: The zone in which the particle was born
	 * zone_current: The zone in which the particle currently resides
	 * zone_history: The zone number of the tracer particle at all timesteps
	 * 		This is -1 at timesteps before the tracer particle is born
	 * timestep_origin: The timestep at which the tracer particle is born
	 *
	 * Notes
	 * =====
	 * zone_history is an array filled from user-specifications in python
	 */

	double mass;
	int *zone_history;
	unsigned int zone_origin;
	unsigned int zone_current;
	unsigned long timestep_origin;

} TRACER;


typedef struct migration {

	/*
	 * This struct encodes migration settings for multizone simulations
	 *
	 * n_zones: The number of zones in the simulation
	 * n_tracers: The number of tracer particles per zone per timestep
	 * tracer_count: The number of active tracer particles
	 * gas_migration: The migration matrix associated with the ISM gas
	 * tracers: Pointers to the tracer particles themselves
	 */

	unsigned int n_zones;
	unsigned int n_tracers;
	unsigned long tracer_count;
	double ***gas_migration;
	TRACER **tracers;
	FILE *tracers_output;

} MIGRATION;


typedef struct multizone {

	/*
	 * This struct is the core of the multizone object.
	 *
	 * name: The name of the simulation
	 * zones: The SINGLEZONE objects corresponding to the individual zones
	 * mig: The migration settings for this simulation
	 * verbose: boolean int describing whether or not to print the time as the
	 * 		simulation evolves
	 */

	char *name;
	SINGLEZONE **zones;
	MIGRATION *mig;
	unsigned short verbose;
	unsigned short simple;

} MULTIZONE;


typedef struct integral {

	/*
	 * This struct encodes information on a definite integral.
	 *
	 * func: The function to integrate
	 * a: The lower bound of integration
	 * b: The upper bound of integration
	 * tolerance: The maximum allowed numerical tolerance
	 * method: The hash-code for the method of integration
	 * Nmax: The maximum number of bins in quadrature (failsafe against
	 * 		non-convergent solutions)
	 * Nmin: The minimum number of bins in quadrature
	 * results: The numerically computed value of the integral, it's
	 * 		approximate numerical errors and the number of bins in quadrature
	 * 		at the time of convergence.
	 */

	double (*func)(double);
	double a;
	double b;
	double tolerance;
	unsigned long method;
	unsigned long Nmax;
	unsigned long Nmin;
	unsigned long iters;
	double result;
	double error;

} INTEGRAL;


typedef struct fromfile {

	/*
	 * This struct holds data from a square ascii output file, which is the
	 * format that VICE output is stored.
	 *
	 * name: The name of the file
	 * labels: The column labels to key on from python via the VICE dataframe
	 * n_rows: The number of lines of data in the file
	 * n_cols: The dimensionality of the data
	 * data: The data itself
	 */

	char *name;
	char **labels;
	unsigned long n_rows;
	unsigned int n_cols;
	double **data;

} FROMFILE;


typedef struct hydrodiskstars {

	/*
	 * This struct holds data from star particles in a hydrodynamical
	 * simulation for construction of migration schemes.
	 *
	 * n_stars: the number of star particles in the data
	 * ids: The ID of each star particle
	 * birth_times: The times in Gyr at which each star particle was born
	 * birth_radii: The radii in kpc at which each star particle was born
	 * final_radii: The radii in kpc at which each star particle was located
	 * 		at the end of the simulation.
	 * zform: The height above/below disk midplane in kpc at formation
	 * zfinal: The final height above/below disk midplane in kpc
	 * v_rad: Radial velocity in km/s
	 * v_phi: Circular velocity in km/s
	 * v_z: Vertical velocity in km/s
	 * rad_bins: The radial bins in kpc which discretize the disk
	 * decomp: An integer index assigning star particles to thin/thick disk,
	 * 		bulge, or pseudobulge
	 * n_rad_bins: The number of radial bins
	 * mode: The mode of stellar migration
	 */

	unsigned long n_stars;
	unsigned long *ids;
	double *birth_times;
	double *birth_radii;
	double *final_radii;
	double *zform;
	double *zfinal;
	double *v_rad;
	double *v_phi;
	double *v_z;
	double *rad_bins;
	unsigned short *decomp;
	unsigned short n_rad_bins;
	char *mode;

} HYDRODISKSTARS;


#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* OBJECTS_OBJECTS_H */

