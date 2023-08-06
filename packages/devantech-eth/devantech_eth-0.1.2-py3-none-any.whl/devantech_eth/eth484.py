from devantech_eth import module_socket

class ETH484(module_socket.ModuleSocket):
    """
    This class provides all the methods needed for easily controlling an ETH484.
                   
    """
    
    def __init__(self, ip = "192.168.0.2", port = 17494, password = None):
        """
        The constructor for the ETH002 class.

        Parameters:
            ip: (string): The IP address of the module
            port (int): The port number of the module
            password (string): The password used to unlock the module. 
        """
        super().__init__( ip = ip, port = port, password = password, moduleID = 20)

    def getDigitalOutputs(self):
        """
        Get an array that represents the states of the digital outputs.

        Returns:
            array: Bytes indicating the states of the outputs.
        """
        self.write(b'\x24')
        d = self.read(2)
        return d

    def getDigitalInputs(self):
        """
        Get an array that represents the states of the digital outputs.

        Returns:
            array: Bytes indicating the states of the outputs.
        """
        self.write(b'\x25')
        d = self.read(2)
        return d

    def getAnalogueInput(self, port):
        """
        Gets the two bytes that make value of an analogue input.

        Returns:
            array: The bytes that make the analogue value.
        """
        message = "\x32"
        message += chr(port)
        self.write(bytes(message, "utf-8"))
        d = self.read(2)
        return d

    def getAI1Value(self):
        """
        Gets the value of analogue input 1.

        Returns:
            int: the value
        """
        d = self.getAnalogueInput(1)
        v = d[0]
        v <<= 8
        v |= d[1]
        return v

    def getAI2Value(self):
        """
        Gets the value of analogue input 2.

        Returns:
            int: the value
        """
        d = self.getAnalogueInput(2)
        v = d[0]
        v <<= 8
        v |= d[1]
        return v

    def getAI3Value(self):
        """
        Gets the value of analogue input 3.

        Returns:
            int: the value
        """
        d = self.getAnalogueInput(3)
        v = d[0]
        v <<= 8
        v |= d[1]
        return v

    def getAI4Value(self):
        """
        Gets the value of analogue input 4.

        Returns:
            int: the value
        """
        d = self.getAnalogueInput(4)
        v = d[0]
        v <<= 8
        v |= d[1]
        return v
    

    def getDigitalInputs(self):
        """
        Get an array that represents the states of the digital outputs.

        Returns:
            array: Bytes indicating the states of the outputs.
        """
        self.write(b'\x25')
        d = self.read(2)
        return d

    def getDO1State(self):
        """
        Get the state of digital output 1.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[0] & 0b00000001 else 0
        return st

    def getDO2State(self):
        """
        Get the state of digital output 2.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[0] & 0b00000010 else 0
        return st

    def getDO3State(self):
        """
        Get the state of digital output 3.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[0] & 0b00000100 else 0
        return st

    def getDO4State(self):
        """
        Get the state of digital output 4.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[0] & 0b00001000 else 0
        return st

    def getDO9State(self):
        """
        Get the state of digital output 9.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00000001 else 0
        return st

    def getDO10State(self):
        """
        Get the state of digital output 10.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00000010 else 0
        return st

    def getDO11State(self):
        """
        Get the state of digital output 11.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00000100 else 0
        return st

    def getDO12State(self):
        """
        Get the state of digital output 12.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00001000 else 0
        return st

    def getDO13State(self):
        """
        Get the state of digital output 13.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00010000 else 0
        return st

    def getDO14State(self):
        """
        Get the state of digital output 14.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b00100000 else 0
        return st

    def getDO15State(self):
        """
        Get the state of digital output 15.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b01000000 else 0
        return st

    def getDO16State(self):
        """
        Get the state of digital output 16.

        Returns:
            int: 1 for active 0 for inactive
        """
        d = self.getDigitalOutputs()
        st = 1 if d[1] & 0b10000000 else 0
        return st
   
    def setDO1Active(self):
        """
        Sets digital output 1 to active.
        """
        self.digitalActive(1, 0)

    def setDO2Active(self):
        """
        Sets digital output 2 to active
        """
        self.digitalActive(2, 0)

    def setDO3Active(self):
        """
        Sets digital output 3 to active
        """
        self.digitalActive(3, 0)

    def setDO4Active(self):
        """
        Sets digital output 4 to active
        """
        self.digitalActive(4, 0)
        
    def setDO9Active(self):
        """
        Sets digital output 9 to active
        """
        self.digitalActive(9, 0)

    def setDO10Active(self):
        """
        Sets digital output 10 to active
        """
        self.digitalActive(10, 0)

    def setDO11Active(self):
        """
        Sets digital output 11 to active
        """
        self.digitalActive(11, 0)
            
    def setDO12Active(self):
        """
        Sets digital output 12 to active
        """
        self.digitalActive(12, 0)

    def setDO13Active(self):
        """
        Sets digital output 13 to active
        """
        self.digitalActive(13, 0)

    def setDO14Active(self):
        """
        Sets digital output 14 to active
        """
        self.digitalActive(14, 0)

    def setDO15Active(self):
        """
        Sets digital output 15 to active
        """
        self.digitalActive(15, 0)

    def setDO16Active(self):
        """
        Sets digital output 9 to active
        """
        self.digitalActive(16, 0)

    def setDO1Inactive(self):
        """
        Sets digital output 1 to inactive.
        """
        self.digitalInactive(1, 0)
    
    def setDO2Inactive(self):
        """
        Sets digital output 2 to inactive
        """
        self.digitalInactive(2, 0)
    
    def setDO3Inactive(self):
        """
        Sets digital output 3 to inactive
        """
        self.digitalInactive(3, 0)
    
    def setDO4Inactive(self):
        """
        Sets digital output 4 to inactive
        """
        self.digitalInactive(4, 0)
    
    def setDO9Inactive(self):
        """
        Sets digital output 9 to inactive
        """
        self.digitalInactive(9, 0)
        
    def setDO10Inactive(self):
        """
        Sets digital output 10 to inactive
        """
        self.digitalInactive(10, 0)
        
    def setDO11Inactive(self):
        """
        Sets digital output 11 to inactive
        """
        self.digitalInactive(11, 0)
        
    def setDO12Inactive(self):
        """
        Sets digital output 12 to inactive
        """
        self.digitalInactive(12, 0)
        
    def setDO13Inactive(self):
        """
        Sets digital output 13 to inactive
        """
        self.digitalInactive(13, 0)
        
    def setDO14Inactive(self):
        """
        Sets digital output 14 to inactive
        """
        self.digitalInactive(14, 0)
        
    def setDO15Inactive(self):
        """
        Sets digital output 15 to inactive
        """
        self.digitalInactive(15, 0)
        
    def setDO16Inactive(self):
        """
        Sets digital output 16 to inactive
        """
        self.digitalInactive(16, 0)
    
    def setDO1State(self, state):
        """
        Sets the state of digital output 1.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(1, 0, state)

    def setDO2State(self, state):
        """
        Sets the state of digital output 2.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(2, 0, state)

    def setDO3State(self, state):
        """
        Sets the state of digital output 3.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(3, 0, state)

    def setDO4State(self, state):
        """
        Sets the state of digital output 4.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(4, 0, state)

    def setDO9State(self, state):
        """
        Sets the state of digital output 9.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(9, 0, state)

    def setDO10State(self, state):
        """
        Sets the state of digital output 10.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(10, 0, state)

    def setDO11State(self, state):
        """
        Sets the state of digital output 11.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(11, 0, state)

    def setDO12State(self, state):
        """
        Sets the state of digital output 12.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(12, 0, state)

    def setDO13State(self, state):
        """
        Sets the state of digital output 13.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(13, 0, state)

    def setDO14State(self, state):
        """
        Sets the state of digital output 14.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(14, 0, state)

    def setDO15State(self, state):
        """
        Sets the state of digital output 15.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(15, 0, state)

    def setDO16State(self, state):
        """
        Sets the state of digital output 16.

        Parameters: 
            state (int): 0 for inactive, > 0 for active.
        """
        self.setDigitalState(16, 0, state)

    def toggleDO1(self):
        """
        Toggles digital output 1.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[0] & 0b00000001 else 1
        self.setDO1State(st)

    def toggleDO2(self):
        """
        Toggles digital output 2.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[0] & 0b00000010 else 1
        self.setDO2State(st)

    def toggleDO3(self):
        """
        Toggles digital output 3.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[0] & 0b00000100 else 1
        self.setDO3State(st)

    def toggleDO4(self):
        """
        Toggles digital output 4.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[0] & 0b00001000 else 1
        self.setDO4State(st)

    def toggleDO9(self):
        """
        Toggles digital output 9.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00000001 else 1
        self.setDO9State(st)
        
    def toggleDO10(self):
        """
        Toggles digital output 10.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00000010 else 1
        self.setDO10State(st)
        
    def toggleDO11(self):
        """
        Toggles digital output 11.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00000100 else 1
        self.setDO11State(st)
        
    def toggleDO12(self):
        """
        Toggles digital output 12.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00001000 else 1
        self.setDO12State(st)
        
    def toggleDO13(self):
        """
        Toggles digital output 13.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00010000 else 1
        self.setDO13State(st)
        
    def toggleDO14(self):
        """
        Toggles digital output 14.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b00100000 else 1
        self.setDO14State(st)
        
    def toggleDO15(self):
        """
        Toggles digital output 15.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b01000000 else 1
        self.setDO15State(st)
        
    def toggleDO16(self):
        """
        Toggles digital output 16.

        If the output is active it will become active, if it is active it will become inactive.
        """
        d = self.getDigitalOutputs()
        st = 0 if d[1] & 0b10000000 else 1
        self.setDO16State(st)

    def getDI1State(self):
        """
        Gets the state of digital input 1.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00000001 else 0
        return st

    def getDI2State(self):
        """
        Gets the state of digital input 2.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00000010 else 0
        return st

    def getDI3State(self):
        """
        Gets the state of digital input 3.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00000100 else 0
        return st

    def getDI4State(self):
        """
        Gets the state of digital input 4.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00001000 else 0
        return st

    def getDI5State(self):
        """
        Gets the state of digital input 5.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00010000 else 0
        return st

    def getDI6State(self):
        """
        Gets the state of digital input 6.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b00100000 else 0
        return st

    def getDI7State(self):
        """
        Gets the state of digital input 7.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b01000000 else 0
        return st

    def getDI8State(self):
        """
        Gets the state of digital input 8.

        Returns:
            int: 1 is active otherwise 0.
        """
        d = self.getDigitalInputs()
        st = 1 if d[1] & 0b10000000 else 0
        return st
