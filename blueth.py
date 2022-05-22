import serial

serialPort = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=1)
size = 1024

while 1:
    data = serialPort.readline(size)

    if data:
        print(data)