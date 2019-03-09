# RFM69 radio bonnet receiver test
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
    display.fill(0)   

    
    while (packetRX == None):
        packetRX = rfm69.receive()
        display.text('Listening for packet...', 0, 0, 1)
        display.show()

    packet = packetRX
    displayPacket = str(packet, "utf-8")
    display.fill(0) 
    display.text('Packet = ', 0, 0, 1)
    display.text(displayPacket, 25, 10, 1)
    display.show()
    time.sleep(1)
    packetTX = bytes("ACK", "utf-8")
    rfm69.send(packetTX)
    packet = packetTX
    displayPacket = str(packet, "utf-8")
    display.fill(0) 
    display.text('ack Packet = ', 0, 0, 1)
    display.text(displayPacket, 25, 10, 1)
    display.show()
    time.sleep(1)
        
