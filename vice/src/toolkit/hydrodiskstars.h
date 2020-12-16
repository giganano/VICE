
#ifndef TOOLKIT_HYDRODISKSTARS_H 
#define TOOLKIT_HYDRODISKSTARS_H 

#ifdef __cplusplus 
extern "C" { 
#endif /* __cplusplus */ 

/* 
 * Maximum allowed difference in birth radii between a stellar population and 
 * its analog star particle in kpc for initial analog search. 
 */ 
#ifndef INITIAL_ANALOG_SEARCH_RADIUS 
#define INITIAL_ANALOG_SEARCH_RADIUS 0.250 
#endif /* INITIAL_ANALOG_SEARCH_RADIUS */ 

/* 
 * Maximum allowed difference in birth times between a stellar population and 
 * its analog star particle in Gyr for initial analog search. 
 */ 
#ifndef INITIAL_ANALOG_SEARCH_TIME 
#define INITIAL_ANALOG_SEARCH_TIME 0.300 
#endif /* INITIAL_ANALOG_SEARCH_TIME */ 

/* 
 * The distance in kpc to increment the difference in birth radii until an 
 * analog is found. This is relevant for widened searches of candidate 
 * analogs. 
 */ 
#ifndef INCREMENT_ANALOG_SEARCH_RADIUS 
#define INCREMENT_ANALOG_SEARCH_RADIUS 0.250 
#endif 

/* 
 * The amount of time in Gyr to increment the difference in birth times until 
 * an analog is found. This is relevant for widened searches of candidate 
 * analogs.
 */ 
#ifndef INCREMENT_ANALOG_SEARCH_TIME 
#define INCREMENT_ANALOG_SEARCH_TIME 0.300 
#endif 

/* 
 * Maximum allowed difference in birth times between a stellar population and 
 * its analog star particle in Gyr for widened analog search. 
 * 
 * Note: widened search only runs if initial search finds no candidates 
 */ 
// #ifndef WIDENED_ANALOG_SEARCH_TIME 
// #define WIDENED_ANALOG_SEARCH_TIME 0.600 
// #endif /* WIDENED_ANALOG_SEARCH_TIME */ 

/* 
 * Maximum allowed difference in birth radii between a stellar population and 
 * its analog star particle in kpc for widened analog search. 
 * 
 * Note: widened search only runs if initial search finds no candidates 
 */ 
// #ifndef WIDENED_ANALOG_SEARCH_RADIUS 
// #define WIDENED_ANALOG_SEARCH_RADIUS 0.500 
// #endif /* WIDENED_ANALOG_SEARCH_TIME */ 

/* 
 * The span of ages in Gyr of each star particle in the hydrodynamical 
 * simulationdata. 
 */ 
#ifndef HYDRODISK_END_TIME 
#define HYDRODISK_END_TIME 12.2 
#endif /* HYDRODISK_END_TIME */ 

#include "../objects.h" 

/* 
 * Read the raw data describing hydrodynamical simulation star particles into 
 * the hydrodiskstars object. 
 * 
 * Parameters 
 * ==========
 * hds: 				A pointer to the hydrodiskstars object to import into 
 * Nstars: 				The number of star particles necessary for the model 
 * filestem: 			The path to the files to import, minus the "_subN.dat" 
 * ids_column: 			The column of star particle IDs 
 * birth_times_column: 	The column of times in Gyr each star particle was born 
 * birth_radii_column: 	The column of radii in kpc each star particle was born at 
 * final_radii_column: 	The column of radii in kpc each star particle ends at 
 * zform_column: 		The column of disk heights of formation in kpc 
 * zfinal_column: 		The column of present day disk heights in kpc 
 * v_radcolumn: 		The column of radial velocities in km/sec 
 * v_phicolumn: 		The column of azimuthal velocities in km/sec 
 * v_zcolumn: 			The column of vertical velocities in km/sec 
 * 
 * Returns 
 * =======
 * 1 on success, 0 on failure 
 * 
 * source: hydrodiskstars.c 
 */ 
extern unsigned short hydrodiskstars_import(HYDRODISKSTARS *hds, 
	unsigned long Nstars, char *filestem, unsigned short ids_column, 
	unsigned short birth_times_column, unsigned short birth_radii_column, 
	unsigned short final_radii_column, unsigned short zform_column, 
	unsigned short zfinal_column, unsigned short v_radcolumn, 
	unsigned short v_phicolumn, unsigned short v_zcolumn, 
	unsigned short decomp_column); 

/* 
 * Find an analog star particle from the hydrodynamical simulation given a 
 * birth radius and time of a stellar population in a multizone simulation. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing the star particle data 
 * birth_radius: 	The radius of birth in kpc 
 * birth_time: 		The time of birth in Gyr 
 * 
 * Returns 
 * =======
 * The index of the star particle in the hydrodiskstars data. 
 * 
 * Notes
 * =====
 * This function first searches for star particles born with R +/- 250 pc and 
 * T +/- 300 Myr. If no candidate analog is found, it widens it to R +/- 500 pc 
 * and T +/- 600 Myr. It continues this process of widening the search by 
 * dR = 250 pc and dT = 300 Myr until an analog is found. 
 * 
 * source: hydrodiskstars.c 
 */ 
extern long hydrodiskstars_find_analog(HYDRODISKSTARS hds, double birth_radius, 
	double birth_time); 

/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the linear migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * birth_time: 		The time the stellar population was born in Gyr 
 * birth_radius: 	The radius of the stellar population's birth in kpc 
 * end_time: 		The time of the end of the simulation (should always be 
 * 						12.2 for consistency w/hydrosim) 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The zone number of the stellar population at the intermediate time. 
 * 
 * Note 
 * ====
 * Stars which find no analog are assumed to not migrate. 
 * 
 * source: hydrodiskstars.c 
 */ 
extern long calczone_linear(HYDRODISKSTARS hds, double birth_time, 
	double birth_radius, double end_time, long analog_idx, double time); 

/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the sudden migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * migration_time: 	The time at which the star particle migrates 
 * birth_radius: 	The radius of the stellar population's birth 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The zone number of the stellar population at the intermediate time. 
 * 
 * Note 
 * ==== 
 * Stars which find no analog are assumed to not migrate. 
 * 
 * source: hydrodiskstars.c 
 */ 
extern long calczone_sudden(HYDRODISKSTARS hds, double migration_time, 
	double birth_radius, long analog_idx, double time); 

/* 
 * Determine the zone number of a stellar population at intermediate times 
 * under the diffusive migration assumption. 
 * 
 * Parameters 
 * ==========
 * hds: 			The hydrodiskstars object containing star particle data 
 * birth_time: 		The time the stellar population was born in Gyr 
 * birth_radius: 	The radius of the stellar population's birth in kpc 
 * end_time: 		The time of the end of the simulation (should always be 
 * 						12.2 for consistency w/hydrosim) 
 * analog_idx: 		The index of the analog star particle 
 * 						-1 if no analog is found 
 * time: 			The intermediate time in Gyr 
 * 
 * Returns 
 * =======
 * The zone number of the stellar population at the intermediate time. 
 * 
 * Note 
 * ====
 * Stars which find no analog are assumed to not migrate. 
 * 
 * source: hydrodiskstars.c 
 */ 
extern long calczone_diffusive(HYDRODISKSTARS hds, double birth_time, 
	double birth_radius, double end_time, long analog_idx, double time); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* TOOLKIT_HYDRODISKSTARS_H */ 
