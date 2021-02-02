
import src 
import os 

# src.plots.h277.decomposition("./figures/h277/decomposition") 
# src.plots.h277.decomposition("./figures/h277/decomposition_young") 
# src.plots.migration("./figures/migration") 
# src.plots.eta_tau_sfh("./figures/eta_tau_sfh") 
# src.plots.evol(
# 	"./outputs/high-resolution/diffusion/static", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst", 
# 	"./outputs/high-resolution/diffusion/outerburst", 
# 	"./figures/evol") 

# src.plots.surface_density_gradient(
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./figures/surface_density_gradient") 

# src.plots.sfe(["./outputs/high-resolution/diffusion/insideout"], 
# 	"./figures/sfe", labels = None) 
# src.plots.sfe(
# 	["./outputs/alt_mstar/diffusion/insideout"], 
# 	"./figures/sfe_alt_mstar", labels = None) 

# src.plots.ofe_feh_densitymap(
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/post-process/insideout", 
# 	"./figures/ofe_feh_densitymap") 
# src.plots.ofe_feh_densitymap(
# 	"./outputs/alt_mstar/diffusion/insideout", 
# 	"./outputs/alt_mstar/post-process/insideout", 
# 	"./figures/ofe_feh_densitymap_alt_mstar") 

# src.plots.tracks(
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/post-process/insideout", 
# 	"./figures/tracks") 

# src.plots.metallicity_gradient(
# 	"./outputs/high-resolution/diffusion/static", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst", 
# 	"./outputs/high-resolution/diffusion/outerburst", 
# 	"./figures/metallicity_gradient") 

# src.plots.mdf_3panel("Fe", 
# 	["./outputs/high-resolution/diffusion/insideout"], 
# 	"./figures/mdf_3panel_fe", labels = ["Inside-Out"], apogee = True) 
# src.plots.mdf_3panel("Fe", 
# 	["./outputs/alt_mstar/diffusion/insideout"], 
# 	"./figures/mdf_3panel_fe_alt_mstar", labels = ["Inside-Out"], apogee = True) 

# src.plots.mdf_3panel("O", 
# 	["./outputs/high-resolution/diffusion/insideout"], 
# 	"./figures/mdf_3panel_o", labels = ["Inside-Out"], apogee = True) 
# src.plots.mdf_3panel("O", 
# 	["./outputs/alt_mstar/diffusion/insideout"], 
# 	"./figures/mdf_3panel_o_alt_mstar", labels = ["Inside-Out"], apogee = True) 

# src.plots.mdf_3panel("Fe", 
# 	["./outputs/high-resolution/diffusion/static", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst", 
# 	"./outputs/high-resolution/diffusion/outerburst"], 
# 	"./figures/mdf_3panel_fe_all", 
# 	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"], 
# 	apogee = True) 

# src.plots.mdf_3panel("O", 
# 	["./outputs/high-resolution/diffusion/static", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst", 
# 	"./outputs/high-resolution/diffusion/outerburst"], 
# 	"./figures/mdf_3panel_o_all", 
# 	labels = ["Constant SFR", "Inside-Out", "Late-Burst", "Outer-Burst"], 
# 	apogee = True) 

# src.plots.ofe_mdfs(
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./figures/ofe_mdfs") 
# src.plots.ofe_mdfs(
# 	"./outputs/alt_mstar/diffusion/insideout", 
# 	"./figures/ofe_mdfs_alt_mstar") 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/post-process/insideout", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/sudden/insideout", 
# 	"./outputs/high-resolution/linear/insideout", 
# 	"./figures/age_ofe_migration_comparison", 
# 	names = [["Post-Process", "Diffusion"], ["Sudden", "Linear"]]) 

# src.plots.age_ofe(
# 	"./outputs/high-resolution/diffusion/static", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst", 
# 	"./outputs/high-resolution/diffusion/outerburst", 
# 	"./figures/age_ofe_sfh_comparison") 

# src.plots.amr.galactic_regions("O", "Fe", 
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./figures/age_alpha_regions") 

# src.plots.amr.galactic_regions("O", "Fe", 
# 	"./outputs/high-resolution/diffusion/static", 
# 	"./figures/age_alpha_regions_static") 

# src.plots.amr.comparison("O", 
# 	["./outputs/high-resolution/diffusion/static"], 
# 	"./figures/amr_static_o", 
# 	feuillet2019 = False, legend = False, radii = [[7, 9], [11, 13]], 
# 	labels = None, 
# 	left = 0.15, right = 0.85, bottom = 0.18) 

# src.plots.amr.solar_annulus(
# 	"./outputs/high-resolution/diffusion/insideout", 
# 	"./figures/amr_solar_annulus") 

# src.plots.amr.comparison("Fe", 
# 	["./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst"], 
# 	"./figures/amr_insideout_vs_lateburst_fe", 
# 	labels = ["Inside-Out", "Late-Burst"]) 
# src.plots.amr.comparison("Fe", 
# 	["./outputs/alt_mstar/diffusion/insideout", 
# 	"./outputs/alt_mstar/diffusion/lateburst"], 
# 	"./figures/amr_insideout_vs_lateburst_fe_alt_mstar", 
# 	labels = ["Inside-Out", "Late-Burst"]) 

# src.plots.amr.comparison("O", 
# 	["./outputs/high-resolution/diffusion/insideout", 
# 	"./outputs/high-resolution/diffusion/lateburst"], 
# 	"./figures/amr_insideout_vs_lateburst_o", 
# 	labels = ["Inside-Out", "Late-Burst"]) 

