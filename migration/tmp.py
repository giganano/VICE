
import src 
suite = src.simulations.suite(
	tau_star_mol = src.simulations.sfe(baseline = 1, index = 0) 
) 
for i in ["diffusion", "linear", "post-process", "sudden"]: 
# for i in ["post-process"]: 
	# for j in ["static", "insideout", "lateburst"]: 
	for j in ["lateburst"]: 
		kwargs = dict(
			name = "outputs/low-resolution/1Gyr/%s/%s" % (i, j), 
			spec = j 
		) 
		if i == "post-process": 
			kwargs["simple"] = True 
		else: 
			kwargs["migration_mode"] = i 
		# suite.simulations.append(src.simulations.diskmodel(**kwargs)) 
		suite.simulations.append(src.simulations.diskmodel.from_config(
			suite.config, **kwargs)) 

if __name__ == "__main__": 
	suite.run(overwrite = True) 
	# print(len(suite.simulations)) 

