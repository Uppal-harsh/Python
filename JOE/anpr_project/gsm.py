import serial
import time
from config import SERIAL_PORT, BAUD_RATE

class GSMManager:
    def __init__(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            self.connected = True
            print("GSM Module Connected")
        except Exception as e:
            print(f"GSM Connection Error: {e}")
            self.connected = False

    def send_at(self, command, wait_time=1):
        if not self.connected: return ""
        self.ser.write((command + "\r\n").encode())
        time.sleep(wait_time)
        return self.ser.read(self.ser.inWaiting()).decode()

    def send_sms(self, phone_number, message):
        if not self.connected: return False
        
        print(f"Sending SMS to {phone_number}...")
        self.send_at("AT+CMGF=1") # Set SMS mode to text
        time.sleep(0.1)
        self.send_at(f'AT+CMGS="{phone_number}"')
        time.sleep(0.1)
        self.ser.write((message + "\x1A").encode()) # Send CTRL+Z
        time.sleep(3)
        print("SMS Task Sent")
        return True

    def close(self):
        if self.connected:
            self.ser.close()
