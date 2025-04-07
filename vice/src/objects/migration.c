/*
 * This file implements memory management for the migration object.
 */

#include <stdlib.h>
#include "../migration.h"
#include "objects.h"
#include "callback_current_state.h"
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
	mig -> callback_gas_migration = 0u;
	mig -> n_zones = n;
	mig -> n_tracers = 0u;
	mig -> tracer_count = 0ul;
	mig -> gas_migration = NULL;
	mig -> tracers = NULL;
	mig -> tracers_output = NULL;
	mig -> callback_objects = (CALLBACK_CURRENT_STATE ***) malloc (
		(*mig).n_zones * sizeof(CALLBACK_CURRENT_STATE **));
	for (unsigned int i = 0u; i < (*mig).n_zones; i++) {
		mig -> callback_objects[i] = (CALLBACK_CURRENT_STATE **) malloc (
			(*mig).n_zones * sizeof(CALLBACK_CURRENT_STATE *));
		for (unsigned int j = 0u; j < (*mig).n_zones; j++) {
			mig -> callback_objects[i][j] = callback_current_state_initialize();
		}
	}
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

		if ((*mig).callback_objects != NULL) {
			for (unsigned int i = 0u; i < (*mig).n_zones; i++) {
				for (unsigned int j = 0u; j < (*mig).n_zones; j++) {
					if ((*mig).callback_objects[i] != NULL) {
						callback_current_state_free(
							mig -> callback_objects[i][j]);
					} else {}
				}
			}
			free(mig -> callback_objects);
			mig -> callback_objects = NULL;
		} else {}

		free(mig);
		mig = NULL;

	} else {}

}

