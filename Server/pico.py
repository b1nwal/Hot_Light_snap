import machine
import socket
import network
import onewire, ds18x20
import time
import _thread

ap = network.WLAN(network.AP_IF)
ap.config(essid='HLS', password='hotlightsnap')
ap.active(True)

class Pico:
    def __init__(self, *, temp_pin,led_pin):
        self.temp_pin = machine.Pin(temp_pin, machine.Pin.IN)
        self.led_pin = machine.Pin(led_pin, machine.Pin.OUT)
        self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(temp_pin)))
        self.d = self.ds.scan()[0]
        self.temp = 0

    def temperature(self):
        pico.ds.convert_temp()
        self.temp = str("OP2 " + pico.ds.read_temp(pico.d))
        return self.temp

sock = socket.socket()
sock.bind(("192.168.4.1",8080))
sock.listen()

pico = Pico(temp_pin=16,led_pin=15)

def proc_msg(_msg):
    r_flag = True
    msg = _msg.decode('utf-8')
    print(msg)
    if "OP0" in msg: # bi-directional exit
        r_flag = False
    elif "OP1" in msg: # simplex command
        if "LIGHT_ON" in msg:
            pico.led_pin.value(1) # currently not stateful, this might cause problems later
        elif "LIGHT_OFF" in msg:
            pico.led_pin.value(0)
    elif "OP2" in msg: # duplex command (send answer form here, question form on ui)
        if "TEMP?" in msg:
            conn.send(bytes(pico.temperature(),'utf-8'))
    return r_flag

def control_loop(_):
    while 1:
        time.sleep(1)
        pico.temperature()

while 1: # pico sends periodic updates, always listens for instructions
    conn, addr = sock.accept() # blocks until connection is made
    ret = True
    t = _thread.start_new_thread(control_loop, (1,))
    while ret:
        msg = conn.recv(32)
        ret = proc_msg(msg)
        if not ret: 
            t.exit()
            break