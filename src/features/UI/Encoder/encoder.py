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
        self.encoder = RotaryIRQ(pin_num_clk=config.clk,
                          pin_num_dt=config.dt,
                          min_val=config.min_val,
                          reverse=True,
                          range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        

        self.prev_rot: int = self.encoder.value()
        self.button = Pin(config.sw, Pin.IN, Pin.PULL_UP)


    def get_current_rot(self):
        return self.encoder.value()
    
    def get_prev_rot(self):
        return self.prev_rot
    
    def update_prev_rot(self, val: int):
        self.prev_rot = val
    
    def is_button_pressed(self):
        return self.button.value() == 0
    
    def reset(self):
        self.encoder.reset()
    

    
    
    