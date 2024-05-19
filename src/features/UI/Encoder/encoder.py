from rotary_irq_rp2 import RotaryIRQ
from machine import Pin



class EncoderConfig:
    def __init__(self, config):
        config = config["encoder"]
        self.clk = config["clk"]
        self.dt = config["dt"]
        self.min_val = config["min_val"]
        self.sw = config["sw"]
        


class RotaryEncoder:
    def __init__(self, config: EncoderConfig):
        self.r = RotaryIRQ(pin_num_clk=config.clk,
                          pin_num_dt=config.dt,
                          min_val=config.min_val,
                          reverse=True,
                          range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        self.val_old = self.r.value()
        self.sw = Pin(config.sw, Pin.IN, Pin.PULL_UP)


    def get_raw(self):
        return self.r.value()
    
    def get_raw_prev(self):
        return self.val_old
    
    def update_raw(self, val: int):
        self.val_old = val
    
    def get_button(self):
        return self.sw.value()
    
    def reset(self):
        self.r.reset()
    

    
    
    