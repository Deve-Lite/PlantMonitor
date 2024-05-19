from rotary_irq_rp2 import RotaryIRQ
from machine import Pin


class RotaryEncoder:
    def __init__(self, clk=15, dt=14, min_val=0, sw=16):
        self.r = RotaryIRQ(pin_num_clk=clk,
                          pin_num_dt=dt,
                          min_val=min_val,
                          reverse=True,
                          range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        self.val_old = self.r.value()
        self.sw = Pin(sw, Pin.IN, Pin.PULL_UP)


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
    

    
    
    