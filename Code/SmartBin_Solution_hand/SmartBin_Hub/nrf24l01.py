from RF24 import *
import time
from config import *

class NRF24L01:
    def __init__(self):
        self.radio = RF24(22, 0)

        self.radio.begin()
        self.radio.enableDynamicPayloads()
        self.radio.setRetries(5,15)
        self.radio.enableAckPayload()
        self.radio.setDataRate(RF24_250KBPS)

        self.radio.openWritingPipe(NRF24_ADDRESS)

        self.radio.powerUp()
    
    def write(self, data):
        self.radio.write(data)