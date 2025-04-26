"""
--------------------------------------------------------------------------
sLED DotStar Driver - Lightsaber Project
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

# Import libraries
import spidev
import time
import random

#-----------------------------------------------------------------------
# DotStar
#-----------------------------------------------------------------------

"""
This code contains the final functions used in the DotStar class for the
light_saber project. It contains the following functions:

set_pixel_color : Sets the color of one pixel

clear : turns off all of sLED by setting colors to (0, 0, 0)

show : handles communication with sLED via SPI, with start_frame + tuple +
end_frame and uses a brightness multiplier

fill : sets all LEDs to the same color

close : cleanup function for dotstar -> closes SSPI connection

base_color : sets up base color of sLED

"""
class DotStar:
    
    def __init__(self, num_leds, brightness=1.0):
        self.num_leds = num_leds # number of LEDs on DotStar Strip
        self.brightness = max(0.0, min(brightness, 1.0))  # Clamp between 0.0 and 1.0
        self.pixels = [(0, 0, 0)] * num_leds  # RGB tuples

        # Initialize SPI1 on PocketBeagle
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # bus 1, device 0 = SPI1 on PocketBeagle
        self.spi.max_speed_hz = 4000000  # 4 MHz is a safe speed
        self.spi.mode = 0b00

    def set_pixel_color(self, n, r, g, b):
        if 0 <= n < self.num_leds:
            self.pixels[n] = (r, g, b)

    def clear(self):
        self.pixels = [(0, 0, 0)] * self.num_leds
        self.show()

    def show(self):
        start_frame = [0x00] * 4
        end_frame = [0xFF] * ((self.num_leds + 15) // 16)

        led_data = []
        for r, g, b in self.pixels:
            r = int(r * self.brightness)
            g = int(g * self.brightness)
            b = int(b * self.brightness)
            led_data.extend([0xFF, b, g, r])  # DotStar expects BGR + header

        self.spi.xfer2(start_frame + led_data + end_frame)

    def fill(self, r, g, b):
        for i in range(self.num_leds):
            self.set_pixel_color(i, r, g, b)
        self.show()

    def close(self):
        self.spi.close()
        
    def base_color():
        # Returns the baseline color as an RGB tuple
        return (255, 147, 41)  # Example baseline color (orange)