from fltk import *
import socket
import threading

x = 100
y = 100
width = 1000
height = 1000

temp = 0

def r(gui, cont):
    while 1:
        msg = cont.socket.recv(1024).decode('utf-8')
        print(msg)
        global temp
        temp = msg

class Controller:

    def __init__(self, socket):
        self.lights_on = False
        self.heating_on = False
        self.socket = socket
    def toggle_lights(self):
        self.lights_on = not self.lights_on
        # self.socket.send(b'OP1 LIGHT_'+(b'ON' if self.lights_on else b'OFF'))

    def toggle_heating(self):
        self.heating_on = not self.heating_on


class LightGUI:

    def __init__(self, controller):

        self.controller = controller
        
        # window
        self.window = Fl_Window(x, y, width, height, "LED Control")
        
        # top header
        self.title_box = Fl_Box(int(0), int(0), int(width), int(height*0.1), "Heating + Lighting Integrated System // System Online")
        self.title_box.box(FL_UP_BOX)
        self.title_box.labelsize(20)

        # second header
        self.overview_box = Fl_Box(int(0), int(height*0.1), int(width), int(height*0.15), "Overview")
        self.overview_box.box(FL_UP_BOX)
        self.overview_box.labelsize(25)

        # occupancy checker
        self.occupancy_box = Fl_Box(int(width*0.025), int(height*0.3), int(width*0.225), int(height*0.3), "Occupancy")
        self.occupancy_box.box(FL_UP_BOX)
        self.occupancy_box.labelsize(20)

        # Temperature metre
        self.temperature_box = Fl_Box(int(width*0.275), int(height*0.3), int(width*0.275), int(height*0.3), "Temperature: ")
        self.temperature_box.box(FL_UP_BOX)
        self.temperature_box.labelsize(20)


        #manual light box
        self.light_box = Fl_Box(int(width*0.025), int(height*0.65), int(width*0.525), int(height*0.125), "Lights Manual Switch")
        self.light_box.box(FL_UP_BOX)
        self.light_box.labelsize(20)

        
        # manual light button
        self.light_button = Fl_Button(int(width*0.4), int(height*0.675), int(width*0.125), int(height*0.075), "Toggle")
        self.light_button.callback(self.toggle_lights)

        # manual heat box
        self.heat_box = Fl_Box(int(width*0.025), int(height*0.825), int(width*0.525), int(height*0.125), "Heating Manual Switch")
        self.heat_box.box(FL_UP_BOX)
        self.heat_box.labelsize(20)

        # manual heat button
        self.heat_button = Fl_Button(int(width*0.4), int(height*0.85), int(width*0.125), int(height*0.075), "Toggle")
        self.heat_button.callback(self.toggle_heating)

        self.window.end()


    def toggle_lights(self, widget):
        global temp
        temp = ""

        self.temperature_box = Fl_Box(int(width*0.275), int(height*0.3), int(width*0.275), int(height*0.3), "Temperature: "+temp)

        self.controller.toggle_lights()

        if self.controller.lights_on:
            self.light_box.label("Lights ON")
            self.light_box.color(FL_YELLOW)
        else:
            self.light_box.label("Lights OFF")
            self.light_box.color(FL_GRAY)

        self.light_box.redraw()


    def toggle_heating(self, widget):
        self.controller.toggle_heating()

        if self.controller.heating_on:
            self.heat_box.label("Heating ON")
            self.heat_box.color(FL_YELLOW)
        else:
            self.heat_box.label("Heating OFF")
            self.heat_box.color(FL_GRAY)

        self.heat_box.redraw()


    def run(self):

        self.window.show()
        Fl.run()


if __name__ == "__main__":
    sock = socket.socket()
    # sock.connect(("192.168.4.1", 8080))

    controller = Controller(sock)

    gui = LightGUI(controller)
    # t = threading.Thread(target=r, args=(gui,controller))
    # t.start()

    gui.run()
