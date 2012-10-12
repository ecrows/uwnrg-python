"""
design choice that all dialogs are modal, and no events will be processed until after they are closed. That means all main work will be done on the main screen. This can be changed, but was too much effort to figure out otherwise as when pressing the escape in the top right corner, even if returning True, it would still destroy the window instead of hide.
"""
import gtk
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
        comboConversion = {0 : facade.LEFT, 1 : facade.RIGHT, 2 : facade.UP, 3 : facade.DOWN, 4 : facade.CLOCKWISE, 5 : facade.CCLOCKWISE}
        direction = comboConversion[self.__builder.get_object("manual_control_instruction_combobox").get_active()]
        magnitude = self.__builder.get_object("manual_control_entry").get_text()

        if magnitude.isdigit():
            facade.move_immediate(int(magnitude), direction, self.__x_axis_inverted, self.__y_axis_inverted)
        else:
            log.log_error("The magnitude of a movement must be an integer, '{0}' is not an integer.".format(magnitude))

    def __keyboard_movement_instruction(self, window, event):
        """ Sends movement instruction to facade

        Keyword arguments:
        window -- object the action occured on
        event -- contains information about the key press event

        """
        key_pressed = event.keyval
        combo_conversion = {97 : facade.LEFT, 100 : facade.RIGHT, 119 : facade.UP, 115 : facade.DOWN, 101 : facade.CLOCKWISE, 113 : facade.CCLOCKWISE}

        if key_pressed in combo_conversion and self.__keyboard_input :
            direction = combo_conversion[key_pressed]
            magnitude = facade.DEFAULT_MOVEMENT_MAGNITUDE
            facade.move_immediate(magnitude, direction, self.__x_axis_inverted, self.__y_axis_inverted)

    def __init__(self):
        filename = "GUI.glade"
        handlers = {
            "on_setup_menu_exit_activate" : gtk.main_quit,
            "on_main_window_destroy" : gtk.main_quit,
            "on_manual_control_enter_button_clicked" : self.__enter_movement_instruction,
            "on_edit_menu_invert_x_axis_toggled" : self.__invert_x_axis,
            "on_edit_menu_invert_y_axis_toggled" : self.__invert_y_axis,
            "on_help_menu_about_activate" : self.__open_about_window,
            "on_help_menu_help_activate" : self.__open_help_window,
            "on_tools_menu_manual_keyboard_input_toggled" : self.__toggle_keyboard_input,
            "on_main_window_key_press_event" : self.__keyboard_movement_instruction,
            "on_edit_menu_clear_log_activate" : self.__clear_log
        }

        self.__builder = gtk.Builder()
        self.__builder.add_from_file(filename)
        self.__builder.connect_signals(handlers)
        self.__builder.get_object("main_window").show_all()

        self.__keyboard_input = True
        self.__log = log.Log()
        self.__mode = facade.ACTUATOR
        self.__x_axis_inverted = False
        self.__y_axis_inverted = False

        self.__log.set_buffer(self.__builder.get_object("vertical_log_scroll_window_text_view").get_property('buffer'))

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

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        about_window.run()
        about_window.hide()

    def __open_help_window(self, menu_item):
        """ Opens the help program window

        Keyword arguments:
        menu_item -- object the action occured on

        """
        help_window = self.__builder.get_object("help_window")

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        help_window.run()
        help_window.hide()

    def __toggle_keyboard_input(self, menu_item):
        """ Updates keyboard input variable

        Keyword arguments:
        check_menu_item -- object the action occured on

        """
        self.__keyboard_input ^= True;

app = MainWindow()
gtk.main()
