trick.sim_services.exec_set_trap_sigfpe(1)
simControlPanel = trick.SimControlPanel()
trick.add_external_application(simControlPanel)
trickView = trick.TrickView()
trick.add_external_application(trickView)
trickView.set_auto_open_file('TV_potential.tv')
trick.real_time_enable()
trick.sim_services.exec_set_terminate_time(10)
trick.exec_set_software_frame(0.001)
trick.TMM_reduced_checkpoint(False)
trick_mm.mm.set_expanded_arrays(True)
trick_sys.sched.set_enable_freeze(True)
trick_sys.sched.set_freeze_command(True)

# exec(open("RUN_test/my_results.dr").read())

# # Input
# mySimObject.model.netInput.capacitor.mCapacitance = 10
# mySimObject.model.netInput.thermal_potential.mSourcePotential = 150
# mySimObject.model.netInput.thermal_potential2.mSourcePotential = 50

# # Config
# mySimObject.model.netConfig.conductor.mDefaultConductivity = 10
