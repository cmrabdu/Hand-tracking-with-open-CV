import serial
import time
import logging

class SerialObject:

    def __init__(self, portNo, baudRate, digits):

        self.portNo = portNo
        self.baudRate = baudRate
        self.digits = digits
        try:
            self.ser = serial.Serial(self.portNo, self.baudRate)
            print("Serial Device Connected")
        except:
            logging.warning("Serial Device Not Connected")

    def sendData(self, data):

        myString = "$"
        for d in data:
            myString += str(int(d)).zfill(self.digits)
        try:
            self.ser.write(myString.encode())
            return True
        except:
            return False


def main():
    mySerial = SerialObject("/dev/cu.usbmodem1101", 9600, 1)
    while True:
        mySerial.sendData([1, 1, 1, 1, 1])
        time.sleep(2)
        mySerial.sendData([0, 0, 0, 0, 0])
        time.sleep(2)


if __name__ == "__main__":
    main()
