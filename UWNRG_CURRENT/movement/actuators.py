import array as array
import log as log
import serial as serial
import serial.tools.list_ports as list_ports
import struct as struct
import time as time

def _convert_bytes_to_int(byte_array):
    """ Returns a signed integer from a bytearray type (little endian)

    Keyword Arguments:
    byte_array -- array of 4 bytes

    """
    return struct.unpack('<i', array.array('B', byte_array))[0]

def _convert_int_to_bytes(i):
    """ Returns a bytearray (little endian) from a signed integer

    Keyword Arguments:
    i -- integer to be converted

    """
    return array.array('B', struct.pack('<i', i))

def get_available_com_ports():
    """ Returns a list of all available com-ports """
    return list(list_ports.comports())

class Actuators():
    """ Actuator Controller

    Attributes:
    _SETTINGS -- Settings that can be changed on the actuators. Available
                 settings to add can be found at:
                 http://www.zaber.com/wiki/Manuals/T-LSR#Detailed_Command_Reference
    __properties -- A dictionary utilizing lazy load to speed up accessing of
                    actuator settings
    """
    _SETTINGS = {"MAX_POSITION":44,
                 "ACCELERATION":43,
                 "HOME_OFFSET":47,
                 "SPEED":42}
    __properties = {}
    __x_device = 1
    __y_device = 2

    def flush_buffers(self):
        """ Clears the input and output buffer for the serial connection """
        self.__ser.flushInput()
        self.__ser.flushOutput()

    def get_setting(self, device, setting):
        """ Returns the specified setting's value in a list if multiple devices
        are specified (i.e. device = 0) or a single value if a single device is
        chosen. Utilizes a lazy load system for speed.

        Keyword Arguments:
        device -- The actuator to check the settings of. If 0, check all
                  actuators.
        setting -- The setting to return. Must be one from the self._SETTINGS
                   list.

        """
        if setting in self._SETTINGS:
            if setting not in self.__properties:
                self.__properties[setting] = {}

            #if the device settings are not currently stored
            if (device not in self.__properties[setting] and
                (device != 0 or
                 self.__num_devices != len(self.__properties[setting]))):

                response = self.__issue_command(device,
                                                53,
                                                self._SETTINGS[setting],
                                                0,
                                                0,
                                                0)

                #updates self.__properties with the returned values
                for response_i in response:
                    temp_val = _convert_bytes_to_int(''.join(response_i[2:]))
                    temp_dev_number = ord(response_i[0])
                    self.__properties[setting][temp_dev_number] = temp_val

            #whether to return a list or a single value
            if device == 0:
                return_val = []

                for i in range(self.__num_devices):
                    return_val.append(self.__properties[setting][i + 1])
            else:
                return_val = self.__properties[setting][device]

            return return_val
        else:
            log.log_error("The specified setting '{0}' is not currently " \
                          "supported".format(setting))

    def __init__(self, com_port):
        """ Initializes Actuator Control

        Keyword Arguments:
        com_port -- The com-port the actuators are on.
        num_devices -- The number of actuators being used.

        """
        self.__ser = serial.Serial(com_port)
        self.flush_buffers()

        self.__num_devices = None
        self.__num_devices = len(self.__issue_command(0, 55, 0, 0, 0, 0))

        log.log_info("Actuators have been initialized.")

    def __issue_command(self, b_0, b_1, b_2, b_3, b_4, b_5):
        """ Sends 6 bytes of information to the actuators. It returns the
        response from the actuators. Available commands can be found at:
        http://www.zaber.com/wiki/Manuals/T-LSR#Detailed_Command_Reference

        Keyword arguments:
        b_i -- the ith byte to send to the actuators
        """
        self.__ser.write(bytearray([b_0, b_1, b_2, b_3, b_4, b_5]))
        return self.__read_input(b_0)

    def move(self, vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot relative to it's current
        position. It executes first the x component and then the y component.

        Keyword Arguments:
        self -- actuator object the function was called on
        vector -- movement vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        device = self.__x_device

        if invert_x_axis:
            vector[0] *= -1

        byte_array = _convert_int_to_bytes(vector[0])

        self.__issue_command(device,
                             21,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

        device =  self.__y_device

        if invert_y_axis:
            vector[1] *= -1

        byte_array = _convert_int_to_bytes(vector[1])

        self.__issue_command(device,
                             21,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

    def move_to(self, position_vector, invert_x_axis, invert_y_axis):
        """ Given input parameters, moves the robot to the specified position.
        It will execute the x component and then the y component.

        Keyword Arguments:
        self -- actuator object the function was called on
        position_vector -- position vector
        invert_x_axis -- boolean of whether to invert on the x-axis
        invert_y_axis -- boolean of whether to invert on the y-axis

        """
        device = self.__x_device

        if invert_x_axis:
            max_pos = self.get_setting(device, "MAX_POSITION")
            position_vector[0] = max_pos - position_vector[0]

        byte_array = _convert_int_to_bytes(position_vector[0])

        self.__issue_command(device,
                             20,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

        device = self.__y_device

        if invert_y_axis:
            max_pos = self.get_setting(device, "MAX_POSITION")
            position_vector[1] = max_pos - position_vector[1]

        byte_array = _convert_int_to_bytes(position_vector[1])

        self.__issue_command(device,
                             20,
                             byte_array[0],
                             byte_array[1],
                             byte_array[2],
                             byte_array[3])

    def __read_input(self, device_num):
        """ Returns input from the actuators. Reads until 6 bytes have
        been read per actuator a response is expected from.

        Keyword arguments:
        device_num -- the device number a response is expected from.

        """
        l=[]

        if device_num:
            l.append(self.__read_byte())
        elif self.__num_devices:
            while len(l) < self.__num_devices:
                l.append(self.__read_byte())
        else:
            time.sleep(1)

            while self.__ser.inWaiting() > 0:
                l.append(self.__read_byte())

        print l
        return l

    def __read_byte(self):
        """ Reads a byte from the input. """
        temp = []

        while len(temp) < 6:
            temp.append(self.__ser.read(1))

        return temp

    def renumber_actuators(self):
        """ Sends a command to renumber all the actuators. This must
        be performed after a factory reset of the settings."""
        self.__issue_command(0,2,0,0,0,0)

    def reset_actuators(self):
        """ Factor resets the actuators, flushes the buffers, resets
        all information stored, and returns the actuators to the home
        position. """
        self.__issue_command(0,36,0,0,0,0)
        self.flush_buffers()
        self.__properties = {}
        self.renumber_actuators()
        self.return_to_home(0)

    def return_to_home(self, device):
        """ Returns the specified device to the home position.

        Keyword Arguments:
        device -- the actuator number to send the command to
        """
        self.__issue_command(device,1,0,0,0,0)

    def set_setting(self, device, setting, val):
        """ Sets the desired setting for the desired device to the specified
        value. This will also update the local properties dictionary, thus this
        is the only way settings are allowed to be updated.

        Keyword Arguments:
        device -- the actuator number to send the command to
        setting -- The setting to return. Must be one from the self._SETTINGS
                   list.
        val -- The specified value to set the actuator(s) to.

        """
        if setting in self._SETTINGS:
            byte_array = _convert_int_to_bytes(val)

            self.__issue_command(device,
                                 self._SETTINGS[setting],
                                 byte_array[0],
                                 byte_array[1],
                                 byte_array[2],
                                 byte_array[3])

            if setting not in self.__properties:
                self.__properties[setting] = {}

            if device == 0:
                for i in range(self.__num_devices):
                    self.__properties[setting][i] = val
            else:
                self.__properties[setting][device] = val
        else:
            log.log_error("The specified setting '{0}' is not currently " \
                          "supported".format(setting))
