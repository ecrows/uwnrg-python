"""
    design choice that all dialogs are modal, and no events will be processed until after they are closed. That means all main work will be done on the main screen. This can be changed, but was too much effort to figure out otherwise as when pressing the escape in the top right corner, even if returning True, it would still destroy the window instead of hide.
"""

import gtk

class  MainWindow:

    def enterMovementInstruction(self, button):
        entry = self.builder_.get_object("instructionEntry")
        combo = self.builder_.get_object("instructionComboBox")
        #combo.get_active()
        ##{0 : "LEFT", 1 : "RIGHT", 2 : "UP", 3 : "DOWN", 4 : "CLOCKWISE", 5 : "CCLOCKWISE"}
        ###for 0&1 multiply entry by invertXAxis, 2&3 multiply entry by invertYAxis, 4&5 multiply entry by both
        #entry.get_text()
        ##defaults to zero (Which is awesome)
        #log that a command was entered, with error checking on input
        #use command to do something

    def invertXAxis(self, checkMenuItem):
        self.invertXAxis_ *= -1;
 
    def invertYAxis(self, checkMenuItem):
        self.invertYAxis_ *= -1;         

    def openAboutWindow(self, menuItem):
        aboutWindow = self.builder_.get_object("AboutWindow")

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        aboutWindow.run()
        aboutWindow.hide()

    def openHelpWindow(self, menuItem): 
        helpWindow = self.builder_.get_object("HelpWindow")

        #do not listen for close events in order for the close button on the window to work, as you are unable to add a signal to the close button
        helpWindow.run()
        helpWindow.hide()

    def __init__(self):
        filename = "GUI.glade"
        self.builder_ = gtk.Builder()
        self.builder_.add_from_file(filename)
        self.invertXAxis_ = 1
        self.invertYAxis_ = 1
        handlers = {
            "gtk_main_quit" : gtk.main_quit,
            "on_MainWindow_destroy" : gtk.main_quit,
            "on_enterInstructionButton_clicked" : self.enterMovementInstruction,
            "on_invertXAxisMenu_toggled" : self.invertXAxis,
            "on_invertYAxisMenu_toggled" : self.invertYAxis,
            "on_AboutMenu_activate" : self.openAboutWindow,
            "on_helpHelpMenu_activate" : self.openHelpWindow,
        }
        self.builder_.connect_signals(handlers)
        self.builder_.get_object("MainWindow").show_all()

app = MainWindow()
gtk.main()

