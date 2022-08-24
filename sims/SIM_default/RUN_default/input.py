STOP = 10
RATE = 0.1
DEBUG = True

trick.sim_services.exec_set_terminate_time(STOP)

if DEBUG:
    trick.sim_services.exec_set_trap_sigfpe(1)
    simControlPanel = trick.SimControlPanel()
    trick.add_external_application(simControlPanel)
    trickView = trick.TrickView()
    trick.add_external_application(trickView)
    trickView.set_auto_open_file("RUN_default/tv.tv")
    trick.real_time_enable()
    trick.exec_set_software_frame(RATE)
    trick.TMM_reduced_checkpoint(False)
    trick_mm.mm.set_expanded_arrays(True)
    trick_sys.sched.set_enable_freeze(True)
    trick_sys.sched.set_freeze_command(True)
else:
    exec(open("RUN_default/dr.dr").read())
