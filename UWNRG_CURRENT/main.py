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
            facade.move(list(magnitude * x for x in direction),
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

        speed_change = {45 : -1, 43 : 1}

        key_pressed = event.keyval

        if key_pressed in direction_conversion and self.__keyboard_input:
            direction = direction_conversion[key_pressed]
            direction = [x * self.__actuator_step for x in direction]
            facade.move(direction,
                        self.__x_axis_inverted,
                        self.__y_axis_inverted)
        elif key_pressed in speed_change and self.__keyboard_input:
            facade.change_speed(speed_change[key_pressed])

    def __end_keyboard_movement_instruction(self, window, event):
        """ Ends Movment Instruction to facade

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

        if key_pressed in direction_conversion and self.__keyboard_input:
            direction = direction_conversion[key_pressed]
            direction = [x for x in direction]
            facade.end_move(direction,
                        self.__x_axis_inverted,
                        self.__y_axis_inverted)

    def __figure_eight(self, menu_item):
        facade.figure_eight()

    def __toggle_solenoid_awp(self, menu_item):
        temp = facade.toggle_awp()
        if temp == None:
            log.log_info("Failed to set AWP")
        elif temp:
            log.log_info("AWP is on")
        else:
            log.log_info("AWP is off")

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
            "on_emma_mode_actuator_radio_toggled" : self.__switch_mode_EMMA_actuator,
            "on_emma_mode_solenoid_radio_toggled" : self.__switch_mode_EMMA_solenoid,
            "on_copter_mode_radio_toggled" : self.__switch_mode_copter,
            "on_setup_menu_actuators_activate" :
                                            self.__open_actuator_setup_window,
            "on_setup_menu_solenoids_activate" :
                                            self.__open_solenoid_setup_window,
            "on_setup_menu_camera_activate" : self.__open_img_window,
            "on_img_ok_close_clicked" : self.__save_image_settings,
            "on_tools_menu_stop_camera_feed_activate" : self.__stop_feed,
            "on_tools_menu_start_camera_feed_activate" : self.__start_feed,
            "on_figure_eight_activate" : self.__figure_eight,
            "on_main_window_key_release_event" :
                                          self.__end_keyboard_movement_instruction
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
        self.__solenoid_step = 1

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

    def __open_solenoid_setup_window(self, menu_item):
        """ Opens the solenoid setup window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        #set the current solenoid step value in the textbox
        solenoid_step_entry = self.__builder.get_object("solenoid_step_entry1")
        solenoid_step_entry.set_text(str(self.__solenoid_step))

        #set the desired current value in the textbox
        solenoid_desired_current_entry = self.__builder.get_object("solenoid_adc_entry")
        solenoid_desired_current_entry.set_text(str(facade.get_desired_current()))

        solenoid_setup_window = self.__builder.get_object("solenoid_setup_window")
        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        solenoid_setup_window.run()
        solenoid_setup_window.hide()

        #sets the solenoid step
        solenoid_step = solenoid_step_entry.get_text()

        if solenoid_step.isdigit():
            self.__solenoid_step = int(solenoid_step)
        else:
            log.log_error("The magnitude of solenoid time must be an integer,"\
                          " '{0}' is not an integer.".format(magnitude))

        #sets the desired current for solenoids
        solenoid_desired_current = solenoid_desired_current_entry.get_text()

        try:
            facade.set_desired_current(float(solenoid_desired_current))
        except ValueError:
            log.log_error("The desired current must be a decimal number,"\
                          " '{0}' is not an integer.".format(solenoid_desired_current))

        #switches the adc
        toggle_solenoid_adc = self.__builder.get_object("toggle_solenoid_adc")
        if toggle_solenoid_adc.get_active():
            response = facade.toggle_solenoid_adc()

            if response != None:
                switch_actuator_axis.set_active(response)

    def __open_actuator_setup_window(self, menu_item):
        """ Opens the actuator setup window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        #set the combo box values
        com_port_combo = self.__builder.get_object("com_port_combo")
        available_com_ports = facade.get_available_com_ports()
        com_port_liststore = self.__builder.get_object("com_port_liststore")
        com_port_liststore.clear()

        for com_port_info in available_com_ports:
            com_port_combo.append_text(com_port_info[0])

        com_port_combo.set_active(0)

        #set the current actuator step value in the textbox
        actuator_step_entry = self.__builder.get_object("actuator_step_entry")
        actuator_step_entry.set_text(str(self.__actuator_step))

        actuator_setup_window = self.__builder.get_object("actuator_setup_window")
        # do not listen for close events in order for the close button on the
        # window to work, as you are unable to add a signal to the close button
        actuator_setup_window.run()
        actuator_setup_window.hide()

        #sets the com-port for the actuators
        facade.set_com_port(com_port_combo.get_active_text())

        #sets the actuator step
        actuator_step = actuator_step_entry.get_text()

        if actuator_step.isdigit():
            self.__actuator_step = int(actuator_step)
        else:
            log.log_error("The magnitude of actuator step must be an integer,"\
                          " '{0}' is not an integer.".format(magnitude))

        #switches the actuator axis if the box was checked
        switch_actuator_axis = self.__builder.get_object("switch_actuator_axis")

        if switch_actuator_axis.get_active():
            facade.switch_actuator_axis()
            switch_actuator_axis.set_active(False)

    def __switch_mode_EMMA_solenoid(self, check_menu_item):
        """ Checks to see if EMMA mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_EMMA_solenoid()

    def __switch_mode_EMMA_actuator(self, check_menu_item):
        """ Checks to see if EMMA mode is being enabled

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        if check_menu_item.active:
            facade.switch_to_EMMA_actuator()

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

    def __open_img_window(self, menu_item):
        """ Opens the image settings window """
        img_window = self.__builder.get_object("img_window")

        img_window.run()
        img_window.hide()

        # TODO: Backup old image settings, so that if the user presses
        # "Cancel" old image settings are restored

        # image window will display settings, camera feed will be displayed in separate window
        # if time permits, camera feed should be embedded directly into window

    def __save_image_settings(self, menu_item):
        """ Update camera settings upon pressing OK """
        facade.confirm_new_settings(med_width, ad_bsize, ad_const, can_low, can_high)

    def __start_feed(self, menu_item):
        """ Start camera feed """
        if (self.__field.thread_running == False):
            self.__field.thread_running = True
            t = threading.Thread(target=self.__work)
            t.start()
            #facade.start_feed(self.__field)

    def __stop_feed(self, menu_item):
        """ Terminate camera feed """
        if (self.__field.thread_running == True):
            facade.stop_feed(self.__field)
            self.__field.thread_running = False

app = MainWindow()
gtk.main()
