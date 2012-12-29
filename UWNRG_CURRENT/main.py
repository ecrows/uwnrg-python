import gtk as gtk
import facade as facade
import log as log

class  MainWindow:
    """ main window for the application, has no public methods or variables"""
    def __clear_log(self, menu_item):
        """ Clears the log

        Keyword arguments:
        menu_item -- object the action occured on

        """
        self.__log.clear_log()

    def __enter_movement_instruction(self, button):
        """ Sends movement instruction to facade

        Keyword arguments:
        button -- object the action occured on

        """
        direction_conversion = {0: (-1, 0, 0),
                                1: (1, 0, 0),
                                2: (0, 1, 0),
                                3: (0, -1, 0),
                                4: (0, 0, 1),
                                5: (0, 0, -1)}
        direction = direction_conversion[self.__builder.get_object(
                           "manual_control_instruction_combobox").get_active()]
        magnitude = self.__builder.get_object(
                           "manual_control_entry").get_text()

        if magnitude.isdigit():
            magnitude = int(magnitude)
            facade.move(tuple(magnitude * x for x in direction),
                                  self.__x_axis_inverted,
                                  self.__y_axis_inverted)
        else:
            log.log_error("The magnitude of a movement must be an integer, " \
                          "'{0}' is not an integer.".format(magnitude))

    def __keyboard_movement_instruction(self, window, event):
        """ Sends movement instruction to facade

        Keyword arguments:
        window -- object the action occured on
        event -- contains information about the key press event

        """
        direction_conversion = {97: (-1, 0, 0),
                                100: (1, 0, 0),
                                119: (0, 1, 0),
                                115: (0, -1, 0),
                                101: (0, 0, 1),
                                113: (0, 0, -1)}
        key_pressed = event.keyval

        if key_pressed in direction_conversion and self.__keyboard_input :
            direction = direction_conversion[key_pressed]
            direction = [x * self.__actuator_step for x in direction]
            facade.move(direction,
                        self.__x_axis_inverted,
                        self.__y_axis_inverted)

    def __init__(self):
        filename = "GUI.glade"
        handlers = {
            "on_setup_menu_exit_activate" : gtk.main_quit,
            "on_main_window_destroy" : gtk.main_quit,
            "on_manual_control_enter_button_clicked" :
                                             self.__enter_movement_instruction,
            "on_edit_menu_invert_x_axis_toggled" : self.__invert_x_axis,
            "on_edit_menu_invert_y_axis_toggled" : self.__invert_y_axis,
            "on_help_menu_about_activate" : self.__open_about_window,
            "on_help_menu_help_activate" : self.__open_help_window,
            "on_tools_menu_manual_keyboard_input_toggled" :
                                                  self.__toggle_keyboard_input,
            "on_main_window_key_press_event" :
                                          self.__keyboard_movement_instruction,
            "on_edit_menu_clear_log_activate" : self.__clear_log,
            "on_emma_mode_radio_toggled" : self.__switch_mode_EMMA,
            "on_copter_mode_radio_toggled" : self.__switch_mode_copter,
            "on_setup_menu_actuators_activate" :
                                            self.__open_actuator_setup_window
        }

        self.__builder = gtk.Builder()
        self.__builder.add_from_file(filename)
        self.__builder.connect_signals(handlers)
        self.__builder.get_object("main_window").show_all()

        self.__keyboard_input = True
        self.__log = log.Log()
        self.__x_axis_inverted = False
        self.__y_axis_inverted = False
        self.__actuator_step = 1

        self.__log.set_buffer(self.__builder.get_object(
                "vertical_log_scroll_window_text_view").get_property('buffer'))

    def __invert_x_axis(self, check_menu_item):
        """ Updates x inversion variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__x_axis_inverted ^= True;

    def __invert_y_axis(self, check_menu_item):
        """ Updates y inversion variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__y_axis_inverted ^= True;

    def __open_about_window(self, menu_item):
        """ Opens the about program window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        about_window = self.__builder.get_object("about_window")

        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        about_window.run()
        about_window.hide()

    def __open_help_window(self, menu_item):
        """ Opens the help program window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        help_window = self.__builder.get_object("help_window")

        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        help_window.run()
        help_window.hide()

    def __open_actuator_setup_window(self, menu_item):
        """ Opens the actuator setup window

        Keyword arguments:
        menu_item -- object the action occured on

        """

        com_port_combo = self.__builder.get_object("com_port_combo")
        available_com_ports = facade.get_available_com_ports()

        for i in available_com_ports:
            com_port_combo.append_text(i[0])

        actuator_setup_window = self.__builder.get_object("actuator_setup_window")
        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        actuator_setup_window.run()
        actuator_setup_window.hide()

        facade.set_com_port(com_port_combo.get_active_text())

        actuator_step_entry = self.__builder.get_object("actuator_step_entry")
        actuator_step = actuator_step_entry.get_text()

        if actuator_step.isdigit():
            self.__actuator_step = int(actuator_step)
        else:
            log.log_error("The magnitude of actuator step must be an integer,"\
                          " '{0}' is not an integer.".format(magnitude))

    def __switch_mode_EMMA(self, check_menu_item):
        """ Checks to see if EMMA mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_EMMA()

    def __switch_mode_copter(self, check_menu_item):
        """ Checks to see if the copter mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_copter()

    def __toggle_keyboard_input(self, menu_item):
        """ Updates keyboard input variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__keyboard_input ^= True;

app = MainWindow()
gtk.main()
