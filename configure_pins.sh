#!/bin/bash
# --------------------------------------------------------------------------
# Light Saber - Configure Pins
# --------------------------------------------------------------------------
# 
# Configure pins for Light Saber project:
#   - I2C2 (MPU6050)
#   - Button 0 & 1
#   - Mini LEDs (bLED, gLED, rLED, wLED)
#   - Strip LED (DotStar)
# 
# --------------------------------------------------------------------------

# I2C2 for MPU6050
echo "Configuring I2C2 (MPU6050)..."
config-pin P1_26 i2c  # SDA
config-pin P1_28 i2c  # SCL

# Buttons
echo "Setting up Button pins..."
config-pin P2_17 gpio
config-pin P2_19 gpio

# mLEDs (bLED, gLED, rLED, wLED)
echo "Setting up mLED GPIO pins..."
config-pin P2_02 out
config-pin P2_04 out
config-pin P2_06 out
config-pin P2_08 out

# sLEDs (DotStar)
echo "Configuring SPI for DotStar..."
config-pin P1_08 spi
config-pin P1_12 spi

echo "All pins configured successfully."
