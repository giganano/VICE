
__modules__ = ["amr"]
__files__ = ["age_ofe", "evol", "eta_tau_sfh", "h277_decomposition",
	"mdf_3panel", "metallicity_gradient", "migration", "ofe_feh_densitymap",
	"ofe_mdfs", "sfe", "surface_density_gradient", "tracks"]
__all__ = __modules__ + __files__

for i in __modules__: exec("from . import %s" % (i))
for i in __files__: exec("from .%s import main as %s" % (i, i))

