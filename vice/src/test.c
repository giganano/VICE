
#include <stdlib.h> 
#include <stdio.h> 
#include "imf.h" 

int main(void) {

	printf("Setting up custom IMF....\n"); 
	IMF *custom = imf_initialize("custom", 0.05, 100); 
	imf_add_mass_bin(custom); 
	imf_add_mass_bin(custom); 
	custom -> mass_bins[1] = 1; 
	custom -> mass_bins[2] = 10; 
	custom -> power_law_indeces[0] = 0; 
	custom -> power_law_indeces[1] = 1; 
	custom -> power_law_indeces[2] = 5; 

	double m = 0.1; 
	while (m < 100) {
		printf("Custom(%.1f) = %.5f\n", m, imf_evaluate(custom, m)); 
		m += 0.1; 
	} 

	printf("Freeing up custom IMF....\n"); 
	imf_free(custom); 
	printf("Finished!\n"); 
	return 0; 

}



