"""
    design choice that all dialogs are modal, and no events will be processed until after they are closed. That means all main work will be done on the main screen. This can be changed, but was too much effort to figure out otherwise as when pressing the escape in the top right corner, even if returning True, it would still destroy the window instead of hide.
"""
import gtk
import facade
import log

class  MainWindow:
    def __enterMovementInstruction(self, button):
        comboConversion = {0 : facade.LEFT, 1 : facade.RIGHT, 2 : facade.UP, 3 : facade.DOWN, 4 : facade.CLOCKWISE, 5 : facade.CCLOCKWISE}
        direction = comboConversion[self.builder_.get_object("instructionComboBox").get_active()]

        magnitude = self.builder_.get_object("instructionEntry").get_text()

        if magnitude.isdigit():
            facade.moveImmediate(int(magnitude), direction)
        #else:
        #    log that an integer must be inputted for the magnitude
            
        ###for the implementation of this, 0&1 multiply entry by invertXAxis, 2&3 multiply entry by invertYAxis, 4&5 multiply entry by both

#editable - the editable that received the signal
#new_text - the string that is being inserted
#new_text_length - the length of the new text
#position - a pointer to the location at which the new text will be inserted

    def __invertXAxis(self, checkMenuItem):
        self.invertXAxis_ ^= True;
 
    def __invertYAxis(self, checkMenuItem):
        self.invertYAxis_ ^= True;         

    def __openAboutWindow(self, menuItem):
        aboutWindow = self.builder_.get_object("AboutWindow")

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        aboutWindow.run()
        aboutWindow.hide()

    def __openHelpWindow(self, menuItem): 
        helpWindow = self.builder_.get_object("HelpWindow")

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        helpWindow.run()
        helpWindow.hide()

    def __toggleKeyboardInput(self, menuItem):
        self.keyboardInput_ ^= True;

    def __keyboardMovementInstruction(self, window, event):
        keyPressed = event.keyval
        comboConversion = {97 : facade.LEFT, 100 : facade.RIGHT, 119 : facade.UP, 115 : facade.DOWN, 101 : facade.CLOCKWISE, 113 : facade.CCLOCKWISE}

        if keyPressed in comboConversion and self.keyboardInput_ :
            direction = comboConversion[keyPressed]
    
            magnitude = facade.DEFAULT_MOVEMENT_MAGNITUDE
    
            facade.moveImmediate(magnitude, direction)


    def __init__(self):
        filename = "GUI.glade"
        self.builder_ = gtk.Builder()
        self.builder_.add_from_file(filename)
        self.invertXAxis_ = False
        self.invertYAxis_ = False
        self.keyboardInput_ = True
        log._log.setBuffer(self.builder_.get_object("logView").get_property('buffer')) #sets the buffer for local log variable in the Log file

        handlers = {
            "gtk_main_quit" : gtk.main_quit,
            "on_MainWindow_destroy" : gtk.main_quit,
            "on_enterInstructionButton_clicked" : self.__enterMovementInstruction,
            "on_invertXAxisMenu_toggled" : self.__invertXAxis,
            "on_invertYAxisMenu_toggled" : self.__invertYAxis,
            "on_AboutMenu_activate" : self.__openAboutWindow,
            "on_helpHelpMenu_activate" : self.__openHelpWindow,
            "on_keyboardInputMenu_toggled" : self.__toggleKeyboardInput,
            "on_MainWindow_key_press_event" : self.__keyboardMovementInstruction,
        }
        self.builder_.connect_signals(handlers)
        self.builder_.get_object("MainWindow").show_all()

app = MainWindow()
gtk.main()
