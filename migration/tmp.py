
import src 
import os 

# src.plots.h277.decomposition("./figures/h277/decomposition") 
# src.plots.migration("./figures/migration") 
# src.plots.eta_tau_sfh("./figures/eta_tau_sfh") 

# src.plots.evol(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/evol") 

# src.plots.sfe(["./outputs/high-resolution/2Gyr_timedep/diffusion/insideout"], 
# 	"./figures/sfe", labels = None) 

# src.plots.surface_density_gradient(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/surface_density_gradient") 

# src.plots.ofe_feh_densitymap(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./figures/ofe_feh_densitymap") 

# src.plots.tracks(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./figures/tracks") 

# src.plots.metallicity_gradient(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/metallicity_gradients") 

# src.plots.mdf_3panel("Fe", 
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst"], 
# 	"./figures/mdf_3panel_fe", labels = ["Late-Burst"], apogee = True) 

# src.plots.mdf_3panel("O", 
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst"], 
# 	"./figures/mdf_3panel_o", labels = ["Late-Burst"], apogee = True) 

# src.plots.ofe_mdfs(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/ofe_mdfs/2Gyr_timedep/diffusion/insideout") 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/sudden/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/linear/insideout", 
# 	"./figures/age_ofe_migration_comparison", 
# 	names = [["Post-Process", "Diffusion"], ["Sudden", "Linear"]]) 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/age_ofe_sfh_comparison") 

# src.plots.amr.galactic_regions("O", "Fe", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/age_alpha_regions") 

# src.plots.amr.comparison("O", 
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/static"], 
# 	"./figures/amr/regions/2Gyr_timedep/diffusion/static_o", 
# 	feuillet2019 = False, legend = False, radii = [[7, 9], [11, 13]], 
# 	labels = None, 
# 	left = 0.15, right = 0.85, bottom = 0.18) 

src.plots.amr.comparison("O", 
	["./outputs/high-resolution/no_outer_disk/diffusion/static"], 
	"./figures/amr/regions/2Gyr_timedep/diffusion/static_o_no_outer_disk", 
	feuillet2019 = False, legend = False, labels = None) 

# src.plots.amr.solar_annulus(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/amr_solar_annulus") 

# src.plots.amr.solar_annulus(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/test") 

# src.plots.amr.comparison("Fe", 
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst"], 
# 	"./figures/amr/2Gyr_timedep/diffusion/insideout_vs_lateburst_fe", 
# 	labels = ["Inside-Out", "Late-Burst"]) 


###########################################################


# def transfer(infile): 
# 	print(infile) 
# 	os.system("cp %s %s_orig.%s" % (infile, infile.split('.')[0], 
# 		infile.split('.')[1])) 
# 	with open(infile, 'r') as in_: 
# 		with open("tmp.out", 'w') as out: 
# 			out.write("# zone_origin\ttime_origin\tanalog_id\tzfinal\n") 
# 			while True: 
# 				line = in_.readline() 
# 				if line == "": break 
# 				if line[0] == '#': continue 
# 				line = [float(_) for _ in line.split()] 
# 				if line[-1] == 100: 
# 					line[2] = -1 
# 					line[3] = 0 
# 				out.write("%d\t%.2f\t%d\t%.2f\n" % (line[0], line[1], line[2], 
# 					line[3])) 
# 			out.close() 
# 		in_.close() 
# 	os.system("mv tmp.out %s" % (infile)) 


# for i in ["static", "insideout", "lateburst", "outerburst"]: 
# 	transfer(
# 		"outputs/high-resolution/2Gyr_timedep/diffusion/%s_analogdata.out" % (
# 			i)) 
# for i in ["linear", "sudden", "post-process"]: 
# 	transfer(
# 		"outputs/high-resolution/2Gyr_timedep/%s/insideout_analogdata.out" % (
# 			i)) 


###########################################################

