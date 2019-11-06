
FIGURES = Fig1.pdf Fig2.pdf Fig3.pdf Fig4.pdf Fig5.pdf Fig6.pdf Fig7.pdf \
	Fig8.pdf Fig9.pdf Fig10.pdf Fig11.pdf 
TIMESTEP = 0.001

all: simulations $(FIGURES) 
.PHONY: simulations clean 

$(FIGURES): plots/*.py 
	$(MAKE) -C plots/ 
	mv plots/plots/fiducial_bursts.pdf ./Fig1.pdf 
	mv plots/plots/smoothing_time.pdf ./Fig2.pdf 
	mv plots/plots/schmidt_smoothing.pdf ./Fig3.pdf 
	mv plots/plots/sr_cc_yields.pdf ./Fig4.pdf 
	mv plots/plots/sr_yields_ssp.pdf ./Fig5.pdf 
	mv plots/plots/sr_yield_assumptions.pdf ./Fig6.pdf 
	mv plots/plots/fiducial_bursts_sr.pdf ./Fig7.pdf 
	mv plots/plots/sro_bursts.pdf ./Fig8.pdf 
	mv plots/plots/oscil.pdf ./Fig9.pdf 
	mv plots/plots/oscillations_v_time.pdf ./Fig10.pdf 
	mv plots/plots/slow_bursts.pdf ./Fig11.pdf 

simulations: simulations/simulations.py 
	python $< $(TIMESTEP)

clean: 
	$(MAKE) -C simulations/ clean 
	$(MAKE) -C plots/ clean 
	rm -f *.pdf 

