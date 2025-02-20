#!/usr/bin/env python3
import rospy
import serial
from std_msgs.msg import String

# Initialize serial communication
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace with your Arduino serial port
rospy.init_node('sensor_data_node', anonymous=True)

# Create publishers for GPS and BME680 data
gps_pub = rospy.Publisher('gps_data', String, queue_size=10)
bme_pub = rospy.Publisher('bme680_data', String, queue_size=10)

def read_serial_data():
    while not rospy.is_shutdown():
        if ser.in_waiting > 0:
            # Read the serial data
            data = ser.readline().decode('utf-8').strip()
            
            # Separate the GPS and BME680 data
            if "GPS Data:" in data:
                gps_pub.publish(data)
            elif "BME680 Data:" in data:
                bme_pub.publish(data)
            else:
                rospy.loginfo(data)

if __name__ == '__main__':
    try:
        # Start reading and publishing data
        read_serial_data()
    except rospy.ROSInterruptException:
        pass

