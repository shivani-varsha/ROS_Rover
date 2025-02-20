#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import serial
import struct

class TeleopMotorController():

    def __init__(self):
        rospy.init_node('teleop_wheel')
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.subscription_speed = rospy.Subscriber('/cmd_vel', Twist, self.listener_callback_speed)
        self.w_r = 0
        self.w_l = 0
        self.wheel_rad = 0.0125 
        self.wheel_sep = 0.600
        self.serial_msg = [0, 0, 0, 0]  # [motorLF, motorLB, motorRF, motorRB]

    def listener_callback_speed(self, msg):
        self.speed_ang = msg.angular.z
        self.speed_lin = msg.linear.x
        self.w_r = (self.speed_lin / self.wheel_rad) + ((self.speed_ang * self.wheel_sep) / (2.0 * self.wheel_rad))
        self.w_l = (self.speed_lin / self.wheel_rad) - ((self.speed_ang * self.wheel_sep) / (2.0 * self.wheel_rad))
        self.MotorL(self.w_l * 10)
        self.MotorR(self.w_r * 10)
        rospy.loginfo(str(self.serial_msg))
        self.send_float_array(self.serial_msg)

    def MotorL(self, PulseWidth):
        self.serial_msg[0] = PulseWidth
        self.serial_msg[1] = PulseWidth

    def MotorR(self, PulseWidth):
        self.serial_msg[2] = PulseWidth
        self.serial_msg[3] = PulseWidth

    def send_float_array(self, data):
        self.packed_data = struct.pack('ffff', *data)
        self.ser.write(self.packed_data)

if __name__ == '__main__':
    try:
        teleopMotor = TeleopMotorController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
