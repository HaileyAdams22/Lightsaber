"""
--------------------------------------------------------------------------
sLED Animations Driver - Lightsaber Project
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
from sLED_DotStar import DotStar


#-----------------------------------------------------------------------
# sLED
#-----------------------------------------------------------------------

""" 
This code contains the final functions used in the sLED class for the 
light_saber project. It contains the following functions:

light_up : animates the sLED to light up from base - UNFINISHED

flicker : flickers sLED around a base color while movement is occuring 
detected by MPU.

flash : flash sLED around a base color when the MPU detects a major 
acceleration change occurs using the interrupt pin.

light_down : animates sLED to turn off from end - UNFINISHED

"""

class Animations:
    
    def __init__(self, led_strip, flicker_active):
        self.led_strip = led_strip
        self.num_leds = led_strip.num_leds
        self.flicker_active = flicker_active

    # Delegate LED functions to DotStar instance
    def set_pixel_color(self, n, r, g, b):
        self.led_strip.set_pixel_color(n, r, g, b)

    def show(self):
        self.led_strip.show()

    def fill(self, r, g, b):
        self.led_strip.fill(r, g, b)
    
    def light_up(self, base_color=lambda: (255, 147, 41), speed=2.0):
        
        
        """
        Lights up the LEDs starting from both the first and last LED and meeting at the middle.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - speed: The speed of the animation (delay between each step).
        """
        r_base, g_base, b_base = base_color()

        # Set up two pointers: one starting at the first LED and one at the last LED
        start = 0
        end = self.num_leds - 1

        # Continue lighting up LEDs until the two pointers meet in the middle
        while start <= end:
            # Turn on LEDs at both the start and end pointers
            self.set_pixel_color(start, r_base, g_base, b_base)
            self.set_pixel_color(end, r_base, g_base, b_base)
           
            # Update the LEDs and move towards the center
            self.show()
            time.sleep(speed)

            # Move the pointers towards the center
            start += 1
            end -= 1
            
    def flicker(self, base_color=lambda: (255, 147, 41), flicker_range=30, speed=0.05, is_active_func=lambda: False):
        self.flicker_active[0] = True  # Signal flicker is starting

        try:
            while is_active_func():
                r_base, g_base, b_base = base_color()
                for i in range(self.num_leds):
                    if not is_active_func():  # Check again mid-loop for faster stop
                        break
                    r = max(0, min(255, r_base + random.randint(-flicker_range, flicker_range)))
                    g = max(0, min(255, g_base + random.randint(-flicker_range, flicker_range)))
                    b = max(0, min(255, b_base + random.randint(-flicker_range, flicker_range)))
                    self.set_pixel_color(i, r, g, b)
                self.show()
                time.sleep(speed)
        finally:
            self.flicker_active[0] = False  # Reset flicker flag when done
        
    
    def flash(self, base_color=lambda: (255, 147, 41), flash_duration=0.1, flash_speed=0.05):
        """
        Turns the LEDs from baseline color to a very quick and bright flash of white, 
        then returns to the original baseline color.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - flash_duration: Time (in seconds) the flash of white will last.
        - flash_speed: Speed at which to perform the transition (controls delay between updates).
        """
    
        # Save the original base color
        r_base, g_base, b_base = base_color()
    
        # Step 1: Set all LEDs to baseline color
        self.fill(r_base, g_base, b_base)
    
        # Step 2: Flash to white (very quick)
        self.fill(255, 255, 255)  # Full white color flash
        time.sleep(flash_duration)  # Duration of the flash
     
        # Step 3: Return to the original baseline color
        self.fill(r_base, g_base, b_base)

    
    def light_down(self, base_color=lambda: (255, 147, 41), speed=2.0):
        """
        Powers down the LEDs starting from the middle LED and turning off LEDs towards both ends.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - speed: The speed of the animation (delay between each step).
        """
        r_base, g_base, b_base = base_color()

        # Set up pointer starting from the middle LED
        middle = self.num_leds // 2  # Always works for odd numbers

        # Continue powering down LEDs until we reach the ends of the strip
        for i in range(middle + 1):
            # Turn off LEDs at positions moving outwards from the middle
            self.set_pixel_color(middle - i, 0, 0, 0)  # Turning off from the middle left
            self.set_pixel_color(middle + i, 0, 0, 0)  # Turning off from the middle right

            # Update the LEDs and pause before the next step
            self.show()
            time.sleep(speed)
