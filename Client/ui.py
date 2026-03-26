from fltk import *

x = 100
y = 100
width = 800
height = 800

TEMP_MIN = 10
TEMP_MAX = 90

class MyWindow(Fl_Window):
    def __init__(self, x, y, w, h, t, controller):
        super().__init__(x,y,w,h,t)
        self.controller = controller
        self.gui = LightGUI(controller)
        self.end()
        self.resizable(self)
        
    def resize(self, x, y, w, h):
        super().resize(x, y, w, h)
        self.layout(w, h)

    def run(self):
        self.show()
        Fl.run()
    def layout(self, w, h):
        self.gui.layout(w,h)
        self.redraw()


class Controller:
    def __init__(self):
        self.lights_on = False
        self.heating_on = False
        self.occupied = False
        self.automated = False
        self.target_temp = 21.0

    def toggle_lights(self):
        self.lights_on = not self.lights_on

    def toggle_heating(self):
        self.heating_on = not self.heating_on

    def change_temp(self, widget): # why is this in LightGUI and not controller?
        temp = widget.value()
        self.target_temp = temp


class LightGUI:
    def __init__(self, controller):

        self.controller = controller
       
        # top header
        self.title_box = Fl_Box(0, 0, 0, 0, "Heating + Lighting Integrated System // System Online")
        self.title_box.box(FL_UP_BOX)
        self.title_box.labelsize(20)

        # second header
        self.overview_box = Fl_Box(0, 0, 0, 0, "Overview")
        self.overview_box.box(FL_UP_BOX)
        self.overview_box.labelsize(25)

        # occupancy box
        self.occupancy_box = Fl_Box(0, 0, 0, 0)
        self.occupancy_box.box(FL_UP_BOX)
        self.occupancy_box.labelsize(20)

        # occupancy box title
        self.occupancy_title = Fl_Box(0, 0, 0, 0, "Occupancy")
        self.occupancy_title.box(FL_FLAT_BOX)
        self.occupancy_title.labelsize(20)

        # occupancy value output
        self.occupancy_value = Fl_Box(0, 0, 0, 0, "NO")
        self.occupancy_value.box(FL_FLAT_BOX)
        self.occupancy_value.labelsize(30)
        self.occupancy_value.labelfont(FL_BOLD)
        #self.occupancy_value.align(FL_ALIGN_CENTRE)

        # occupancy button
        self.occupancy_button = Fl_Button(0, 0, 0, 0, "Toggle Occupancy")
        self.occupancy_button.callback(self.toggle_occupancy)

        # Temperature box
        self.temperature_box = Fl_Box(0, 0, 0, 0)
        self.temperature_box.box(FL_UP_BOX)
        self.temperature_box.labelsize(20)

        # Temperature box title
        self.temperature_title = Fl_Box(0, 0, 0, 0, "Temperature")
        self.temperature_title.box(FL_FLAT_BOX)
        self.temperature_title.labelsize(20)

        # temperature value input
        self.temp_input = Fl_Spinner(0, 0, 0, 0, "")
        self.temp_input.minimum(TEMP_MIN)
        self.temp_input.maximum(TEMP_MAX)
        self.temp_input.step(0.5)
        self.temp_input.value(self.controller.target_temp)
        self.temp_input.callback(self.change_temp)

        # temperature roller
        self.temp_roller = Fl_Roller(0, 0, 0, 0, "")
        self.temp_roller.minimum(TEMP_MIN)
        self.temp_roller.maximum(TEMP_MAX)
        self.temp_roller.step(0.5)
        self.temp_roller.value(self.controller.target_temp)
        self.temp_roller.callback(self.change_temp)

        # temperature value input label (title)
        self.temp_label = Fl_Box(0, 0, 0, 0, "Set Temp:")
        self.temp_label.box(FL_NO_BOX)
        self.temp_label.labelsize(20)
        self.temp_label.align(FL_ALIGN_LEFT | FL_ALIGN_INSIDE)

        # temperature change callback
        self.temp_input.callback(self.change_temp)

        # schedule box
        self.schedule_box = Fl_Box(0, 0, 0, 0)
        self.schedule_box.box(FL_UP_BOX)
        self.schedule_box.labelsize(20)

        # Light schedule title
        self.light_schedule_title = Fl_Box(0, 0, 0, 0, "Lighting Schedule")
        self.light_schedule_title.box(FL_FLAT_BOX)
        self.light_schedule_title.labelsize(20)

        # Temp schedule title
        self.temp_schedule_title = Fl_Box(0, 0, 0, 0, "Boiler Schedule")
        self.temp_schedule_title.box(FL_FLAT_BOX)
        self.temp_schedule_title.labelsize(20)

        # schedule section labels
        self.light_schedule_label = Fl_Box(0, 0, 0, 0, "Lights")
        self.light_schedule_label.box(FL_NO_BOX)
        self.light_schedule_label.labelsize(20)
        self.light_schedule_label.labelfont(FL_BOLD)

        self.temp_schedule_label = Fl_Box(0, 0, 0, 0, "Heating")
        self.temp_schedule_label.box(FL_NO_BOX)
        self.temp_schedule_label.labelsize(20)
        self.temp_schedule_label.labelfont(FL_BOLD)

        self.light_from_label = Fl_Box(0, 0, 0, 0, "From")
        self.light_from_label.box(FL_NO_BOX)

        self.light_to_label = Fl_Box(0, 0, 0, 0, "To")
        self.light_to_label.box(FL_NO_BOX)

        self.temp_from_label = Fl_Box(0, 0, 0, 0, "From")
        self.temp_from_label.box(FL_NO_BOX)

        self.temp_to_label = Fl_Box(0, 0, 0, 0, "To")
        self.temp_to_label.box(FL_NO_BOX)


        # light schedule spinners
        self.light_from_hour = Fl_Spinner(0, 0, 0, 0, "")
        self.light_from_min = Fl_Spinner(0, 0, 0, 0, "")
        self.light_to_hour = Fl_Spinner(0, 0, 0, 0, "")
        self.light_to_min = Fl_Spinner(0, 0, 0, 0, "")

        # temp schedule spinners
        self.temp_from_hour = Fl_Spinner(0, 0, 0, 0, "")
        self.temp_from_min = Fl_Spinner(0, 0, 0, 0, "")
        self.temp_to_hour = Fl_Spinner(0, 0, 0, 0, "")
        self.temp_to_min = Fl_Spinner(0, 0, 0, 0, "")


        # schedule time
        for s in [self.light_from_hour, self.light_to_hour,
                self.temp_from_hour, self.temp_to_hour]:
            s.minimum(0)
            s.maximum(23)
            s.step(1)
            # s.callback(self.update_schedule)

        for k in [self.light_from_min, self.light_to_min,
                self.temp_from_min, self.temp_to_min]:
            k.minimum(0)
            k.maximum(59)
            k.step(1)
            # k.callback(self.update_schedule)

        # default values
        self.light_from_hour.value(2)
        self.light_from_min.value(35)
        self.light_to_hour.value(3)
        self.light_to_min.value(35)

        self.temp_from_hour.value(1)
        self.temp_from_min.value(40)
        self.temp_to_hour.value(5)
        self.temp_to_min.value(59)

        for s in [self.light_from_hour, self.light_from_min,
                self.light_to_hour, self.light_to_min]:
            s.callback(self.update_light_schedule)

        for s in [self.temp_from_hour, self.temp_from_min,
                self.temp_to_hour, self.temp_to_min]:
            s.callback(self.update_temp_schedule)

        self.light_schedule_value = Fl_Box(0, 0, 0, 0, "")
        self.light_schedule_value.box(FL_FLAT_BOX)
        self.light_schedule_value.labelsize(20)
        self.light_schedule_value.labelfont(FL_BOLD)

        self.temp_schedule_value = Fl_Box(0, 0, 0, 0, "")
        self.temp_schedule_value.box(FL_FLAT_BOX)
        self.temp_schedule_value.labelsize(20)
        self.temp_schedule_value.labelfont(FL_BOLD)

        # automated mode box
        self.automation_box = Fl_Box(0, 0, 0, 0)
        self.automation_box.box(FL_UP_BOX)
        self.automation_box.labelsize(20)

        # automation box title
        self.automation_title = Fl_Box(0, 0, 0, 0, "Turn Automated Mode on?")
        self.automation_title.box(FL_FLAT_BOX)
        self.automation_title.labelsize(20)

        # automation checkbox
        self.automation_checkbox = Fl_Check_Button(0, 0, 0, 0)
        self.automation_checkbox.callback(self.toggle_automation)

        # automation label
        self.automation_status = Fl_Box(0, 0, 0, 0, "MANUAL")
        self.automation_status.box(FL_FLAT_BOX)
        self.automation_status.labelsize(20)
        self.automation_status.labelfont(FL_BOLD)

        # manual light box
        self.light_box = Fl_Box(0, 0, 0, 0, "Lights Manual Switch")
        self.light_box.box(FL_UP_BOX)
        self.light_box.labelsize(20)
        
        # manual light button
        self.light_button = Fl_Button(0, 0, 0, 0, "Toggle")
        self.light_button.callback(self.toggle_lights)

        # manual heat box
        self.heat_box = Fl_Box(0, 0, 0, 0, "Heating Manual Switch")
        self.heat_box.box(FL_UP_BOX)
        self.heat_box.labelsize(20)

        # manual heat button
        self.heat_button = Fl_Button(0, 0, 0, 0, "Toggle")
        self.heat_button.callback(self.toggle_heating)

        # clean up title bg if i choose to do so

        self.layout(width, height)
        self.update_occupancy()
        self.update_automation()
        self.update_light_schedule(None)
        self.update_temp_schedule(None)


    def layout(self, w, h):
        # headers
        self.title_box.resize(int(0), int(0), int(w), int(h*0.1))
        self.overview_box.resize(int(0), int(h*0.1), int(w), int(h*0.15))

        # info boxes
        self.occupancy_box.resize(int(w*0.025), int(h*0.3), int(w*0.225), int(h*0.3))
        self.temperature_box.resize(int(w*0.275), int(h*0.3), int(w*0.275), int(h*0.3))
        self.schedule_box.resize(int(w*0.575), int(h*0.3), int(w*0.4), int(h*0.5))
        self.automation_box.resize(int(w*0.575), int(h*0.825), int(w*0.4), int(h*0.125))

        # titles
        self.occupancy_title.resize(int(w*0.13), int(h*0.35), int(w*0), int(h*0))
        self.temperature_title.resize(int(w*0.415), int(h*0.35), int(w*0), int(h*0))
        self.automation_title.resize(int(w*0.75), int(h*0.85), int(w*0), int(h*0))
        self.light_schedule_title.resize(int(w*0.7), int(h*0.35), int(w*0), (h*0))
        self.temp_schedule_title.resize(int(w*0.7), int(h*0.55), int(w*0), int(h*0))
 
        # light components 
        self.light_box.resize(int(w*0.025), int(h*0.65), int(w*0.525), int(h*0.125))
        self.light_button.resize(int(w*0.4), int(h*0.675), int(w*0.125), int(h*0.075))

        # heat components
        self.heat_box.resize(int(w*0.025), int(h*0.825), int(w*0.525), int(h*0.125))
        self.heat_button.resize(int(w*0.4), int(h*0.85), int(w*0.125), int(h*0.075))

        # heat inputs
        self.temp_input.resize(int(w*0.3), int(h*0.45), int(w*0.2), int(h*0.1))
        self.temp_roller.resize(int(w*0.51), int(h*0.45), int(w*0.03), int(h*0.1))
        self.temp_label.resize(int(w*0.3), int(h*0.43), int(w*0), int(h*0))

        # schedule inputs light
        self.light_from_label.resize(int(w*0.58), int(h*0.4), int(w*0.0645), int(h*0.05))
        self.light_from_hour.resize(int(w*0.6445), int(h*0.4), int(w*0.0645), int(h*0.05))
        self.light_from_min.resize(int(w*0.709), int(h*0.4), int(w*0.0645), int(h*0.05))
        self.light_to_label.resize(int(w*0.7735), int(h*0.4), int(w*0.0645), int(h*0.05))
        self.light_to_hour.resize(int(w*0.838), int(h*0.4), int(w*0.0645), int(h*0.05))
        self.light_to_min.resize(int(w*0.9025), int(h*0.4), int(w*0.0645), int(h*0.05))

        self.light_schedule_value.resize(int(w*0.67), int(h*0.46), int(w*0.25), int(h*0.05))

        #schedule inputs temperature
        self.temp_from_label.resize(int(w*0.58), int(h*0.6), int(w*0.0645), int(h*0.05))
        self.temp_from_hour.resize(int(w*0.6445), int(h*0.6), int(w*0.0645), int(h*0.05))
        self.temp_from_min.resize(int(w*0.709), int(h*0.6), int(w*0.0645), int(h*0.05))
        self.temp_to_label.resize(int(w*0.7735), int(h*0.6), int(w*0.0645), int(h*0.05))
        self.temp_to_hour.resize(int(w*0.838), int(h*0.6), int(w*0.0645), int(h*0.05))
        self.temp_to_min.resize(int(w*0.9025), int(h*0.6), int(w*0.0645), int(h*0.05))


        self.temp_schedule_value.resize(int(w*0.67), int(h*0.66), int(w*0.25), int(h*0.05))

        # occupancy components
        self.occupancy_value.resize(int(w*0.06), int(h*0.4), int(w*0.15), int(h*0.1))
        self.occupancy_button.resize(int(w*0.05), int(h*0.55), int(w*0.18), int(h*0.05))

        # automation components
        self.automation_checkbox.resize(int(w*0.65), int(h*0.884), int(w*0.02), int(h*0.025))
        self.automation_status.resize(int(w*0.7), int(h*0.87), int(w*0.15), int(h*0.05))

    def update_occupancy(self):
        if self.controller.occupied:
            self.occupancy_value.label("YES")
            #self.occupancy_value.labelcolor(FL_GREEN)
        else:
            self.occupancy_value.label("NO")
            #self.occupancy_value.labelcolor(FL_RED)

        self.occupancy_value.redraw()

    def toggle_occupancy(self, widget):
        self.controller.occupied = not self.controller.occupied #senor_value
        self.update_occupancy()

    def update_automation(self):
        if self.controller.automated:
            self.automation_status.label("AUTOMATED")
            #self.automation_status.labelcolor(FL_GREEN)
        else:
            self.automation_status.label("MANUAL")
            #self.automation_status.labelcolor(FL_RED)

        self.automation_status.redraw()

    def toggle_automation(self, widget):
        self.controller.automated = bool(widget.value())
        self.update_automation()

    def toggle_lights(self, widget):
        self.controller.automated = False
        self.automation_checkbox.value(0)
        self.update_automation()

        self.controller.toggle_lights()

        if self.controller.lights_on:
            self.light_box.label("Lights ON")
            self.light_box.color(FL_YELLOW)
        else:
            self.light_box.label("Lights OFF")
            self.light_box.color(FL_GRAY)

        self.light_box.redraw()


    def toggle_heating(self, widget):
        self.controller.automated = False
        self.automation_checkbox.value(0)
        self.update_automation()

        self.controller.toggle_heating()

        if self.controller.heating_on:
            self.heat_box.label("Heating ON")
            self.heat_box.color(fl_rgb_color(255, 154, 0))
        else:
            self.heat_box.label("Heating OFF")
            self.heat_box.color(FL_GRAY)

        self.heat_box.redraw()

    def change_temp(self, widget): # why is this in LightGUI and not controller?
        temp = widget.value()
        self.controller.target_temp = temp
        self.temp_input.value(temp)
        self.temp_roller.value(temp)


    def update_light_schedule(self, widget):
        fh = int(self.light_from_hour.value())
        fm = int(self.light_from_min.value())
        th = int(self.light_to_hour.value())
        tm = int(self.light_to_min.value())
        self.light_schedule_value.label(f"{fh:02d}:{fm:02d} to {th:02d}:{tm:02d}")

        start_total = fh * 60 + fm
        end_total = th * 60 + tm

        if end_total <= start_total:
            self.light_schedule_value.label("Invalid time range")
            self.light_schedule_value.labelcolor(FL_RED)
        else:
            self.light_schedule_value.label(f"{fh:02d}:{fm:02d} to {th:02d}:{tm:02d}")
            self.light_schedule_value.labelcolor(FL_BLACK)

        self.light_schedule_value.redraw()

    def update_temp_schedule(self, widget):
        fh = int(self.temp_from_hour.value())
        fm = int(self.temp_from_min.value())
        th = int(self.temp_to_hour.value())
        tm = int(self.temp_to_min.value())
        self.temp_schedule_value.label(f"{fh:02d}:{fm:02d} to {th:02d}:{tm:02d}")

        start_total = fh * 60 + fm
        end_total = th * 60 + tm

        if end_total <= start_total:
            self.temp_schedule_value.label("Invalid time range")
            self.temp_schedule_value.labelcolor(FL_RED)
        else:
            self.temp_schedule_value.label(f"{fh:02d}:{fm:02d} to {th:02d}:{tm:02d}")
            self.temp_schedule_value.labelcolor(FL_BLACK)

        self.temp_schedule_value.redraw()


if __name__ == "__main__":

    controller = Controller()
    win = MyWindow(x, y, width, height, "LED Control", controller)
    win.run()
