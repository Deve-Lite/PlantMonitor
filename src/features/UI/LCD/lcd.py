from lcd_i2c import LCD
from machine import I2C, Pin
import uasyncio
from abstractions.configuration import Configuration

class MyLCDConfig:
    def __init__(self, config):
        config = config["lcd"]
        self.i2c_addr = int(config["i2c_addr"],16)
        self.rows = config["rows"]
        self.cols = config["cols"]
        self.buff_size = config["buff_size"]
        self.sda = config["sda_pin"]
        self.scl = config["scl_pin"]

class MyLCD:
    def __init__(self, config: MyLCDConfig):
        self.config = config
        self.hidden_cols = config.buff_size - config.cols
        
        
        i2c = I2C(0, scl=Pin(config.scl), sda=Pin(config.sda), freq=800000)
        self.lcd = LCD(addr=config.i2c_addr, cols=config.cols, rows=config.rows,i2c=i2c)
        
        self.lcd.begin()
        self.lcd.home()
        
        
    def split_text(self, text, prefix="", postfix=""):
        text = text.replace('\n', ' ')  # for multiline strings
        text = self.config.cols * prefix + text + self.config.cols * postfix
        
        fragments = []
        last_n = ""
        for i in range(0, len(text), self.hidden_cols):
            fragment = last_n + text[i:i+ self.hidden_cols]
            fragments.append(fragment)
            last_n = fragment[-self.config.cols:]

        return fragments

        
    async def display_long_text(self, text, interval=0.2, prefix="", postfix=""):
        fragments = self.split_text(text, prefix, postfix)
        
        print(fragments)
        for fragment in fragments:
            self.lcd.home()
            self.lcd.print(fragment)
            for _ in range(min(len(fragment) - self.config.cols, self.hidden_cols)):
                self.lcd.scroll_display_left()
                await uasyncio.sleep(interval)
        
    
    def print(self, text):
        self.lcd.print(text)
        
    def clear(self):
        self.lcd.clear()
        

    # prints values Probably TO be changed
    def print_values(self, *args):
        values = []
        units = []
        for i in range(0, len(args), 2):
            values.append(args[i])
            units.append(args[i+1])
            
        
        unit_mapping = {
        "Celsius": "C",
        "Percentage": "%"
        }
    
      
        mapped_units = [unit_mapping.get(unit, "") for unit in units]
        
        to_display = [f"{value}{unit}" for value, unit in zip(values, mapped_units)]
        
        spaces_total = self.cols - sum([len(to_display[i]) for i in range(len(to_display))])
        
        spaces_per_word = spaces_total // (len(to_display) -  1)
        
        buff =""
        for i in range(len(to_display)-1):
            buff += (to_display[i])
            buff += (spaces_per_word * " ")
        
    
        buff +=( (spaces_total -  (len(to_display) -1) * spaces_per_word) * " ")
        buff +=(to_display[-1])
        
        self.lcd.set_cursor(col=0, row=1)
        self.print(buff)
        print(buff)
        
