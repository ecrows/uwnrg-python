class Log:
    """ Follows the borg pattern described at
    http://code.activestate.com/recipes/66531-singleton-we-dont-need-no-stinkin-singleton-the-bo/ Stores the
    buffer, and allows calls from all files to add to the log and clear it

    Public Methods:
    set_buffer -- sets the buffer for all instances of the Log class
    get_buffer -- gets the buffer for the Log class
    clear_log -- clears the Log's buffer

    """
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

    def set_buffer(self, logBuffer):
        """ Sets the buffer for all instances of the Log class

        Keyword arguments:
        logBuffer -- gtk.TextBuffer for the log to use

        """
        self.__shared_state['logBuffer'] = logBuffer

    def get_buffer(self):
        """ Gets the buffer for the Log class """
        return self.__shared_state.get('logBuffer')

    def clear_log(self):
        """ Clears the buffer of the Log class """
        self.__shared_state['logBuffer'].set_text("")

#probably want this to take an Exception class at somepoint
def log_error(text):
    """ Formats the input and sends it to the Log's buffer

    Keyword arguments:
    text -- text to add to the buffer

    """
    log = Log()

    if log.get_buffer():
        i = log.get_buffer().get_end_iter()
        log.get_buffer().insert(i, "ERROR: ")
        log_text(text)

def log_info(text):
    """ Formats the input and sends it to the Log's buffer

    Keyword arguments:
    text -- text to add to the buffer

    """
    log = Log()

    if log.get_buffer():
        i = log.get_buffer().get_end_iter()
        log.get_buffer().insert(i, "INFO: ")
        log_text(text)

def log_text(text):
    """ Formats the input and sends it to the Log's buffer

    Keyword arguments:
    text -- text to add to the buffer

    """
    log = Log()

    if log.get_buffer():
        i = log.get_buffer().get_end_iter()
        log.get_buffer().insert(i, text + '\n')
