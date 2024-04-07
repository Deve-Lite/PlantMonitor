from features.analog_accessor.analog_accessor import AnalogAccessor

class SMSDriver:
    def __init__(self, analog_accessor: AnalogAccessor, channel, min_moist=0, max_moist=65535):
        self.analog_accessor  = analog_accessor
        self.__moisture = -1
        self.__channel = channel
        self.__min_moist = min_moist
        self.__max_moist = max_moist

    def measure(self):
        self.__moisture = self.analog_accessor.read(self.__channel)


    def moisture(self):
        if self.__moisture < 0:
            raise RuntimeError("moisture() method called before measure()")
        return (self.__moisture - self.__min_moist) * 100 / (self.__max_moist - self.__min_moist)

    