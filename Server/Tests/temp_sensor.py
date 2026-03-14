import machine
import time
import onewire, ds18x20

dat = machine.Pin(16)
ds = ds18x20.DS18X20(onewire.OneWire(dat))
d = ds.scan()[0]
while 1:
    ds.convert_temp()
    time.sleep(.2)
    print(ds.read_temp(d))
