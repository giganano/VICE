
all: timer.pdf 
.PHONY: timer.pdf clean 

timer.pdf: mpl.timer.py 
	@ echo Timing with N = 5 elements 
	# @ python timer.py 5 
	@ echo Timing with N = 10 elements 
	# @ python timer.py 10 
	@ echo Timing with N = 15 elements 
	# @ python timer.py 15 
	@ echo Timing with N = 20 elements 
	# @ python timer.py 20 
	@ echo Timing with N = 25 elements 
	# @ python timer.py 25 
	@ echo Producing figure 
	# @ python $< 
	@ echo Finished 

clean: 
	@ echo Cleaning docs/src/timer/ 
	@ # @ rm -rf *.vice/ 
	@ rm -f *.pdf 
	@ rm -f *.png 
