#!/bin/tcsh
if ( $1 == "" ) then
    set NEWSIM = SIM_new
else
    set NEWSIM = SIM_$1
cd /root/gunns-sims/sims
cp -r SIM_default $NEWSIM
sed -i "s/SIM_default/$NEWSIM/g" "$NEWSIM/Sim.sm"
