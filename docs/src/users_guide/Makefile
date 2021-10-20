
all: pkgcontents
.PHONY: pkgcontents clean

pkgcontents:
	@ $(MAKE) -C pkgcontents

clean:
	@ echo Cleaning docs/src/users_guide/
	@ rm -rf __pycache__
	@ $(MAKE) -C pkgcontents/ clean
