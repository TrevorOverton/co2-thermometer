
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import busio
import adafruit_bme280
import time
import adafruit_ccs811
import datetime
from gpiozero import Button

button = Button(21)
b = True

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

while not ccs811.data_ready:
    pass

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

WIDTH = 128
HEIGHT = 32 
BORDER = 5
width = 128
height = 32
border = 5
x=0
padding = -2
top = padding
bottom = height - padding

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()


while True:

    if button.is_pressed:
        b = not b

    if b:

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        temp = bme280.temperature - 3
        humidity = round(bme280.humidity)
        pressure = round(bme280.pressure, 1)

        hour = datetime.datetime.now().hour
        if hour > 12:
            hour = hour - 12

        min = datetime.datetime.now().minute

        temp = (9/5)*temp + 32
        temp = round(temp, 1)

        draw.text((x, top + 0), "{}:{}".format(hour,min), font=font, fill=255)
        draw.text((x, top + 8), "Temperature: {} F".format(temp), font=font, fill=255)
        draw.text((x, top + 16), "Humidity: {} %".format(humidity), font=font, fill=255)
        draw.text((x, top + 25), "Pressure: {} Mbar ".format(pressure), font=font, fill=255)

        oled.image(image)
        oled.show()

        time.sleep(10)

        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        try:
            co2 = ccs811.eco2
            tvoc = ccs811.tvoc
        except:
            pass

        hour = datetime.datetime.now().hour
        if hour > 12:
            hour = hour - 12

        min = datetime.datetime.now().minute

        draw.text((x, top + 0), "{}:{}".format(hour,min), font=font, fill=255)
        draw.text((x, top + 8), "CO2: {} ppm".format(co2), font=font, fill=255)
        draw.text((x, top + 16), "TVOC: {} ppb".format(tvoc), font=font, fill=255)

        oled.image(image)
        oled.show()

        time.sleep(10)
    else:
        oled.fill(0)
        oled.show()

        time.sleep(1)


