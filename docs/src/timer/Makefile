
all: timer.pdf 
.PHONY: timer_5.out timer_10.out timer_15.out timer_20.out timer_25.out clean 

timer.pdf: mpl.timer.py 
	@ echo Producing figure 
	@ python $< 

timer_5.out: 
	@ echo Timing with N = 5 elements 
	@ python timer.py 5 

timer_10.out: 
	@ echo Timing with N = 10 elements 
	@ python timer.py 10 

timer_15.out: 
	@ echo Timing with N = 15 elements 
	@ python timer.py 15 

timer_20.out: 
	@ echo Timing with N = 20 elements 
	@ python timer.py 20 

timer_25.out: 
	@ echo Timing with N = 25 elements 
	@ python timer.py 25 

clean: 
	@ echo Cleaning docs/src/timer/ 
	@ rm -f *.pdf 
	@ rm -f *.png 
