from features.UI.Encoder.encoder import RotaryEncoder
from features.UI.LCD.lcd import MyLCD
import uasyncio


class UI:
    def __init__(self, encoder: RotaryEncoder, lcd: MyLCD, devices: []):
        self._encoder = encoder
        self._lcd = lcd
        self._devices = devices

        self._manual_mode = False
        self._current_device = 0
        self._prev_device = 0
        self._device_count = len(devices)
        
        
        

    
    async def loop(self):
       pressed = False
       
       
       while True:
            
            if self._encoder.get_button() == 0:
                if pressed == False:
                    self._manual_mode = not self._manual_mode
                    
                    if self._manual_mode:
                        self.print_device()
                        #self._devices[self._current_device].enable_lcd()
                        self._encoder.update_raw(self._encoder.get_raw())
                    else:
                        self._devices[self._current_device].disable_lcd()
                        
                pressed = True
            else:
                pressed = False
            
           # print(self._manual_mode)
            
            

            # if manual mode on, then check rotations
            if(self._manual_mode):
                #print(self._current_device, self._devices[self._current_device].config.id)
                val_new = self._encoder.get_raw()
                val_old = self._encoder.get_raw_prev()


                # setting device to display
                if val_new > val_old:
                    self._current_device = (self._current_device + 1) % self._device_count

                if val_new < val_old:
                    self._current_device = (self._current_device - 1) % self._device_count
                
                if val_new != val_old:
                    self._encoder.update_raw(val_new)
                    self._devices[self._prev_device].disable_lcd()
                    #self._devices[self._current_device].enable_lcd()
                    self.print_device()
                    
            
                
                # now we have selected device + manual mode, so we can display its data
                
                # we will tell that device that it can start printing now
                
                
            
                
                
                
            await uasyncio.sleep_ms(50)
    def print_device(self):
        dev_type = self._devices[self._current_device].config.type
        dev_name = self._devices[self._current_device].config.name
        dev_id = self._devices[self._current_device].config.id
        
        self._lcd.clear()
        self._lcd.print(f"{dev_type} {dev_name} {dev_id}")
        self._devices[self._current_device].enable_lcd()
