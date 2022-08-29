


class Meter(object):

    def __init__(self, name):
        self.device_name = name
        self.temperature = 0
        self.humidity = 0

    def set_measurements(self, temp, humidity):
        # Temp from device status is given in C
        self.temperature = self.convert_C_to_F(temp)
        self.humidity = humidity

    def convert_C_to_F(self, temp):

        return (temp * 1.8) + 32

    def __str__(self):
        return f"{self.device_name}\nTemperature: {round(self.temperature, 1)} F\nHumidity: {self.humidity} %\n"
