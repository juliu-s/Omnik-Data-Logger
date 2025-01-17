import struct  # Converting bytes to numbers


class InverterMsg(object):
    """Decode the response message from an omniksol inverter."""
    raw_msg = ""

    def __init__(self, msg, offset=0):
        self.raw_msg = msg
        self.offset = offset

    def __get_string(self, begin, end):
        """Extract string from message.

        Args:
            begin (int): starting byte index of string
            end (int): end byte index of string

        Returns:
            str: String in the message from start to end
        """
        try:
            decoded_str = self.raw_msg[begin:end].decode('utf-8')
        except UnicodeDecodeError:
            decoded_str = self.raw_msg[begin:end].decode('utf-16')
        except:
            raise
            
        return decoded_str

    def __get_short(self, begin, divider=10):
        """Extract short from message.

        The shorts in the message could actually be a decimal number. This is
        done by storing the number multiplied in the message. So by dividing
        the short the original decimal number can be retrieved.

        Args:
            begin (int): index of short in message
            divider (int): divider to change short to float. (Default: 10)

        Returns:
            int or float: Value stored at location `begin`
        """
        num = struct.unpack('!H', self.raw_msg[begin:begin + 2])[0]
        if num == 65535:
            return -1
        else:
            return float(num) / divider

    def __get_long(self, begin, divider=10):
        """Extract long from message.

        The longs in the message could actually be a decimal number. By
        dividing the long, the original decimal number can be extracted.

        Args:
            begin (int): index of long in message
            divider (int): divider to change long to float. (Default : 10)

        Returns:
            int or float: Value stored at location `begin`
        """
        return float(
            struct.unpack('!I', self.raw_msg[begin:begin + 4])[0]) / divider

    @property
    def id(self):
        """ID of the inverter."""
        return self.__get_string(15, 31)

    @property
    def temperature(self):
        """Temperature recorded by the inverter."""
        return self.__get_short(31)

    @property
    def power(self):
        """Power output"""
        return self.__get_short(59)

    @property
    def e_total(self):
        """Total energy generated by inverter in kWh"""
        return self.__get_long(71)

    def v_pv(self, i=1):
        """Voltage of PV input channel.

        Available channels are 1, 2 or 3; if not in this range the function will
        default to channel 1.

        Args:
            i (int): input channel (valid values: 1, 2, 3)

        Returns:
            float: PV voltage of channel i
        """
        if i not in range(1, 4):
            i = 1
        num = 33 + (i - 1) * 2
        return self.__get_short(num)

    def i_pv(self, i=1):
        """Current of PV input channel.

        Available channels are 1, 2 or 3; if not in this range the function will
        default to channel 1.

        Args:
            i (int): input channel (valid values: 1, 2, 3)

        Returns:
            float: PV current of channel i
        """
        if i not in range(1, 4):
            i = 1
        num = 39 + (i - 1) * 2
        return self.__get_short(num)

    def i_ac(self, i=1):
        """Current of the Inverter output channel

        Available channels are 1, 2 or 3; if not in this range the function will
        default to channel 1.

        Args:
            i (int): output channel (valid values: 1, 2, 3)

        Returns:
            float: AC current of channel i

        """
        if i not in range(1, 4):
            i = 1
        num = 45 + (i - 1) * 2
        return self.__get_short(num)

    def v_ac(self, i=1):
        """Voltage of the Inverter output channel

        Available channels are 1, 2 or 3; if not in this range the function will
        default to channel 1.

        Args:
            i (int): output channel (valid values: 1, 2, 3)

        Returns:
            float: AC voltage of channel i
        """
        if i not in range(1, 4):
            i = 1
        num = 51 + (i - 1) * 2
        return self.__get_short(num)

    def f_ac(self, i=1):
        """Frequency of the output channel

        Available channels are 1, 2 or 3; if not in this range the function will
        default to channel 1.

        Args:
            i (int): output channel (valid values: 1, 2, 3)

        Returns:
            float: AC frequency of channel i
        """
        if i not in range(1, 4):
            i = 1
        num = 57 + (i - 1) * 4
        return self.__get_short(num, 100)

    def p_ac(self, i=1):
        """Power output of the output channel

        Available channels are 1, 2 or 3; if no tin this range the function will
        default to channel 1.

        Args:
            i (int): output channel (valid values: 1, 2, 3)

        Returns:
            float: Power output of channel i
        """
        if i not in range(1, 4):
            i = 1
        num = 59 + (i - 1) * 4
        return int(self.__get_short(num, 1))  # Don't divide

    @property
    def e_today(self):
        """Energy generated by inverter today in kWh"""
        return self.__get_short(69, 100)  # Divide by 100

    @property
    def h_total(self):
        """Hours the inverter generated electricity"""
        return int(self.__get_long(75, 1))  # Don't divide
