
#ifndef MIGRATION_H
#define MIGRATION_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/*
 * ij'th element represents likelihood gas or particle will migrate in a 10 Myr
 * time interval
 */
#ifndef NORMALIZATION_TIME_INTERVAL
#define NORMALIZATION_TIME_INTERVAL 0.01
#endif /* NORMALIZATOIN_TIME_INTERVAL */

#include "objects.h"
#include "multizone/migration.h"
#include "objects/migration.h"

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* MIGRATION_H */

