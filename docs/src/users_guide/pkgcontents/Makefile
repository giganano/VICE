
all: pkgcontents 
.PHONY: pkgcontents clean 

pkgcontents: 
	@ echo Generating package contents documentation 
	@ python ./gen 

clean: 
	@ echo Cleaning docs/src/users_guide/pkgcontents/ 
	@ rm -rf __pycache__ 
	@ rm -f *.rst 
	@ rm -rf vice.* 
	@ $(MAKE) -C gen/ clean 

