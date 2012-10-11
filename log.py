"""
    this file is horrible
    it allows the buffer for the logs to be sent to be set here
    _log is local to the file so that logError, logInfo, and logText can be called as log._functionName_
    _log is however accessed in main.py during the initialization
"""

class Log:
    def setBuffer(self, logBuffer):
        self.logBuffer_ = logBuffer

_log = Log()

def logError(text):
    i = _log.logBuffer_.get_end_iter()
    _log.logBuffer_.insert(i, "ERROR: ")
    logText(text)

def logInfo(text):
    i = _log.logBuffer_.get_end_iter()
    _log.logBuffer_.insert(i, "INFO: ")
    logText(text)

def logText(text):
    i = _log.logBuffer_.get_end_iter()
    _log.logBuffer_.insert(i, text + '\n')
