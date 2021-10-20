
.PHONY: figures clean

all: figures

figures:
	@ $(MAKE) -C plots/

clean:
	@ echo Cleaning starbursts/plots/
	@ rm -f *.pyc
	@ $(MAKE) -C plots/ clean

