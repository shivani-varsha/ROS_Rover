#!/usr/bin/env python3
from ultralytics import YOLO
import numpy as np
import pyrealsense2 as rs
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import cv2
import time
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Pose
import rospy

class Runner:
    def __init__(self):
        rospy.init_node('simple_node', anonymous=True)
        self.twist_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.reseter = rospy.Publisher('camera/reset', Bool, queue_size=10)
        self.image_subscriber = rospy.Subscriber('/camera/rgb/image_raw', Image, self.callback)
        self.depth_subscriber = rospy.Subscriber('/camera/depth/image_raw', Image, self.depth_callback)
        self.angle_subscriber = rospy.Subscriber('/rover/pose', Pose, self.pose_callback)
        self.model = YOLO("/home/waaraak/Desktop/rover/rov_irc/src/auto/src/best.pt")
        self.bridge = CvBridge()
        self.twist = Twist()
        self.angle=0
        self.end_signal = False
        self.reset=False
        self.turn_at = 800
        self.search_deg = 10
        self.nturns = 360 / self.search_deg
        self.dir = 0
        self.bar = 0.8
        self.frame = None
        self.height = 5  # Height of the camera from ground
        self.move_speed = 1
        self.obs_threshold = 0.5
        self.turn_speed = 1
        self.check_turn_cols = 3
        self.dtorque = 0.1
        self.nsamples_depth = 50
        self.depth_array = None
        self.lens_angle = {"down": -43.5, "up": 43.5}
        self.wait_sec = 5
        self.f_width = None
        self.f_height = None

    def pose_callback(self, msg):
        self.angle=msg.orientation.y

    def depth_callback(self, msg):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            depth_image = cv2.resize(depth_image, (640, 480))
            self.depth_array = np.array(depth_image, dtype=np.float32)
        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {str(e)}")

    def callback(self, data):
        try:
            self.frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"Error converting image: {str(e)}")

    def get_depth_obj(self, depth_array: np.array, coords: list) -> float:
        x1, y1, x2, y2 = coords
        if depth_array is None:
            return float('inf')
        try:
            depth = depth_array[y1:y2, x1:x2]
            return np.mean(depth[~np.isnan(depth)])  # Exclude NaN values
        except (IndexError, ValueError):
            return float('inf')

    def predict(self):
        if self.frame is None:
            return None
        
        resized = cv2.resize(self.frame, (640, 480))
        self.f_width = resized.shape[1]
        self.f_height = resized.shape[0]
        
        results = self.model(resized, conf=0.5, verbose=False)
        if len(results[0].boxes.cls) == 0:
            return None
            
        boxes = []
        for result in results[0].boxes:
            score = result.conf.item()
            x1, y1, x2, y2 = map(int, result.xyxy[0].tolist())
            class_id = int(result.cls[0])
            
            if class_id == 0:
                boxes.append((x1, y1, x2, y2, score, -4))
            elif class_id == 1:
                boxes.append((x1, y1, x2, y2, score, 2))
                
        if not boxes:
            return None
            
        boxes = sorted(boxes, key=lambda box: box[4], reverse=True)
        return boxes[0]

    def search(self):
        direction = self.predict()
        if direction is not None:
            rospy.loginfo("Arrow Found")
            return [True, (direction[:4], direction[-1])]
        else:
            rospy.loginfo("Arrow Not Found")
            return False, None

    def move(self):
        dir = 0
        rospy.loginfo("Initializing movement")
        rate = rospy.Rate(10)  # 10 Hz control rate
        
        while not rospy.is_shutdown() and not self.end_signal:
            dir=0
            if self.frame is None or self.depth_array is None:
                rospy.logwarn("Waiting for camera data...")
                rate.sleep()
                continue
                
            found, result = self.search()
            if found and result is not None:
                try:
                    depth = self.get_depth_obj(self.depth_array, result[0])
                    dir+=result[1]
                    
                    while depth > self.turn_at:
                        rospy.loginfo("Found Arrow Mark. Moving.")
                        found, result = self.search()
                        if not found or result is None:
                            break
                        if not self.align_rover(*result[0][:4]):
                            continue
                        self.start_move()                    
                        depth = self.get_depth_obj(self.depth_array, result[0])
                        rospy.loginfo(f"Current depth: {depth}")
                        dir += result[1]
                        rospy.sleep(3)
                        self.stop_rover()
                        
                    if dir > 0:
                        self.stop_rover()
                        rospy.sleep(2.5)
                        self.right()
                        rospy.loginfo(f"Turning right: {dir}")
                        self.stop_rover()
                    elif dir < 0:
                        self.stop_rover()
                        rospy.sleep(2.5)
                        self.left()
                        rospy.loginfo(f"Turning left: {dir}")
                        self.stop_rover()
                        
                except Exception as e:
                    rospy.logerr(f"Error in move loop: {str(e)}")
                    self.stop_rover()
            else:
                self.start_move()
            
            rate.sleep()

    def align_rover(self, x1, y1, x2, y2):
        if self.f_width is None:
            return False
            
        center = (x1 + x2) / 2
        threshold = self.f_width * self.bar / 4
        center_frame = self.f_width / 2
        
        if center <= center_frame - 2 * threshold:
            rospy.loginfo("Major Left Adjustment")
            self.turn_left()
            return False
        elif center <= center_frame - threshold:
            rospy.loginfo("Minor Left Adjustment")
            self.turn_left_slow()
            return False
        elif center >= center_frame + 2 * threshold:
            rospy.loginfo("Major Right Adjustment")
            self.turn_right()
            return False
        elif center >= center_frame + threshold:
            rospy.loginfo("Minor Right Adjustment")
            self.turn_right_slow()
            return False
        else:
            rospy.loginfo("Proper Alignment")
            self.stop_rover()
            return True

    # Movement control methods
    def stop_rover(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.twist_publisher.publish(self.twist)

    def start_move(self, vel=0.5):
        self.twist.linear.x = vel
        self.twist_publisher.publish(self.twist)

    def left(self):
        self.twist.linear.x = 0
        self.twist.angular.z = -0.1
        self.twist_publisher.publish(self.twist)
        while(self.angle>-90):
            continue
        self.twist.angular.z = 0
        self.twist_publisher.publish(self.twist)
        self.reset=True
        self.reseter.publish(self.reset)
        
    def right(self):
        self.twist.linear.x = 0
        self.twist.angular.z = 0.25
        self.twist_publisher.publish(self.twist)
        while(self.angle<90):
            continue
        self.twist.angular.z = 0
        self.twist_publisher.publish(self.twist)
        self.reset=True
        self.reseter.publish(self.reset)

    def turn_left(self):
        self.twist.linear.x = 0
        self.twist.angular.z = -0.25
        self.twist_publisher.publish(self.twist)

    def turn_right(self):
        self.twist.linear.x = 0
        self.twist.angular.z = 0.25
        self.twist_publisher.publish(self.twist)

    def turn_left_slow(self):
        self.twist.linear.x = 0
        self.twist.angular.z = -0.2
        self.twist_publisher.publish(self.twist)

    def turn_right_slow(self):
        self.twist.linear.x = 0
        self.twist.angular.z = 0.2
        self.twist_publisher.publish(self.twist)

if __name__ == "__main__":
    try:
        node = Runner()
        rospy.loginfo("Starting Autonomous Mode")
        node.move()
    except rospy.ROSInterruptException:
        pass
