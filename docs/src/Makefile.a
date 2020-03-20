
all: users_guide science_documentation 
.PHONY: users_guide science_documentation rh_2panel timer clean 

users_guide: 
	@ $(MAKE) -C users_guide 

science_documentation: 
	@ $(MAKE) -C science_documentation 

rh_2panel: 
	@ $(MAKE) -C rh_2panel 

timer: 
	@ $(MAKE) -C timer 

clean: 
	@ echo Cleaning docs/src/ 
	@ $(MAKE) -C users_guide/ clean 
	@ $(MAKE) -C science_documentation/ clean 

