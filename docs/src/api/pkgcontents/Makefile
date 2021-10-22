
all: pkgcontents
.PHONY: pkgcontents clean

pkgcontents:
	@ echo Generating package contents documentation
	@ python3 ./gen

clean:
	@ echo Cleaning docs/src/api/pkgcontents/
	@ rm -rf __pycache__
	@ rm -f *.rst
	@ rm -rf vice.*
	@ $(MAKE) -C gen/ clean

