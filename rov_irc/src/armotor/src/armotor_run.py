#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from arm_ctrl.msg import arm_msg
import serial
import struct

class TeleopSubscriber():
    def __init__(self):
        rospy.init_node('teleop_wheel', anonymous=True)
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.subscription_speed = rospy.Subscriber('/cmd_vel', Twist, self.listener_callback_speed)
        self.subscription_arm = rospy.Subscriber('/chat', arm_msg, self.listener_callback_arm)
        
        self.w_r = 0
        self.w_l = 0
        self.wheel_rad = 0.0125 
        self.wheel_sep = 0.600
        self.lowSpeed = 200
        self.highSpeed = 50
        self.speed_ang = 0
        self.speed_lin = 0
        
        # Motor and arm control message
        self.serial_msg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] 
        # [motorLF motorLB motorRF motorRB base_rotation link1 link2 link3 gripper_wrist gripper_claw]
        
        self.base_speed_lock = 25
        self.link_speed = 255
        self.gripper_wrist = 255
        self.gripper_claw = 255
        
        # Reset motors initially
        self.reset_motors()

    def reset_motors(self):
        self.serial_msg = [0] * 10
        self.send_float_array(self.serial_msg)
        rospy.loginfo("Motors reset to neutral (stopped).")

    def listener_callback_speed(self, msg):
        self.speed_ang = msg.angular.z
        self.speed_lin = msg.linear.x
        
        self.w_r = (self.speed_lin/self.wheel_rad) + ((self.speed_ang*self.wheel_sep)/(2.0*self.wheel_rad))
        self.w_l = (self.speed_lin/self.wheel_rad) - ((self.speed_ang*self.wheel_sep)/(2.0*self.wheel_rad))
        
        self.MotorL(self.w_l * 10)
        self.MotorR(self.w_r * 10)
        
        rospy.loginfo(f"Wheel Speeds: Left={self.w_l}, Right={self.w_r}")
        rospy.loginfo(f"Serial Data: {self.serial_msg}")
        self.send_float_array(self.serial_msg)

    def listener_callback_arm(self, msg):
        self.serial_msg[4] = msg.base_motor * self.base_speed_lock
        self.serial_msg[5] = msg.link_1 * self.link_speed
        self.serial_msg[6] = msg.link_2 * self.link_speed
        self.serial_msg[7] = msg.link_3 * self.link_speed
        self.serial_msg[8] = msg.waist * self.gripper_wrist
        self.serial_msg[9] = msg.claw * self.gripper_claw
        
        rospy.loginfo(f"Arm Control Data: {self.serial_msg}")
        self.send_float_array(self.serial_msg)

    def MotorL(self, PulseWidth):
        self.serial_msg[0] = PulseWidth
        self.serial_msg[1] = PulseWidth

    def MotorR(self, PulseWidth):
        self.serial_msg[2] = PulseWidth
        self.serial_msg[3] = PulseWidth

    def send_float_array(self, data):
        try:
            packed_data = struct.pack('<10f', *data)
            self.ser.write(packed_data)
        except struct.error:
            rospy.logwarn("Invalid data, not sending to Arduino.")

    def read_serial_data(self):
        while not rospy.is_shutdown():
            if self.ser.in_waiting > 0:
                arduino_data = self.ser.readline().decode('utf-8').strip()
                if arduino_data:
                    rospy.loginfo(f"Data from Arduino: {arduino_data}")

if __name__ == '__main__':
    try:
        teleopSub = TeleopSubscriber()
        rospy.spin()
    except rospy.ROSInterruptException:
        teleopSub.reset_motors()
        pass
