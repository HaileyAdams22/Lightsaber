"""
--------------------------------------------------------------------------
MPU6050 Driver - Lightsaber Project
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

class MPU6050:
    def __init__(self, bus_num=2, address=0x68):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        self.PWR_MGMT_1 = 0x6B
        self.init_sensor()

    def init_sensor(self):
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0)

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_sensor_data(self):
        data = {
            "accel_x": (self.read_raw_data(0x3B) / 16384.0) - 0.1,
            "accel_y": (self.read_raw_data(0x3D) / 16384.0) + 0.03,
            "accel_z": (self.read_raw_data(0x3F) / 16384.0) + 0.16,
            "gyro_x": (self.read_raw_data(0x43) / 131.0) + 2.3,
            "gyro_y": (self.read_raw_data(0x45) / 131.0) - 0.6,
            "gyro_z": (self.read_raw_data(0x47) / 131.0) + 0.78,
        }

        data["tot_accel"] = data["accel_x"] + data["accel_y"] + data["accel_z"] - 1
        data["tot_gyro"] = data["gyro_x"] + data["gyro_y"] + data["gyro_z"]
        data["comb_accel_gyro"] = abs(data["tot_accel"]) + abs(data["tot_gyro"] / 100)
        return data
