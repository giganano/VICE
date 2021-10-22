
all: pkgcontents
.PHONY: pkgcontents clean

pkgcontents:
	@ $(MAKE) -C pkgcontents

clean:
	@ echo Cleaning docs/src/api/
	@ rm -rf __pycache__
	@ $(MAKE) -C pkgcontents/ clean
