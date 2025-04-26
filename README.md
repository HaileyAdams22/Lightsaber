# Lightsaber
EDES301 Lightsaber Project

The files in this repository contain code required to run the different functions of a lightsaber. The link to the Hackster page describing the Porject is here:

There are 9 files in this repository and are outlined below

configure_pin.sh : This file is not required to run the lightsaber code yet, but can be used to configure the appropriate pins of the PocketBeagle in the hardware so they can be interfaced digitally through python.

int_class.py : This python script is a class for the Interrupt pin of the MPU used in this project. It is similar to the mpu6050 script. It measures data from the IMU and can detects the motion and impact of the lightsaber. It is used in the main driver to trigger a flicker animation.

lightsaber.py : This python script is the main driver for the lightsaber project. It uses all other drivers (which include classes) to direct classes, objects, animations and behaviors of the lightsaber. This script calls functions from other drivers and heavily relies on threaded logic.

mLED.py : This python script is a class for the mini LEDs used in the handle of the ligthsaber. 4 mLEDs are included in the lightsaber design to indicate what color the sLED will be when turned on.

mpu6050_class.py : This python script is a class for the IMU used in this project. It measures data from the IMU and can detects the motion and impact of the lightsaber. It is used in the main driver to trigger a flicker animation.

run_lightsaber.txt : This file is not required to run the lightsaber code yet, but can be used to run the Lightsaber software on boot of the PocketBeagle.

sLED_Animations.py : This python script defines all functions that produce the animations for the sLED. This includes a flicker, flash, light_up, light_down animation. They are all used in the main driver. 

sLED_DotStar.py : This python script defines simple sLED functions that can set pixle colors, clear the strip, communicate with the PocketBeagle through the SPI interface, fill the sLED with a specific color, establish a base color, and close the communication line with the SPI interface.

threaded_button : This python script defines the simple functions for threaded buttons, mainly in calculating the press times to be used as triggers for animations.
