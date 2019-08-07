
#ifndef STATS_H 
#define STATS_H 

#ifdef __cplusplus 
extern "C" {
#endif /* __cplusplus */ 

#ifndef PI 
#define PI 3.14159265358979 
#endif /* PI */ 

/* 
 * Generate a pseudo-random number from a normal distribution. This function 
 * makes use of the Box-Muller tranformation to do so. 
 * 
 * Parameters 
 * ========== 
 * mean: 		The mean of the distribution 
 * sigma: 		The standard deviation of the distribution 
 * 
 * Returns 
 * ======= 
 * A psuedo-random number drawn from a guassian distribution with specified mean 
 * and standard deviation. 
 * 
 * source: stats.c 
 */ 
extern double normal(double mean, double sigma); 

#ifdef __cplusplus 
} 
#endif /* __cplusplus */ 

#endif /* STATS_H */ 



