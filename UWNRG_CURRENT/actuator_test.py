import movement.actuators as actuators
a = actuators.Actuators(actuators.get_available_com_ports()[0][0])
a.reset_actuators()
print a.get_setting(1, "MAX_POSITION")
print a.get_setting(1, "MAX_POSITION")
print a.get_setting(0, "MAX_POSITION")
print a.get_setting(1, "MAX_POSITION")
print a.get_setting(2, "MAX_POSITION")
a.set_setting(1, "MAX_POSITION", 1000)
print a.get_setting(1, "MAX_POSITION")
print a.get_setting(2, "MAX_POSITION")
print a.get_setting(0, "MAX_POSITION")
a.set_setting(2, "MAX_POSITION", 4000)
print a.get_setting(0, "MAX_POSITION")
a.reset_actuators()
print a.get_setting(0, "MAX_POSITION")
a.move_to([0,0], True, True)
a.move_to([0,0], True, True)
a.move_to([1000,1000], False, False)
a.move([10000,0], False, False)
a.move([-10000,0], False, False)
a.move([-10000,0], True, False)
a.move([0,-10000], True, True)
a.move([0,10000], False, False)
a.move([0,10000], False, True)
