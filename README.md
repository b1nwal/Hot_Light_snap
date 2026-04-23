# Hot Light snap
## Summary
This is a demo prototype project for an integrated heating/lighting building management system (hereafter **BMS**) developed by Spiders Georg (engineering design team.) The assignment was to create a project that addressed an RFP submitted by UVic facilities management to integrate building systems (such as security, fire, heating, lighting, water, etc.) into a single BMS that would enable relative ease in controlling and administartion, as well as modular expandability for future upgrades. 

## Technical Description 
This project integrates heating and lighting, utilizing closed-loop feedback control systems (hysteresis-based for heating, PI for lighting,) and an API-first design philosophy intended to enable maximum customizability and programmability. The demo prototype uses a Raspberry Pi Pico W in access point mode, which hosts a server that exposes an API for essential building management tasks and queries. The frontend software packaged in this repo is an example of what frontend software could look like, in this case implemented in Python with PyFLTK.

HLS is an integrated heating and lighting systems prototype device that responds to changes in room occupancy and environment utilizing the following components: 
- Raspberry Pi Pico W 
- PIR motion sensor 
- Waterproof temperature sensor 
- Photoresistor 
- LEDs 
- Active heating element (Electric Kettle) 
- Relay 

Room occupancy is monitored with a PIR sensor device to monitor movement. Heat is monitored with a digital temperature sensor, and illuminance is monitored with a lux sensor. Device uses a Proportional-Integral control system to create a closed feedback loop which monitors and maintains target illuminance with minimal error.  A hysteresis based design is used to control heat: If the current temperature is above the target temperature and not within the tolerance band, switch the heat off. If below, switch on. For prototyping and demonstration purposes, a room full of air is represented by a container filled with water. The purpose of this substitution is purely demonstrational clarity: water heats smoother and more uniformly, so it will be easier to see the control system establish and maintain temperature. To heat water, an electric heating element is used. This element is powered by 120 Volt AC mains electricity, which is gated by a high-current rated relay. When room occupancy sensors detect that room is unoccupied for 30 consecutive seconds (adjustable), target temperature can be annealed by a user-specified amount over a user-specified period to conserve power. The lighting system utilizes power efficient pulse-width modulated LED lighting to create adaptable lighting. The device responds to room occupancy and ambient temperature. Lights are dimmed significantly when a room is unoccupied, and individual light levels are adjusted to reach a target illuminance level, factoring in ambient light (this practice is called 'daylight harvesting'). 

The system is API-first and decoupled from the backend, enabling multiple, custom, or no interface. This means that the server only sends raw plain text data back to the client in response to a command. The client is responsible for presenting this information. As a result, customizability is only limited by the actual capabilities of the device. Commands are designated as Connection updates (OP0), Simplex (one way) commands (OP1), or Duplex (two way) commands (OP2).  

## Description of Control systems
The lighting control is handled by a PI controller. This functions by adjusting the light level in direct proportion to the error (light level – target light level) and keeping track of the steady state error with an integrator to push it to zero. In this way, the light level quickly evens out to a predetermined target level without significant flickering or adjustment time, and this type of controller keeps up well with both slow (sun position over the course of the day) and fast (cloud blocking the sun, etc.) changes in environmental light. It is important that this system uses a feedback loop; The lights in the room contribute to the overall illuminance and must be considered as well. 

## Testing
Testing was conducted primarily for testing sensor function and network connectivity. By sending a particular coded message to the Pico server API Layer, you can confirm you have established a mutual connection and the pico is waiting for commands. Similar testing was conducted to confirm that the Pico could retrieve, store, and send sensor data in response to commands. Finally, a very important series of tests regarding reliable remote control of the relay commanding 1100 Watts of mains electricity going into the element was conducted. These tests very thoroughly examined each edge case (disconnecting during or after message send, automatic mode override, temperature target shift) in order to ensure that there could be no dangerous situations like uncontrolled, rapidly increasing temperatures where a zombied connection exists, not capable of immediately disconnecting the heater if the device is in manual mode. 

## Contributors
Reilley Pfrimmer  
M. H.
