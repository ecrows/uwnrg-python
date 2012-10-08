import gtk

class  TEST:

    def __init__(self):
        filename = "GUI.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)
        builder.get_object("MainWindow").show_all()
        window = builder.get_object("MainWindow")
        window.connect("destroy", gtk.main_quit)
        combo = builder.get_object("combobox1")
        print combo.get_has_entry()

app = TEST()
gtk.main()

