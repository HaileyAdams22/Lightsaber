"""
--------------------------------------------------------------------------
Interrupt Pin Driver - Lightsaber Project
--------------------------------------------------------------------------
License:   
Copyright 2025 - Hailey Adams

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""

import smbus2
import time

class INT_PIN:
    # MPU6050 Registers and Constants
    MPU6050_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    MOT_THR = 0x1F
    MOT_DUR = 0x20
    INT_ENABLE = 0x38
    INT_STATUS = 0x3A
    ACCEL_XOUT_H = 0x3B

    def __init__(self, bus_number=2):
        self.bus = smbus2.SMBus(bus_number)
        self.bus.write_byte_data(self.MPU6050_ADDR, self.PWR_MGMT_1, 0)  # Wake up
        self.configure_motion_detection()
        print("MPU6050 Interrupt Initialized.")

    def configure_motion_detection(self, threshold=0x10, duration=0x01):
        """
        Configure motion detection interrupt settings.
        """
        self.bus.write_byte_data(self.MPU6050_ADDR, self.MOT_THR, threshold)
        self.bus.write_byte_data(self.MPU6050_ADDR, self.MOT_DUR, duration)
        self.bus.write_byte_data(self.MPU6050_ADDR, self.INT_ENABLE, 0x40)  # Enable motion interrupt
        print("Motion detection configured.")

    def read_accel_data(self):
        """
        Reads and returns X-axis accelerometer data (as an example).
        """
        high = self.bus.read_byte_data(self.MPU6050_ADDR, self.ACCEL_XOUT_H)
        low = self.bus.read_byte_data(self.MPU6050_ADDR, self.ACCEL_XOUT_H + 1)
        value = (high << 8) | low
        return value - 65536 if value > 32767 else value

    def check_interrupt(self):
        """
        Checks if the motion interrupt has been triggered.
        """
        status = self.bus.read_byte_data(self.MPU6050_ADDR, self.INT_STATUS)
        return bool(status & 0x40)

    def clear_interrupt(self):
        """
        Clears the interrupt flag (writing a 1 to bit 6).
        """
        self.bus.write_byte_data(self.MPU6050_ADDR, self.INT_STATUS, 0x40)

    def close(self):
        """
        Cleans up the I2C bus.
        """
        self.bus.close()