from features.analog_accessor.analog_accessor import AnalogAccessor


class InsolationDriver:
    def __init__(self, analog_accessor: AnalogAccessor, channel, min_insolation=0, max_insolation=65535):
        self.analog_accessor  = analog_accessor
        self.__insolation = -1
        self.__channel = channel
        self.__min_insolation = min_insolation
        self.__max_insolation = max_insolation

    def measure(self):
        self.__insolation = self.analog_accessor.read(self.__channel)


    def insolation(self):
        if self.__insolation < 0:
            raise RuntimeError("insolation() method called before measure()")
        return (self.__insolation - self.__min_insolation) * 100 / (self.__max_insolation - self.__min_insolation)

    