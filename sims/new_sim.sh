#!/bin/bash
if [ $# -eq 0 ] ; then
    NEWSIM=SIM_new
else
    NEWSIM=SIM_$1
fi
cd /root/gunns-sims/sims
cp -r SIM_default $NEWSIM
sed -i "s/SIM_default/$NEWSIM/g" "$NEWSIM/Sim.sm"
