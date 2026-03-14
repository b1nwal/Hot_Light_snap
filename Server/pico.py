import machine
import socket
import network
import time
import _thread
import onewire, ds18x20

ap = network.WLAN(network.AP_IF)
ap.config(essid='HLS', password='hotlightsnap')
ap.active(True)

class Pico:
    def __init__(self, *, temp_pin,led_pin):
        self.temp_pin = machine.Pin(temp_pin, machine.Pin.IN)
        self.led_pin = machine.Pin(led_pin, machine.Pin.OUT)
        self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(temp_pin)))
        self.d = self.ds.scan()[0]

    def temperature(self):
        return 0

sock = socket.socket()
sock.bind(("192.168.4.1",8080))
sock.listen()

pico = Pico(temp_pin=16,led_pin=15)

def proc_msg(_msg):
    r_flag = True
    msg = _msg.decode('utf-8')
    print(msg)
    if msg=="OP0 EXIT": r_flag = False
    if msg=="OP1 LIGHT_ON": pico.led_pin.value(1) # currently not stateful, this might cause problems later
    if msg=="OP1 LIGHT_OFF": pico.led_pin.value(0)
    return r_flag

def r(sock):
    ret = True
    while ret:
        msg = conn.recv(32)
        ret = proc_msg(msg)
        if not ret: break

while 1: # pico sends periodic updates, always listens for instructions
    conn, addr = sock.accept() # blocks until connection is made
    _thread.start_new_thread(r, (conn,))
    while 1:
        time.sleep(5) # periodic updates
        pico.ds.convert_temp()
        conn.send(bytes(str(pico.ds.read_temp(pico.d)),'utf-8')) # poll temperature
        print('sent')

_thread.start_new_thread(r, (1,))

while 1:
    time.sleep(5)
    conn.send(bytes(str(temp)+'\r\n','utf-8'))
    print("just sent")
    temp += 5