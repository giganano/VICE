# Running this file will produce the wheel and source archive in the current 
# python environment 

make 
python setup.py build_ext -j 12 --inplace 
python setup.py sdist bdist_wheel 
make clean 
