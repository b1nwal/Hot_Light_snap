import machine
import socket
import network
import onewire, ds18x20
import time
import _thread

HOST="192.168.4.1"
PORT=8080

HC_HEAT_DEFAULT=40.0 #adjust default target temp here (make sure it aligns with control software?)
HC_BAND_DEFAULT=5.0
HC_S_OFFSET=5.0

ap=network.WLAN(network.AP_IF)
ap.config(essid='HLS',password='hotlightsnap')
ap.active(True)

class PI: #use this for lux later
    def __init__(self,p_k,i_k,target):
        self.p_k=p_k
        self.i_k=i_k
        self.target=target
        self.r=0
        self.e=0
        self.accumulator=0
    def update(self,deltaT):
        self.e=self.target-self.r
        self.accumulator+=deltaT*self.e
        a = min(65535, max(0,int(self.e*self.p_k+self.i_k*self.accumulator)))
        return a

class Pico:
    def __init__(self,*,temp_pin,led_pin,pir_pin,lux_pin,heat_pin):
        self.temp_pin=machine.Pin(temp_pin,machine.Pin.IN)
        self.led_pin=machine.Pin(led_pin,machine.Pin.OUT)
        self.pir_pin=machine.Pin(pir_pin,machine.Pin.IN)
        self.lux_pin=machine.ADC(lux_pin)
        self.heat_pin=machine.Pin(heat_pin,machine.Pin.OUT)
        self.heat_pin.value(1)
        self.ds=ds18x20.DS18X20(onewire.OneWire(machine.Pin(temp_pin)))
        self.d=self.ds.scan()[0]
        self.temp=0
        self.heater=self._Heater(self)
        self.pir=self._PIR(self.pir_pin)
        self.lux=self._Lux(self.lux_pin)
        self.led_pwm=machine.PWM(self.led_pin)
        self.led_pwm.freq(1000)
        self.led_pwm.duty_u16(0)
        self.led_brightness=0
        self.occ = False #This is actually just whether or not the PIR sensor is *currently* detecting motion. The definition below is for whether or not it actually believes someone is in the room.
        self.occ_guess=False #I know it's confusing, I'm sorry!
        self.automode=False
        self.lighting_controller = PI(0.75, 0, 29535)
    #mini-class definitions here
    class _PIR:
        def __init__(self,pin):
            self.dead_time=0
            self.pin=pin
        def get_current(self):
            v=self.pin.value()
            if v==0:self.dead_time+=1
            else:self.dead_time=0
            return (v==1)
    class _Heater: #little mini-class as a helper
        def __init__(self,pico):
            self.state=False
            self.target=HC_HEAT_DEFAULT
            self.band=HC_BAND_DEFAULT
            self.pico=pico
        def update(self): #hysteresis-based control approach (easily swappable, of course)
            self.current=self.pico.temp #don't bother updating, it should already be updated by now
            if self.current>self.target-self.band:
                self.turn_off()
            elif self.current<self.target-self.band:
                self.turn_on()
        def toggle_state(self):
            self.state=not self.state
        def turn_on(self):
            self.state=True
            self.pico.heat_pin.value(0)
        def turn_off(self):
            self.state=False
            self.pico.heat_pin.value(1)
    class _Lux:
        def __init__(self, pin):
            self.pin = pin
        def read(self):
            return 65535-self.pin.read_u16()
    #class functions defined here
    def temperature(self):
        pico.ds.convert_temp()
        self.temp=pico.ds.read_temp(pico.d)
        return self.temp
    def occupancy(self):
        self.occ=self.pir.get_current()
        return self.occ

def send(conn,t): # small helper function
    conn.send(bytes(t,'utf-8'))

### OPCODE DOCUMENTATION
#   OP0 : ENTER/EXIT
#   OP1 : SIMPLEX COMMAND
#   OP2 : DUPLEX COMMAND (QUESTION AND RESPONSE) 

def proc_msg(_msg,conn): 
    r_flag=True
    msg=_msg.decode('utf-8')
    # print("recv:",msg)
    if not msg: r_flag=False #catastrophic exit
    if "OP0" in msg:
        if "ENTER" in msg:
            send(conn,"OP0 ENTER")
        elif "EXIT" in msg:
            r_flag=False
    elif "OP1" in msg: #simplex command
        if "LIGHT_ON" in msg:
            pico.led_brightness=65535 # this may be changed later to ack system to prevent misalignment
            pico.led_pwm.duty_u16(pico.led_brightness)
        elif "LIGHT_OFF" in msg:
            pico.led_brightness=0 # this may be changed later to ack system to prevent misalignment
            pico.led_pwm.duty_u16(pico.led_brightness)
        elif "TEMP_SET" in msg:
            pico.heater.target = float(msg[13:])
        elif "AUTO_ON" in msg:
            pico.automode = True
        elif "AUTO_OFF" in msg:
            pico.automode = False
        elif "HEAT_ON" in msg:
            pico.heater.turn_on()
        elif "HEAT_OFF" in msg:
            pico.heater.turn_off()
    elif "OP2" in msg: #duplex command (send answer form here, question form on ui)
        if "TEMP?" in msg:
            send(conn,"OP2 TEMP "+str(pico.temperature())) #basically just shorthand for calling pico.temperature() on the line above and using pico.temp here
        elif "OCC?" in msg:
            send(conn,"OP2 OCC "+str(pico.occ_guess)) #occ_guess should be constantly updated anyway, but technically for symmetry I guess I should have a function for updating it?
            print(pico.occ_guess)
        elif "TEMP_TARGET?" in msg:
            send(conn, "OP2 TEMP_TARGET "+str(pico.heater.target))
        elif "AUTO?" in msg:
            send(conn,"OP2 AUTO "+str(pico.automode))
        elif "LIGHT_STAT?" in msg:
            send(conn,"OP2 LIGHT_STAT "+str(("OFF" if pico.led_brightness==0 else "ON")))
        elif "HEAT_STAT?" in msg:
            send(conn, "OP2 HEAT_STAT "+str(("ON" if pico.heater.state else "OFF")))
    return r_flag

def _control_loop(pico): #use the pico state to update the pico state on a loop
    while 1:
        time.sleep(1)
        #occupancy checking happens here
        pico.occupancy() #updates PIR state intrinsically. this is the ONLY place that should ever update the PIR state
        if pico.pir.dead_time>=30 and pico.occ_guess: #if it has been silent for 30 consecutive seconds (and we currently estimate the room is occupied)
            pico.occ_guess=False #update that assumption because it's probably wrong
            pico.heater.target -= HC_S_OFFSET
        if not pico.occ_guess and pico.occ:
            pico.heater.target += HC_S_OFFSET
            pico.occ_guess=True #if the PIR *ever* detects movement, it means the room is occupied (this logic might need to be changed to implement a live-time, tee hee)
        #heater logic happens here
        pico.temperature() #update pico internal temp

        if pico.automode:
            pico.heater.update() #apply control loop logic
            #lights logic happens here
            pico.lighting_controller.r = pico.lux.read()
            pico.led_brightness=pico.lighting_controller.update(1)
            pico.led_pwm.duty_u16(pico.led_brightness)

sock=socket.socket()
sock.bind((HOST,PORT))
sock.listen()

print("Pico active and listening at: {HOST}:{PORT}".format(HOST=HOST,PORT=PORT))

pico=Pico(temp_pin=0,led_pin=10,pir_pin=2,lux_pin=2,heat_pin=26)
control_loop=_thread.start_new_thread(_control_loop,(pico,))

while 1: #pico sends periodic updates, always listens for instructions
    conn,addr=sock.accept() #blocks until connection is made
    ret=True
    while ret:
        msg=conn.recv(32)
        ret=proc_msg(msg,conn)
        if not ret:
            break