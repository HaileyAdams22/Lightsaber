import time
import sys
import threading

from led import LED
from threaded_button import ThreadedButton
from sLED_DotStar import DotStar
from sLED_Animations import Animations
from mpu6050_class import MPU6050
from int_class import INT_PIN

# -----------------------------
# Pin assignments and globals
# -----------------------------
led_pins = ["P2_2", "P2_4", "P2_6", "P2_8"]
button_pin = "P2_19"
leds = [LED(pin) for pin in led_pins]
current_index = [0]
first_press = [True]
sLED_active = [False]  # <-- changed to mutable
flicker_active = [False]

# -----------------------------
# sLED and animation setup
# -----------------------------
sLED = DotStar(num_leds=108, brightness=0.8)
sLED.clear()
led_colors = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 255)
]
for led in leds:
    led.off()

animations = Animations(sLED, flicker_active)
mpu = MPU6050()
int_pin = INT_PIN()
int_pin.configure_motion_detection(threshold=0x20, duration=0x01)  # Configurable here

# -----------------------------
# Button logic
# -----------------------------
def handle_button_release():
    press_duration = button.get_last_press_duration()

    if press_duration >= 2.0:
        print("Long press detected!")

        if sLED_active[0]:
            print("Turning off sLED...")
            flicker_active[0] = False
            time.sleep(0.1)
            animations.light_down(base_color=lambda: led_colors[current_index[0]], speed=0.01)
            sLED_active[0] = False
        else:
            print("Activating sLED...")
            r, g, b = led_colors[current_index[0]]
            animations.light_up(base_color=lambda: (r, g, b), speed=0.01)
            sLED_active[0] = True

        leds[current_index[0]].on()
    else:
        print(f"Short press ({press_duration:.2f}s) - cycling mLED")

        if first_press[0]:
            leds[current_index[0]].on()
            first_press[0] = False
        else:
            leds[current_index[0]].off()
            current_index[0] = (current_index[0] + 1) % len(leds)
            leds[current_index[0]].on()

        if sLED_active[0]:
            r, g, b = led_colors[current_index[0]]
            sLED.fill(r, g, b)

# -----------------------------
# Flicker thread launcher
# -----------------------------
def start_flicker_thread():
    flicker_thread = threading.Thread(
        target=animations.flicker,
        kwargs={
            "base_color": lambda: led_colors[current_index[0]],
            "flicker_range": 30,
            "speed": 0.05,
            "is_active_func": lambda: sLED_active[0] and flicker_active[0]
        },
        daemon=True
    )
    flicker_thread.start()

# -----------------------------
# Motion detection logic
# -----------------------------
def detect_motion_and_flicker():
    motion_history = []
    stop_motion_history = []
    stop_history_len = max_history_len * 10

    while True:
        if sLED_active[0]:
            sensor_data = mpu.get_sensor_data()
            current_motion = sensor_data["comb_accel_gyro"]

            motion_history.append(current_motion)
            if len(motion_history) > max_history_len:
                motion_history.pop(0)

            avg_motion = sum(motion_history) / len(motion_history)

            if avg_motion > motion_threshold and not flicker_active[0]:
                print(f"Motion detected! Avg: {avg_motion:.2f} | Starting flicker...")
                flicker_active[0] = True
                start_flicker_thread()

            elif avg_motion <= motion_threshold and flicker_active[0]:
                stop_motion_history.append(avg_motion)
                if len(stop_motion_history) > stop_history_len:
                    stop_motion_history.pop(0)

                stop_avg = sum(stop_motion_history) / len(stop_motion_history)

                if stop_avg <= motion_threshold:
                    print(f"Sustained calm motion. Stopping flicker. Avg: {stop_avg:.2f}")
                    flicker_active[0] = False
                    sLED.fill(*led_colors[current_index[0]])
                    sLED.show()
                    stop_motion_history.clear()
            else:
                stop_motion_history.clear()

        time.sleep(0.05)

# -----------------------------
# Interrupt detection logic
# -----------------------------
def interrupt_flash_thread():
    flash_cooldown = 1.0
    last_flash_time = 0

    while True:
        if sLED_active[0] and int_pin.check_interrupt():
            current_time = time.time()
            if current_time - last_flash_time >= flash_cooldown:
                print("Interrupt: Sudden motion detected! Flashing white.")
                animations.flash(
                    base_color=lambda: led_colors[current_index[0]],
                    flash_duration=0.1,
                    flash_speed=0.01
                )
                last_flash_time = current_time
                int_pin.clear_interrupt()
        time.sleep(0.05)

# -----------------------------
# Setup and run
# -----------------------------
motion_threshold = 2.0
cooldown_period = 0.5
max_history_len = 5

button = ThreadedButton(pin=button_pin, sleep_time=0.05)
button.set_on_release_callback(handle_button_release)
button.start()

motion_thread = threading.Thread(target=detect_motion_and_flicker, daemon=True)
motion_thread.start()

interrupt_thread = threading.Thread(target=interrupt_flash_thread, daemon=True)
interrupt_thread.start()

print("Press Button 1 to cycle through LEDs. Press Ctrl-C to exit.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    button.cleanup()
    for led in leds:
        led.cleanup()
    sLED.clear()
    sLED.close()
