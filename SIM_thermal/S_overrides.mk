GUNNSDRAWINGS := \
 network/Network.xml
GUNNSDRAW_HEADERS := $(subst .xml,.hh,$(GUNNSDRAWINGS))
S_define: $(GUNNSDRAW_HEADERS)
$(GUNNSDRAW_HEADERS) : %.hh : %.xml
	@ echo $(shell python $(GUNNS_HOME)/draw/netexport.py $<)
export TRICK_GTE_EXT = GUNNS_HOME
