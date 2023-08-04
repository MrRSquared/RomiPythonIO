#!/usr/bin/env python3
"""
    This is adds the Romi IO to the foundation program.
    It can be found here. 
    https://robotpy.readthedocs.io/en/latest/guide/anatomy.html

"""

# I merged many aspcets of this example https://github.com/robotpy/examples/tree/main/commands-v2/romi on Github to get this running...
# The Following Header is also helpful...

# Example that shows how to connect to a ROMI from RobotPy
#
# Requirements
# ------------
#
# You must have the robotpy-halsim-ws package installed. This is best done via:
#
#    # Windows
#    py -3 -m pip install robotpy[commands2,sim]
#
#    # Linux/macOS
#    pip3 install robotpy[commands2,sim]
#
# Run the program
# ---------------
#
# To run the program you will need to explicitly use the ws-client option:
#
#    # Windows
#    py -3 robot.py sim --ws-client
#
#    # Linux/macOS
#    python robot.py sim --ws-client
#
# By default the WPILib simulation GUI will be displayed. To disable the display
# you can add the --nogui option
#

import wpilib
import wpilib.drive
# This is required for the simulator to work.
import os
# This is required for the Accellerometer and Gyro.
import romi
# we also need to import Math to, you know, do Maths
import math


class MyRobot(wpilib.TimedRobot):
    # We like to start constants with a K
    kCountsPerRevolution = 1440.0 
    # Counts per rev is what it sounds like. How many signals do we get in one revolution.
    kWheelDiameterInch = 2.75591
    # We want the diameter to calculate how far the robot is going and how fast it is moving.
    # Mathmatically, we are (almost) peeling the wheel onto the floor as we drive to calcualte the value.


    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.left_motor = wpilib.Spark(0)
        self.right_motor = wpilib.Spark(1)
        self.drive = wpilib.drive.DifferentialDrive(self.left_motor, self.right_motor)
        self.stick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

        # The Romi has onboard encoders that are hardcoded
        # to use DIO pins 4/5 and 6/7 for the left and right
        self.leftEncoder = wpilib.Encoder(4, 5)
        self.rightEncoder = wpilib.Encoder(6, 7)

        # Set up the RomiGyro
        self.gyro = romi.RomiGyro()

        # Set up the BuiltInAccelerometer
        self.accelerometer = wpilib.BuiltInAccelerometer()

        # Use inches as unit for encoder distances
        self.leftEncoder.setDistancePerPulse(
            (math.pi * self.kWheelDiameterInch) / self.kCountsPerRevolution
        )
        self.rightEncoder.setDistancePerPulse(
            (math.pi * self.kWheelDiameterInch) / self.kCountsPerRevolution
        )
        self.resetEncoders()
    def robotPeriodic(self):
        """
        This function is called once upon each loop.
        """

        # Put data on the smart dashboard
        
        # Encoder Data
        wpilib.SmartDashboard.putNumber("Left Encoder Count", self.leftEncoder.get())
        wpilib.SmartDashboard.putNumber("Right Encoder Count", self.rightEncoder.get())
        wpilib.SmartDashboard.putNumber("Left Encoder Distance", self.leftEncoder.getDistance())
        wpilib.SmartDashboard.putNumber("Right Encoder Distance", self.rightEncoder.getDistance())
        
        # Accelerometer Data
        wpilib.SmartDashboard.putNumber("Acc. X", self.accelerometer.getX())
        wpilib.SmartDashboard.putNumber("Acc. Y", self.accelerometer.getY())
        wpilib.SmartDashboard.putNumber("Acc. Z", self.accelerometer.getZ()) 
        
        # Gyro Data
        wpilib.SmartDashboard.putNumber("Gyro X", self.gyro.getAngleX())
        wpilib.SmartDashboard.putNumber("Gyro Y", self.gyro.getAngleY())
        wpilib.SmartDashboard.putNumber("Gyro Z", self.gyro.getAngleZ()) 

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.drive.arcadeDrive(-0.4, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())

    def resetEncoders(self) -> None:
        """Resets the drive encoders to currently read a position of 0."""
        self.leftEncoder.reset()
        self.rightEncoder.reset()

if __name__ == "__main__":
    # These are the two lines required to connect to the Romi through Python.
    # If your ROMI isn't at the default address, set that here
    os.environ["HALSIMWS_HOST"] = "10.0.0.2"
    os.environ["HALSIMWS_PORT"] = "3300"


    wpilib.run(MyRobot)