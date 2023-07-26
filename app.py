import boto3
import requests
import time
#import board
import adafruit_tmp117
from adafruit_tmp117 import TMP117, AlertMode, AverageCount
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

i2c = board.I2C()  # uses board.SCL and board.SDA
print("-" * 40)
print(i2c)
print("-" * 40)
tmp117 = TMP117(i2c)
print(type(tmp117.serial_number))
print("HEX :", hex(tmp117.serial_number))
print("-" * 40)

#tmp117 = adafruit_tmp117.TMP117(i2c)
tmp117.high_limit = 30
tmp117.low_limit = 10

print("\nHigh limit", tmp117.high_limit)
print("Low limit", tmp117.low_limit)

# Try changing `alert_mode`  to see how it modifies the behavior of the alerts.
tmp117.alert_mode = AlertMode.WINDOW #default
tmp117.alert_mode = AlertMode.HYSTERESIS


print("Alert mode:", AlertMode.string[tmp117.alert_mode])
#print("\n\n")
tmp117.averaged_measurements = AverageCount.AVERAGE_64X
print("Number of averaged samples per measurement:",
                AverageCount.string[tmp117.averaged_measurements],
            )
#print("")

myMQTTClient = AWSIoTMQTTClient("Demo") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a37tyqers5vox-ats.iot.us-east-1.amazonaws.com", 8883)
#a37tyqers5vox-ats.iot.us-east-1.amazonaws.com

myMQTTClient.configureCredentials("/home/pi/technoHealth/AmazonRootCA1.pem", "/home/pi/technoHealth/newprivate.key", "/home/pi/technoHealth/NewCer.crt")

#myMQTTClient.configureCredentials("/home/pi/technoHealth/AmazonRootCA1.pem", "/home/pi/technoHealth/Demo.private.key", "/home/pi/technoHealth/Demo.cert.pem")
#myMQTTClient.configureCredentials("AmazonRootCA1.pem", "Demo.private.key", "Demo.crt.pem")
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer From Raspberry Pi...')
myMQTTClient.connect()
myMQTTClient.subscribre("home/Helloworld",1, helloword)
def loop():
    while True:
        print("-" * 40)
        print("Temperature: %.2f degrees C" % tmp117.temperature)
        temperature= tmp117.temperature
        fahrenheit = tmp117.temperature * 1.8 + 32
        print("Sending Temperature: ", Fahrenheit)
        alert_status = tmp117.alert_status
        #print("High alert:", alert_status.high_alert)
        #print("Low alert:", alert_status.low_alert)
        print("")
        time.sleep(0.1)
        print("-" * 40)
       

        myMQTTClient.publish(
            topic="RealTimeDataTrasfer/Temperature",
            QoS=1,
            payload='{"Temperature":"'+str(fahrenheit)+'"}')

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        pass
