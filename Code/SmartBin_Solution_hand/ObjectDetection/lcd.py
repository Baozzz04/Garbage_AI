import time

import RPi.GPIO as GPIO

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from config import *

class PCD8544:

    def __init__(self):
        self.disp = LCD.PCD8544(DC, RST, SCLK, DIN, CE)
        self.disp.begin(contrast=CONTRAST)

        self.disp.clear()
        self.disp.display()

        # Make sure to create image with mode '1' for 1-bit color.
        self.image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

    def draw_text(self, text, position):
        # Draw a white filled box to clear the image.
        self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
        # Write some text.
        self.draw.text(position, text)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()
