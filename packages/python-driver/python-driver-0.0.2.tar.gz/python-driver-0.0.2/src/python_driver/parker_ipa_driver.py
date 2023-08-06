'''
Created on 12/01/2021

@author: dpeterjohn
'''
from cmath import log
import time
import logging
import win32com.client
from ipaddress import IPv4Address
from contextlib import contextmanager


class MaximumPositionError(Exception):
    """Raised when the maximum allowable error between the commanded position and the actual position is violated"""
    pass


class KillAllMotionRequestException(Exception):
    """Raised when the kill all motion request is received"""
    pass


class MaximumRailLimitError(Exception):
    """Raised when the commanded position is greater than the maximum rail limit (X.Max=1980)"""
    pass


class MinimumRailLimitError(Exception):
    """Raised when the commanded position is less than the minimum rail limit (X.Min=0)"""
    pass


class ParkerIpaDriver:
    # For documentation on the ComACRServer6 methods/library see "ComACRServer6_User_Guide.pdf"

    CONNECTION_TYPE = {"OFFLINE": 0, "SERIAL": 2, "IP": 3, "USB": 4}
    MOVE_MODE = ["Mode-Continuous", "Mode-Cornering",
                 "Mode-Start Stop", "Mode-Rapid Start Stop"]
    MOVE_COUNTER = {"Counter Off": 0,
                    "Counter On Up": 1, "Counter On Down": -1}
    AXIS_NUMBER = 0

    def __init__(self):
        self._com_acr_server = win32com.client.DispatchEx(
            'ComACRServer.Channel')
        self.data_dict = {}
        self.data_dict = self.__get_robot_data(
            "C:\ProgramData\Banner\Banner Robotic Data Collection System\Banner Robotic Data Collection System_Robot.ini")
        #self.data_dict = self.__get_robot_data("src\data.txt")

    @contextmanager
    def connect_serial(self):
        raise NotImplementedError

    @contextmanager
    def connect_usb(self):
        raise NotImplementedError

    @contextmanager
    def connect_ip(self, ip_address: IPv4Address, home: bool = True):
        """Connect based on the IP address. Once connect successfully, the robot will home by default. 
        Args:
            ip_address (string): IP address
            home (bool, optional): if true, robot performs a 'home' operation once it has successfully connected 
        """
        self._com_acr_server.bstrIP = str(ip_address)
        # Note: second parameter is not used; provided for compatibility with legacy code.
        self._com_acr_server.Connect(self.CONNECTION_TYPE["IP"], 0)
        if (self._com_acr_server.isOffline):
            raise ConnectionError(
                f"Could not connect to IPA at IP {str(ip_address)}")
        try:
            logging.info(f"Connected v{self._com_acr_server.bstrVersion}")
            self._com_acr_server.fMoveVEL = float(self.data_dict["Velocity"])
            self._com_acr_server.fMoveFVEL = float(self.data_dict["Velocity"])
            self._com_acr_server.fMoveACC = float(
                self.data_dict["Acceleration"])
            if home == True:
                self.home()
            yield
        finally:
            self._com_acr_server.Disconnect()
            logging.info(f"Disconnected v{self._com_acr_server.bstrVersion}")

    def drive_switch(self, switch: bool):
        """Based on the user input, enable or disable the drive
        Args:
            switch (bool): If true, the drive is enabled. If false, the drive is disabled
        """
        self._com_acr_server.SetFlag(8465, switch, True)
        quaternary_axis_status_flags = self._com_acr_server.GetACRCustom("P4360")[
            0]
        if self._com_acr_server.IsFlagSet(quaternary_axis_status_flags, 17):
            logging.info("drive ON")
        else:
            logging.info("drive OFF")

    def home(self):
        """Move rail to the machine origin (position 0) and then sets the absolute position register to zero, establishing a zero reference position
        """
        # Jog Home Direction Flag. Determines JOG HOME direction when JOG HOME Request flag has been set. 0 is positive, 1 is negative direction
        self._com_acr_server.SetFlag(17161, True, True)
        # Jog Home Request Flag. Initiates a JOG HOME command.
        self._com_acr_server.SetFlag(17160, True, True)

        # Give the rail controller some time to receive/process data/commands
        time.sleep(1)

        while True:
            # The parameter of GetACRCustom() is string of up to 32 p-Parameters, comma delimited.  The return value is a tuple cotaining the value(s) of requested p-Parameter(s)
            quinary_axis_status_flags = self._com_acr_server.GetACRCustom("P4600")[
                0]
            # Find home success flag
            if self._com_acr_server.IsFlagSet(quinary_axis_status_flags, 6):
                logging.info("Home successfully found")
                break
            # Find home failure flag
            elif self._com_acr_server.IsFlagSet(quinary_axis_status_flags, 7):
                raise Exception("Failed to find Home")

    def move(self, position_mm: float, is_move_absolute: bool = True, velocity: float = -1, final_velocity: float = -1, acceleration: float = -1):
        """Move rail to an absolute position or relative to current position
        Args:
            position_mm (float): position in millimeters
            is_move_absolute (bool, optional): True for an absolute move or false for a relative move. Defaults to True.
            velocity (float, optional): negative values are ignored and cause the existing profile velocity to be used. Defaults to -1.
            final_velocity (float, optional): negative values are ignored and cause the existing profile final velocity to be used. Defaults to -1.
            acceleration (float, optional): negative values are ignored and cause the existing profile acceleration to be used. Defaults to -1.
        """
        self.__check_fault()

        if is_move_absolute:
            self.__rail_limit_check(position_mm)
            position_mm = self.__flip_position(position_mm)
        else:
            self.__rail_limit_check(
                self.__get_commanded_position() + position_mm)
            position_mm = float(self.data_dict["X.Slope"]) * position_mm

        self._com_acr_server.nMoveMode = self.MOVE_MODE.index(
            "Mode-Rapid Start Stop")
        self._com_acr_server.nMoveCounter = self.MOVE_COUNTER["Counter On Down"]
        self._com_acr_server.bMoveAbsolute = is_move_absolute

        self._com_acr_server.nMoveProfile = 0

        self._com_acr_server.fMoveVEL = velocity
        self._com_acr_server.fMoveFVEL = final_velocity
        self._com_acr_server.fMoveACC = acceleration

        axis_mask = int(1 << self.AXIS_NUMBER)

        targets = [position_mm]

        self._com_acr_server.Move(axis_mask, targets)

        # Give the rail controller some time to receive/process data/commands
        time.sleep(1)

        # Block execution until rail has finished moving
        while True:
            self.__check_fault()
            if (self.is_moving() == False):
                break

    def is_moving(self) -> bool:
        """Check whether the rail is moving or not. If it is moving, return True. Otherwise, return False
        """
        target_position = self._com_acr_server.GetACRCustom("P12289")[0]
        commanded_position = self._com_acr_server.GetACRCustom("P12295")[0]
        if not target_position == commanded_position:
            logging.debug("true : " + str(self.__get_commanded_position()))
            return True
        logging.debug("false : " + str(self.__get_commanded_position()))
        return False

    def stop(self):
        """Stop the rail movement
        """
        self._com_acr_server.Stop(False)
        self.is_moving()
        while (self.is_moving() == True):
            logging.debug(" stop")
            pass
        self.__clear_stop()

    def __clear_stop(self):
        """Reset the stop moving bits, which is a necessary step to enable a new movement after calling stop()  
        """
        # Stop All Moves Flag
        #   Setting this Flag will stop all moves without using any acceleration or deceleration ramps.
        #   This flag does not halt any programs or PLCs.
        #   The user is responsible for clearing this Flag.
        self._com_acr_server.SetFlag(523, False, True)

        # Kill All Moves Flag
        #   Setting this Flag will cause the master to respond the same as receiving a Feedhold Request,
        #   wait for "In Feedhold" flag, and then follow with a Kill All Moves.
        #   Processor acknowledgment clears the Kill All Moves Flag.
        #   The user is responsible for clearing the Kill All Moves Flag."""
        self._com_acr_server.SetFlag(522, False, True)

    def __get_robot_data(self, file: str) -> dict:
        """Read and initialize robotic data. If data doesn't exist, set to a default value or raise exception. if data has a wrong value, raise exception
        Args:
            file (string): the file path to a .ini file that stores robotic data
        """
        with open(file, 'r') as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=")
                    self.data_dict[key] = value.replace("\"", "")

        if "Robot" not in self.data_dict.keys() or "IPAddress" not in self.data_dict.keys() or "X.Min" not in self.data_dict.keys() or "X.Max" not in self.data_dict.keys():
            raise Exception("not sufficient data to initialize robot")
        if self.data_dict["Robot"] != "ParkerIPA":
            raise Exception("wrong Robot")
        if "Velocity" not in self.data_dict.keys():
            self.data_dict["Velocity"] = -1
        if "Acceleration" not in self.data_dict.keys():
            self.data_dict["Acceleration"] = -1
        if "X.Offset" not in self.data_dict.keys():
            self.data_dict["X.Offset"] = 0
        if "X.Slope" not in self.data_dict.keys():
            self.data_dict["X.Slope"] = 1
        return self.data_dict

    def __rail_limit_check(self, position: float):
        """Throw exception if rail tries to move outside of limits

        Args:
            position (float): position in millimeters

        Raises:
            MinimumRailLimitError: position is less than rail minimum
            MaximumRailLimitError: position is greater than rail maximum
        """
        if position < float(self.data_dict["X.Min"]):
            raise MinimumRailLimitError(
                f"Position: {position} is less than rail minimum of {float(self.data_dict['X.Min'])}")
        if position > float(self.data_dict["X.Max"]):
            raise MaximumRailLimitError(
                f"Position: {position} is greater than rail maximum of {float(self.data_dict['X.Max'])}")

    def __flip_position(self, position: float) -> float:
        """Flip direction/movement based on X.Offset and X.Slope
        Args:
            position (float): position in millimeters
        """
        return float(self.data_dict["X.Offset"]) + position * float(self.data_dict["X.Slope"])

    def __get_commanded_position(self) -> float:
        """Get commanded position.
        Also referred to as "Secondary Setpoint" in documentation.
        """
        position = self._com_acr_server.GetACRCustom(
            "P12295")[0] / self.__get_pulse_per_units()
        return self.__flip_position(position)

    def __get_actual_position(self) -> float:
        """Get actual position read through feedback.
        """
        position = self._com_acr_server.GetACRCustom(
            "P12290")[0] / self.__get_pulse_per_units()
        return self.__flip_position(position)

    def __get_target_position(self) -> float:
        """Get user programmed target position of the buffered move.
        """
        position = self._com_acr_server.GetACRCustom(
            "P12289")[0] / self.__get_pulse_per_units()
        return self.__flip_position(position)

    def get_position(self) -> float:
        """A public method to get actual position by calling __get_actual_position(self).
        """
        return self. __get_actual_position()

    def __get_pulse_per_units(self) -> float:
        """Pulse per Programming Unit (PPU) for axis.
        """
        return self._com_acr_server.GetACRCustom("P12375")[0]

    def __print_parameter_b(self, p_parameter: str = "P4112"):
        """Print the value of requested P-parameter in binary 
        Args:
            p_parameter (string, optional): requested p-parameter, default to p4112, the motion status showing stop, acc, dec, move 
        """
        status = self._com_acr_server.GetACRCustom(p_parameter)[0]
        print("{0:b}".format(status))

    def __check_fault(self):
        """Check the control status of the rail. If faults occur, rail exception. 
        """
        # Fourth set of axis status flags
        quaternary_axis_status_flags = self._com_acr_server.GetACRCustom("P4360")[
            0]

        # Latched Excess Position Error Flag:
        #   Indicates that excess position error has been detected, and that motion has been killed and the drive disabled as a result.
        #   Stays latched until cleared with a DRIVE ON command.
        if (self._com_acr_server.IsFlagSet(quaternary_axis_status_flags, 31)):
            raise MaximumPositionError(
                f"The maximum allowable error between the actual position: {self.__get_actual_position()} and the commanded position {self.__get_commanded_position()} is violated")
        # Kill All Motion Request Flag:
        #   When this bit is enabled, all motion is killed for the axis.
        #   Motion is killed when end of travel limits are encountered, a drive fault is detected, or excess position error is detected.
        if (self._com_acr_server.IsFlagSet(quaternary_axis_status_flags, 19)):
            raise KillAllMotionRequestException(
                "Kill all motion request is received")
