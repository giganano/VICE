
import src 

# src.plots.ia_rate( 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	"./figures/ia_rate/insideout_diffusion_vs_postprocess_2Gyr_timedep") 

# element_x = "Fe" 
# element_y = "H" 
# sfe = ["2Gyr_timedep"] 
# migration = ["diffusion"] 
# evol = ["static", "insideout", "lateburst", "outerburst"] 
# for i in sfe: 
# 	for j in migration: 
# 		for k in evol: 
# 			if element_y.lower() == 'h': 
# 				stem = "./figures/amr/%s/%s/%s_%s" % (i, j, k, element_x) 
# 			else: 
# 				stem = "./figures/amr/%s/%s/%s_%s_%s" % (i, j, k, element_x, 
# 					element_y) 
# 			print(stem) 
# 			src.plots.amr.galactic_regions(element_x, element_y, 
# 				"./outputs/high-resolution/%s/%s/%s" % (i, j, k), 
# 				stem) 

# src.plots.evol(
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/static", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/evol/Sigma_gCrit_1e8/2Gyr_timedep/diffusion") 

src.plots.sfe(
	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/static", 
	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/insideout", 
	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/lateburst", 
	"./outputs/low-resolution/Sigma_gCrit_1e8/2Gyr_timedep/diffusion/outerburst", 
	"./figures/sfe/Sigma_gCrit_1e8/2Gyr_timedep/diffusion") 

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

# src.plots.mdf_3panel("Fe", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./figures/mdf_3panel/2Gyr_timedep/diffusion/lateburst") 

# src.plots.tracks.single_panel(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/post-process/insideout", 
# 	[2, 4, 6, 8, 10, 12.8], 
# 	"./figures/tracks/single_panel/diffusion_2Gyr_timedep") 

# src.plots.evol(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/evol/2Gyr_timedep/diffusion") 

# src.plots.sfe(
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/static", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/insideout", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/lateburst", 
# 	"./outputs/high-resolution/2Gyr_timedep/diffusion/outerburst", 
# 	"./figures/sfe/2Gyr_timedep/diffusion") 

# src.plots.eta("./figures/eta") 

# src.plots.amr.galactic_regions("O", "Fe", 
# 	"./outputs/low-resolution/2Gyr/diffusion/insideout", 
# 	"./figures/amr/2Gyr/diffusion/test") 

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

