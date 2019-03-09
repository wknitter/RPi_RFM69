# RFM69 radio bonnet transmitter test
import time
import busio
import board
import adafruit_ssd1306
import adafruit_rfm69
from digitalio import DigitalInOut, Direction, Pull

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
 
# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# RFM69 Configuration
packet = None
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
rfm69.encryption_key = None

while True:
    # initialization
    packetRX = None
    packetTX = None
    display.fill(0)    
    display.text('RFM69: init', 0, 0, 1)
    display.show()
    count = 0

    packetTX = bytes("Hello World!", "utf-8")
    rfm69.send(packetTX)
    display.fill(0)
    display.text('Packet sent', 0, 0, 1)
    display.show()

    while((packetRX == None) & (count < 10)):
        display.fill(0)
        display.text('Listening for ack packet...', 0, 0, 1)
        display.show()
        packetRX = rfm69.receive()
        count = count + 1

    if not packetRX is None:
        display.fill(0)
        packet = packetRX
        displayPacket = str(packet, "utf-8")
        display.text('ACK Packet = ', 0, 0, 1)
        display.text(displayPacket, 25, 10, 1)
        display.show()
        time.sleep(3)
