import time
import serial


class Sensor:

    def __init__(self, serial_con):
        self.serial = serial_con
        self.stopped = False

    def start(self):
        while not self.stopped:
            if self.serial.in_waiting > 0:
                data = self.serial.readline()
                print(data.decode('utf-8').rstrip())
            time.sleep(1)

    def stop(self):
        self.stopped = True
        self.serial.close()
        print('closed')


s = Sensor(serial.Serial('/dev/ttyAMA0', 115200, timeout=1))
try:
    s.start()
except KeyboardInterrupt:
    s.stop()
