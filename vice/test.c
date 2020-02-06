
#include <stdlib.h> 
#include <stdio.h> 
#include "src/modeling/likelihood/linalg.h" 

int main(void) {

	unsigned short i, j; 
	double **test = (double **) malloc (3 * sizeof(double *)); 
	for (i = 0ul; i < 3; i++) {
		test[i] = (double *) malloc (3 * sizeof(double)); 
		for (j = 0ul; j < 3; j++) {
			test[i][j] = i + j; 
		} 
	} 
	for (i = 0ul; i < 3; i++) {
		for (j = 0ul; j < 3; j++) {
			printf("%.1f\t", test[i][j]); 
		} 
		printf("\n"); 
	} 

	printf("Determinant = %lf\n", determinant(test, 3)); 
	free(test); 

} 

