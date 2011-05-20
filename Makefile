
run: membrane.so
	python duck.py 

membrane.so: cmod/membrane.pyx
	cd cmod ; $(MAKE) $(MFLAGS)

