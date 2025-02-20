#!/usr/bin/env python3

import rospy
from arm_ctrl.msg import arm_msg
import serial
import struct

class ArmController():

    def __init__(self):
        rospy.init_node('arm_control')
        # Use a separate serial port for the arm control
        self.ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
        self.subscription_arm = rospy.Subscriber('/chat', arm_msg, self.listener_callback_arm)
        
        # Initialize arm control variables
        self.serial_msg = [0, 0, 0, 0, 0, 0] # [base_rotation, link1, link2, link3, gripper_wrist, gripper_claw]
        self.base_speed_lock = 0
        self.link_speed = 90
        self.gripper_wrist = 90
        self.gripper_claw = 90

    def listener_callback_arm(self, msg):
        # Update the serial message array with arm control values
        self.serial_msg[0] = (msg.base_motor * self.base_speed_lock)
        self.serial_msg[1] = (msg.link_1 * self.link_speed)
        self.serial_msg[2] = (msg.link_2 * self.link_speed)
        self.serial_msg[3] = (msg.link_3 * self.link_speed)
        self.serial_msg[4] = (msg.waist * self.gripper_wrist)
        self.serial_msg[5] = (msg.claw * self.gripper_claw)

        rospy.loginfo(f"Arm Control Data: {self.serial_msg}")
        self.send_float_array(self.serial_msg)

    def send_float_array(self, data):
        # Pack the data into a binary format and send via serial
        packed_data = struct.pack('ffffff', *data)
        self.ser.write(packed_data)

if __name__ == '__main__':
    try:
        armController = ArmController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
