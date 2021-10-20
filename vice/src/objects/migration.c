/*
 * This file implements memory management for the migration object.
 */

#include <stdlib.h>
#include "../migration.h"
#include "objects.h"
#include "migration.h"


/*
 * Allocate memory for an return a pointer to a migration object.
 *
 * Parameters
 * ==========
 * n:		The number of zones in the multizone simulation
 *
 * header: migration.h
 */
extern MIGRATION *migration_initialize(unsigned int n) {

	MIGRATION *mig = (MIGRATION *) malloc (sizeof(MIGRATION));
	mig -> n_zones = n;
	mig -> n_tracers = 0u;
	mig -> tracer_count = 0ul;
	mig -> gas_migration = NULL;
	mig -> tracers = NULL;
	mig -> tracers_output = NULL;
	return mig;

}


/*
 * Free up the memory stored in a migration object.
 *
 * header: migration.h
 */
extern void migration_free(MIGRATION *mig) {

	if (mig != NULL) {

		if ((*mig).gas_migration != NULL) {
			free(mig -> gas_migration);
			mig -> gas_migration = NULL;
		} else {}

		if ((*mig).tracers != NULL) {
			unsigned long i;
			for (i = 0l; i < (*mig).tracer_count; i++) {
				if ((*mig).tracers[i] != NULL) tracer_free(mig -> tracers[i]);
			}
			free(mig -> tracers);
			mig -> tracers = NULL;
		} else {}

		if ((*mig).tracers_output != NULL) {
			fclose(mig -> tracers_output);
			mig -> tracers_output = NULL;
		} else {}

		free(mig);
		mig = NULL;

	} else {}

}

