import time
import serial


class Sensor:

    def __init__(self, serial_con):
        self.serial = serial_con
        self.stopped = False

    def read_data(self):
        while not self.stopped:
            if self.serial.in_waiting > 0:
                data = self.serial.readline()
                print(data.decode('utf-8').rstrip())
            time.sleep(1)

    def close(self):
        self.stopped = True
        self.serial.close()
        print('closed')


s = Sensor(serial.Serial('/dev/ttyAMA0', 115200, timeout=1))
try:
    s.read_data()
except KeyboardInterrupt:
    s.close()
