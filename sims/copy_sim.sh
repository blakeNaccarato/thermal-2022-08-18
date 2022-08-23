cd "/root/thermal-2022-08-18/sims"
cp -r "SIM_default" "SIM_$1"
sed -i "s/SIM_default/SIM_$1/g" "SIM_$1/Sim.sm"
