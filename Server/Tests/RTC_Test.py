from machine import I2C, Pin
from ds1307 import DS1307
import time

# I2C pins for Raspberry Pi Pico (adjust pins as needed for your board)
i2c = I2C(0, scl=Pin(2), sda=Pin(1), freq=100000) #

# DS1307 I2C address is 0x68 (104 decimal)
ds1307 = DS1307(addr=0x68, i2c=i2c)

# --- Set the time ---
# Get current time from the host system (if available) or define it manually
# Time format is a 7-tuple: (year, month, day, hour, minute, second, weekday)
# Weekday is 0-6 (e.g., Monday=0)
now = time.gmtime(time.time())
ds1307.datetime = (now[0], now[1], now[2], now[3], now[4], now[5], now[6]) #

# --- Get and print the time ---
current_time = ds1307.datetime
print("Current time is: {:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(
    current_time[0], current_time[1], current_time[2],
    current_time[3], current_time[4], current_time[5])) #
