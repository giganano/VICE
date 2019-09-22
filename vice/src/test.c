
#include <stdlib.h> 
#include <stdio.h> 
#include <math.h> 
#include <time.h> 
#include "imf.h" 

static double custom_IMF(double m) {

	if (!m) {
		return 0; 
	} else if (m > 1) {
		return pow(m, -5.3); 
	} else {
		return pow(m, 0); 
	}

}

// int main(void) {

// 	time_t start = time(NULL); 
// 	printf("Setting up Kroupa IMF....\n"); 
// 	IMF *kroupa = imf_initialize("kroupa", 0.08, 100); 

// 	double m = 0.01; 
// 	while (m <= 10) {
// 		printf("kroupa(%.2f) = %g\n", m, imf_evaluate(*kroupa, m)); 
// 		m += 0.01; 
// 	} 

// 	printf("Freeing up Kroupa IMF....\n"); 
// 	free(kroupa); 
// 	printf("Finished!\n"); 
// 	time_t stop = time(NULL); 
// 	printf("%g seconds\n", difftime(stop, start)); 
// 	return 0; 

// }

int main(void) {

	time_t start = time(NULL); 
	printf("Setting up custom IMF....\n"); 
	IMF *custom = imf_initialize("custom", 0.08, 100); 

	double *mass_dist = (double *) malloc (
		n_mass_bins(*custom) * sizeof(double)); 
	unsigned long i; 
	for (i = 1l; i < n_mass_bins(*custom); i++) { 
		mass_dist[i] = custom_IMF(IMF_STEPSIZE * i); 
		// mass_dist[i] = kroupa01(IMF_STEPSIZE * i); 
	} 
	imf_set_mass_distribution(custom, mass_dist); 
	free(mass_dist); 

	double m = 0.01; 
	while (m <= 10) {
		printf("custom(%.2f) = %g\n", m, imf_evaluate(*custom, m)); 
		m += 0.01; 
	} 

	printf("Freeing up custom IMF....\n"); 
	free(custom); 
	printf("Finished!\n"); 
	time_t stop = time(NULL); 
	printf("%ld seconds\n", stop - start); 
	return 0; 

}


