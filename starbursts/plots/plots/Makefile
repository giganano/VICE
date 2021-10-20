
all: fiducial_bursts.pdf smoothing_time.pdf schmidt_smoothing.pdf \
	sr_cc_yields.pdf sr_yields_ssp.pdf sr_yield_assumptions.pdf \
	fiducial_bursts_sr.pdf sro_bursts.pdf oscil.pdf oscillations_v_time.pdf \
	slow_bursts.pdf kirby2010.pdf

.PHONY: clean

%.pdf: ../mpl.%.py
	@ echo Producing figure: $@
	@ python $< $@

clean:
	@ echo Cleaning starbursts/plots/plots/
	@ rm -f *.pdf

