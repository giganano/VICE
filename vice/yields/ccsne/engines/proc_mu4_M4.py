
import numpy as np

data = np.genfromtxt('pre_sn.dat',
						skip_header=1, names=True)
M_ZAMS = data['M_ZAMSM_sun']
M4s = data['M_s4M_sun']
mu4s = data['mu_4']

with open('mu4_M4.dat', 'w') as f:
	header = '# Values from Sukhbold et al. 2016 \n# M_ZAMS (Msun) \t M4 (Msun) \t mu4 \n'
	f.write(header)
	for i in range(len(M_ZAMS)):
		f.write('%2.2f \t %1.5e \t % 1.5e \n' % (M_ZAMS[i], M4s[i], mu4s[i]))
	f.close()