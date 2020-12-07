
import src 

# src.plots.migration("./figures/migration") 
# src.plots.eta_tau_sfh("./figures/eta_tau_sfh") 
# src.plots.tau_sfh("./figures/tau_sfh") 
# src.plots.h277.birth_final_radii_pdfs("./figures/h277/birth_final_radii_pdfs") 
# src.plots.h277.decomposition("./figures/h277/decomposition") 
# src.plots.ofe_feh_densitymap(
# 	["./outputs/low-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/outerburst"], 
# 	"./figures/ofe_feh_densitymaps/test", 
# 	colormaps = ["black", "red", "blue"], 
# 	which = ["scatter", "scatter", "scatter"])  
# src.plots.ofe_feh_densitymap(
# 	# ["./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst"], 
# 	"./figures/ofe_feh_densitymaps/2Gyr_timedep/diffusion", 
# 	which = ["contour", "contour"], 
# 	colormaps = ["Reds", "Blues"]) 
# for i in ["insideout", "lateburst", "outerburst"]: 
# 	output_path = "./outputs/low-resolution/2Gyr_timedep/diffusion/" 
# 	figure_path = "./figures/ofe_feh_densitymaps/2Gyr_timedep/diffusion/" 
# 	print(i) 
# 	src.plots.ofe_feh_densitymap(
# 		["%s%s" % (output_path, i)], 
# 		"%s%s" % (figure_path, i), 
# 		colormaps = ["Greys"]) 
for i in ["insideout", "lateburst", "outerburst", "static"]: 
	print(i) 
	src.plots.ofe_mdfs(
		"./outputs/high-resolution/2Gyr_timedep/diffusion/%s" % (i), 
		"./figures/ofe_mdfs/2Gyr_timedep/diffusion/%s" % (i)) 

# src.plots.ofe_feh_densitymap(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./figures/ofe_feh_densitymaps/test") 
# for i in ["insideout", "static", "lateburst", "outerburst"]: 
# 	print(i) 
# 	src.plots.ofe_mdfs(
# 		"./outputs/high-resolution/fiducial/2Gyr_timedep/diffusion/%s" % (i), 
# 		"./figures/ofe_mdfs/fiducial/%s" % (i)) 

# labels = {
# 	"insideout": 	"Inside-Out", 
# 	"lateburst": 	"Late-Burst", 
# 	"outerburst": 	"Outer-Burst" 
# }
# output_path = "./outputs/high-resolution/strong_mass_loading/2Gyr_timedep/" 
# output_path += "diffusion/" 
# figure_path = "./figures/mdf_3panel/strong_mass_loading/2Gyr_timedep/diffusion/" 
# for elem in ["Fe", "O"]: 
# 	print(elem) 
# 	for evol in ["insideout", "lateburst", "outerburst"]: 
# 		print(evol) 
# 		src.plots.mdf_3panel(elem, ["%s%s" % (output_path, evol)], 
# 			"%s%s_%s" % (figure_path, evol, elem), 
# 			labels = [labels[evol]], apogee = True) 

# elem = "Fe" 
# src.plots.mdf_3panel(elem, 
# 	["./outputs/low-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/lateburst"], 
# 	"./figures/mdf_3panel/test_%s" % (elem), 
# 	labels = ["Inside-Out", "Late-Burst"], apogee = True) 

# src.plots.tracks(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	[2, 4, 6, 8, 10, 12.8], 
# 	"./figures/tracks/diffusion_2Gyr_timedep") 

# for elem in ["O", "Fe"]: 
# 	src.plots.amr.comparison(elem, 
# 		"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 		"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 		"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 		"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 		"./figures/amr/2Gyr_timedep/diffusion_%s" % (elem)) 

# src.plots.metallicity_gradient( 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/low-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/metallicity_gradient/strong_mass_loading/2Gyr_timedep/diffusion") 

# src.plots.ia_rate( 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./figures/ia_rate/insideout_diffusion_vs_postprocess_2Gyr_timedep") 

# element_x = "O" 
# element_y = "Fe" 
# sfe = ["2Gyr_timedep"] 
# migration = ["diffusion"] 
# evol = ["static", "insideout", "lateburst", "outerburst"] 
# for i in sfe: 
# 	for j in migration: 
# 		for k in evol: 
			# if element_y.lower() == 'h': 
			# 	stem = "./figures/amr/strong_mass_loading/%s/%s/%s_%s" % (
			# 		i, j, k, element_x) 
			# else: 
			# 	stem = "./figures/amr/strong_mass_loading/%s/%s/%s_%s_%s" % (
			# 		i, j, k, element_x, element_y) 
			# print(stem) 
			# src.plots.amr.galactic_regions(element_x, element_y, 
			# 	"./outputs/high-resolution/strong_mass_loading/%s/%s/%s" % (
			# 		i, j, k), 
			# 	stem) 
			# fig_path = "./figures/ofe_mdfs/Sigma_gCrit_1e8/2Gyr_timedep/" 
			# fig_path += "diffusion/" 
			# out_path = "./outputs/high-resolution/Sigma_gCrit_1e8/" 
			# out_path += "2Gyr_timedep/diffusion/" 
			# print("%s%s" % (out_path, k)) 
			# print("%s%s" % (fig_path, k)) 
			# src.plots.ofe_mdfs("%s%s" % (out_path, k), 
			# 	"%s%s" % (fig_path, k)) 

# src.plots.evol(
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/static", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/evol/Sigma_gCrit_1e8/2Gyr_timedep/diffusion") 

# radii = [5, 7, 9, 11, 13] 
# heights = [0, 0.5, 1.0, 2.0] 
# for i in range(len(radii) - 1): 
# 	for j in range(len(heights) - 1): 
# 		stem = "./figures/amr/2Gyr_timedep/Rgal_%d_%d/absz_%g_%g/diffusion" % (
# 			radii[i], radii[i + 1], heights[j], heights[j + 1]) 
# 		print(stem) 
# 		src.plots.amr.model_comparison(
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 			stem, 
# 			min_rgal = radii[i], 
# 			max_rgal = radii[i + 1], 
# 			min_absz = heights[j], 
# 			max_absz = heights[j + 1]) 

# src.plots.amr(
# 	"./outputs/high-resolution/2Gyr/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr/diffusion/outerburst", 
# 	"./figures/amr/2Gyr/Rgal_9_11/absz_0_0.5/diffusion", 
# 	min_rgal = 9, max_rgal = 11, min_absz = 0, max_absz = 0.5) 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/sudden/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/linear/insideout", 
# 	"./figures/age_ofe/2Gyr_timedep/Rgal_7_9insideout", 
# 	names = [["Post-Process", "Diffusion"], ["Sudden", "Linear"]]) 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/age_ofe/2Gyr_timedep/Rgal_7_9/diffusion", 
# 	names = [["Constant SFR", "Inside-Out"], ["Late-Burst", "Outer-Burst"]]) 

# src.plots.evol(
# 	"./outputs/low-resolution/strong_mass_loading/2Gyr_timedep/diffusion/static", 
# 	"./outputs/low-resolution/strong_mass_loading/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/strong_mass_loading/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/low-resolution/strong_mass_loading/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/evol/strong_mass_loading/2Gyr_timedep/diffusion") 

# src.plots.sfe(
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst"], 
# 	"./figures/sfe/2Gyr_timedep/diffusion") 
# src.plots.sfe(
# 	["./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/insideout"], 
# 	"./figures/sfe/fordavid", 
# 	labels = [r"$\Sigma_\text{g,Crit} = 2\times10^7$ M$_\odot$ kpc$^{-2}$", 
# 		r"$\Sigma_\text{g,Crit} = 10^8$ M$_\odot$ kpc$^{-2}$"], 
# 		ylim = [0, 12], yticks = range(0, 14, 2))  

# src.plots.eta("./figures/eta") 

# src.plots.amr.galactic_regions("O", "Fe", 
# 	"./outputs/low-resolution/2Gyr/diffusion/insideout", 
# 	"./figures/amr/2Gyr/diffusion/test") 

# path = "./outputs/high-resolution/strong_mass_loading/2Gyr_timedep/diffusion" 
# src.plots.metallicity_gradient(
# 	"%s/static" % (path), 
# 	"%s/insideout" % (path), 
# 	"%s/lateburst" % (path), 
# 	"%s/outerburst" % (path), 
# 	"./figures/metallicity_gradient/strong_mass_loading/2Gyr_timedep/diffusion") 

# src.plots.metallicity_gradient( 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/metallicity_gradient/test") 

# src.plots.ofe_mdfs(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./figures/ofe_mdfs/insideout_diffusion_2Gyr_timedep") 


# src.plots.ofe_mdfs(
# 	"./outputs/high-resolution/2Gyr/diffusion/insideout", 
# 	"./figures/ofe_mdfs/2Gyr/diffusion/insideout") 

# sfe = ["1Gyr", "1Gyr_timedep", "2Gyr", "2Gyr_timedep"] 
# sfe = ["2Gyr_timedep"] 
# migration = ["diffusion", "linear", "post-process", "sudden"] 
# migration = ["post-process", "sudden"] 
# evol = ["static", "insideout", "lateburst", "outerburst"] 

# for i in sfe: 
# 	for j in migration: 
# 		for k in range(len(radii) - 1): 
# 			for l in range(len(heights) - 1): 
# 				print("./figures/amr/%s/Rgal_%d_%d/absz_%g_%g/%s" % (i, 
# 					radii[k], radii[k + 1], heights[l], heights[l + 1], j))
# 				src.plots.amr(
# 					"./outputs/high-resolution/%s/%s/static" % (i, j), 
# 					"./outputs/high-resolution/%s/%s/insideout" % (i, j), 
# 					"./outputs/high-resolution/%s/%s/lateburst" % (i, j), 
# 					"./outputs/high-resolution/%s/%s/outerburst" % (i, j), 
# 					"./figures/amr/%s/Rgal_%d_%d/absz_%g_%g/%s" % (i, 
# 						radii[k], radii[k + 1], heights[l], heights[l + 1], j), 
# 					min_rgal = radii[k], 
# 					max_rgal = radii[k + 1], 
# 					min_absz = heights[l], 
# 					max_absz = heights[l + 1]) 

# for i in range(len(radii) - 1): 
# 	for j in range(len(heights) - 1): 
# 		print("./figures/age_ofe/2Gyr_timedep/Rgal_%d_%d/absz_%g_%g/diffusion" % (
# 			radii[i], radii[i + 1], heights[j], heights[j + 1])) 
# 		src.plots.age_ofe(
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 			"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 			"./figures/age_ofe/2Gyr_timedep/Rgal_%d_%d/absz_%g_%g/diffusion" % (
# 				radii[i], radii[i + 1], heights[j], heights[j + 1]), 
# 			min_rgal = radii[i], max_rgal = radii[i + 1], 
# 			min_absz = heights[j], max_absz = heights[j + 1]) 

# for i in sfe: 
# 	for j in migration: 
# 		src.plots.metallicity_gradient(
# 			"./outputs/high-resolution/%s/%s/static" % (i, j), 
# 			"./outputs/high-resolution/%s/%s/insideout" % (i, j), 
# 			"./outputs/high-resolution/%s/%s/lateburst" % (i, j), 
# 			"./outputs/high-resolution/%s/%s/outerburst" % (i, j), 
# 			"./figures/metallicity_gradient/%s/%s" % (i, j))  
		# for k in evol: 
			# src.plots.ofe_mdfs(
			# 	"./outputs/high-resolution/%s/%s/%s" % (i, j, k), 
			# 	"./figures/ofe_mdfs/%s/%s/%s" % (i, j, k)) 

# src.plots.ofe_mdfs(
# 	"./outputs/high-resolution/2Gyr/diffusion/lateburst", 
# 	"./figures/ofe_mdfs/2Gyr_diffusion_lateburst_dashed") 

# for i in sfe: 
# 	for j in migration: 
# 			src.plots.amr(
# 				"./outputs/high-resolution/%s/%s/static" % (i, j), 
# 				"./outputs/high-resolution/%s/%s/insideout" % (i, j), 
# 				"./outputs/high-resolution/%s/%s/lateburst" % (i, j), 
# 				"./outputs/high-resolution/%s/%s/outerburst" % (i, j), 
# 				"./figures/amr/%s/%s" % (i, j)) 

# src.plots.amr("./outputs/high-resolution/2Gyr/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr/diffusion/outerburst", 
# 	"./figures/amr/2Gyr/diffusion") 

# src.plots.surface_density_gradient(
# 	"./outputs/high-resolution/2Gyr/diffusion/insideout", 
# 	"./figures/surface_density_gradient") 

