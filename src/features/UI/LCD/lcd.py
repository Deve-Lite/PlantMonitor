from lcd_i2c import LCD
from machine import I2C, Pin
import uasyncio



class MyLCD:
    def __init__(self, i2c_addr=0x27, rows=2, cols=16, buff_s=40 , scl_pin=5, sda_pin=4):
        self.cols = cols
        self.rows = rows
        self.buff_s = buff_s
        self.hidden_cols = buff_s - cols
        
        
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=800000)
        self.lcd = LCD(addr=i2c_addr, cols=cols, rows=rows,i2c=i2c)
        
        self.lcd.begin()
        self.lcd.home()
        
        
    def split_text(self, text, prefix="", postfix=""):
        text = text.replace('\n', ' ')  # for multiline strings
        text = self.cols * prefix + text + self.cols * postfix
        
        fragments = []
        last_n = ""
        for i in range(0, len(text), self.hidden_cols):
            fragment = last_n + text[i:i+ self.hidden_cols]
            fragments.append(fragment)
            last_n = fragment[-self.cols:]

        return fragments

        
    async def display_long_text(self, text, interval=0.2, prefix="", postfix=""):
        fragments = self.split_text(text, prefix, postfix)
        
        print(fragments)
        for fragment in fragments:
            self.lcd.home()
            self.lcd.print(fragment)
            for _ in range(min(len(fragment) - self.cols, self.hidden_cols)):
                self.lcd.scroll_display_left()
                await uasyncio.sleep(interval)
        
    
    def print(self, text):
        self.lcd.print(text)
        
    def clear(self):
        self.lcd.clear()
        
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
        
