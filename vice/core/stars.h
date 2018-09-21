
#ifndef STARS_H
#define STARS_H

extern double get_mstar(INTEGRATION run, MODEL m);

/* MDF functions. */
extern void update_MDF(INTEGRATION run, MODEL *m);
extern void normalize_MDF(INTEGRATION run, MODEL *m);
extern void setup_MDF(INTEGRATION run, MODEL *m);

/* Recycling functions. */
extern double m_turnoff(double t);
extern double m_returned(INTEGRATION run, MODEL m, int index);
extern void setup_R(MODEL *m, double *times, long num_times);
extern void setup_H(MODEL *m, double *times, long num_times);
extern void setup_breakdown(INTEGRATION run, long num_times);
extern void setup_Zall(INTEGRATION *run, long num_times);

#endif /* STARS_H */

