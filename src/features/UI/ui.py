from features.UI.Encoder.encoder import RotaryEncoder
from features.UI.LCD.lcd import MyLCD

from features.devices.air.dht11 import DHT11
from features.devices.light.insolation_sensor import InsolationSensor
from features.devices.soil_humidity.soil_moisture_sensor import PlantState
import uasyncio



class Screen:
    def __init__(self, title, values, global_state= None, state=None):
        self.values = values
        self.title = title
        self.state = state
        self.global_state = global_state
        
        
    def __eq__(self, other):
        if isinstance(other, Screen):
            return self.title == other.title
        return False
        
    def __repr__(self):
        return f"{self.title}"

class UI:
    def __init__(self, encoder: RotaryEncoder, lcd: MyLCD, devices: []):
        self._encoder = encoder
        self._lcd = lcd
        self._devices = devices

        self._manual_mode = False
        self._current_screen = 0
        self._prev_device = 0
       

        self._dht: DHT11 = None
        self._light: InsolationSensor = None
        self._soil_devices = []
        self._screens = []

        for dev in devices:
            if dev.config.type == "air":
                self._dht = dev
            elif dev.config.type == "light":
                self._light = dev
            else:
                self._soil_devices.append(dev)

        self._screen_count = len(self._soil_devices) + 1
        
    async def loop(self):
       pressed = False
       screen = None
       while True:
            if self._encoder.is_button_pressed():
                if pressed == False:
                    self._manual_mode = not self._manual_mode
                    if self._manual_mode:
                        screen = await self.create_screen()
                        self._encoder.update_prev_rot(self._encoder.get_current_rot())
                        
                pressed = True
            else:
                pressed = False

            # if manual mode on, then check rotations
            if(self._manual_mode):
                val_new = self._encoder.get_current_rot()
                val_old = self._encoder.get_prev_rot()


                # setting device to display
                if val_new > val_old:
                    self._current_screen = (self._current_screen + 1) % self._screen_count

                if val_new < val_old:
                    self._current_screen = (self._current_screen - 1) % self._screen_count
                

                if val_new != val_old:
                    self._encoder.update_prev_rot(val_new)
                    screen = await self.create_screen()

                print(screen)
            

                
            await uasyncio.sleep_ms(500)
    

    

    async def create_screen(self):
        glob_state = ""
        
        for dev in self._soil_devices:
            state = await dev.get_plant_state() 
            if  state == PlantState.DRY_WARNING:
                glob_state = "!"
            else:
                glob_state = ""
            
        if self._current_screen == 0:

            temp = await self._dht.get_temperature()
            hum = await self._dht.get_humidity()

            light = await self._light.get_insolation()
            
            sc = self.find_screen("home")
            if sc is not None:
                sc.vals = [temp, hum, light]
                sc.global_state = global_state
                return sc
            
            sc = Screen("Home", [temp, hum, light], global_state=glob_state)
            self._screens.append(sc)
            return sc
        else:
            dev = self._soil_devices[self._current_screen - 1]
            moisture =  await dev.get_moisture()
            state =     await dev.get_plant_state()
        
            title = f"SMS: {dev.config.id}"
        
            sc = self.find_screen(title)
            if sc is not None:
                sc.vals = [moisture]
                sc.global_state = glob_state
                sc.state = state
                return sc
            
            sc = Screen(title, [moisture], glob_state, state)
            self._screens.append(sc)
            return sc
        
    def find_screen(self, title):
        for s in self._screens:
            if s.title == title:
                return s
        return None
