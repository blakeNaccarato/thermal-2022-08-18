GUNNSDRAWINGS := /root/thermal-2022-08-18/BasicThermal/BasicThermal.xml
GUNNSDRAW_HEADERS := $(subst .xml,.hh,$(GUNNSDRAWINGS))
S_define: $(GUNNSDRAW_HEADERS)
$(GUNNSDRAW_HEADERS) : %.hh : %.xml
	@ echo $(shell python $(GUNNS_HOME)/draw/netexport.py $<)
