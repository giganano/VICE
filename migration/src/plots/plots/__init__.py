
__modules__ = ["amr", "h277"] 
__files__ = ["age_ofe", "eta", "evol", "ia_rate", "mdf_3panel", 
	"metallicity_gradient", "migration", "ofe_feh_densitymap", "ofe_mdfs", 
	"sfe", "surface_density_gradient", "tau_sfh", "tracks"] 
__all__ = __modules__ + __files__ 

for i in __modules__: exec("from . import %s" % (i)) 
for i in __files__: exec("from .%s import main as %s" % (i, i)) 

