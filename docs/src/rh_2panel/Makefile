
all: rh_2panel.pdf
.PHONY: clean

%.pdf: mpl.%.py
	@ echo Produing rh_2panel.pdf
	@ python $<

clean:
	@ echo Cleaning docs/src/rh_2panel/
	@ rm -f *.pdf
	@ rm -f *.png

