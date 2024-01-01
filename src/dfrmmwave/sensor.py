import re
import time
from typing import List, Tuple, Callable

import serial


class Sensor:

    def __init__(self, serial_con):
        self.serial = serial_con
        self.stopped = False
        self.handlers: List[Tuple[Callable[[str], bool], bool]] = [(self._presence_handler, False)]
        self.observers: List[Callable[[bool], None]] = []

    def start(self):
        while not self.stopped:
            if self.serial.in_waiting > 0:
                msg_raw = self.serial.readline()
                msg = msg_raw.decode('utf-8').rstrip()
                self._handle_message(msg)
                print(msg)
            time.sleep(1)

    def _presence_handler(self, msg):
        presence_match = re.match(r'^\$JYBSS,([01])', msg)
        if presence_match:
            return False

        presence_value = presence_match.group(1)
        for observer in self.observers:
            observer(bool(presence_value))

        return True

    def _handle_message(self, msg):
        if not self.handlers:
            return

        for handler, remove in self.handlers:
            if handler(msg):
                if remove:
                    self.handlers.remove((handler, remove))
                break

    def stop(self):
        self.stopped = True
        self.serial.close()
        print('closed')


s = Sensor(serial.Serial('/dev/ttyAMA0', 115200, timeout=1))
try:
    s.start()
except KeyboardInterrupt:
    s.stop()
