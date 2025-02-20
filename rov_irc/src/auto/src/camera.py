#!/usr/bin/env python3

import rospy
import cv2
from ultralytics import YOLO
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class RoverCameraDisplay:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('rover_camera_display', anonymous=False)
        
        # Create a bridge between ROS image messages and OpenCV
        self.bridge = CvBridge()
        self.model = YOLO("/home/sandy/rovdepth/src/autonomous_rover/scripts/best.pt").to('cuda')
        
        # Subscribe to the depth camera topic
        # Note: The topic name matches the cameraName in the Gazebo plugin
        rospy.Subscriber('/camera/rgb/image_raw', Image, self.camera_callback)
        rospy.Subscriber('/camera/depth/image_raw', Image, self.depth_callback)
        
        # Window to display the camera feed
        cv2.namedWindow('Rover Depth Camera', cv2.WINDOW_NORMAL)
    
    def depth_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="32FC1")
        depth_normalized = cv2.normalize(
            cv_image, 
            None, 
            alpha=0, 
            beta=255, 
            norm_type=cv2.NORM_MINMAX, 
            dtype=cv2.CV_8U
        )
        depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)
        self.depth = depth_colored

    def camera_callback(self, msg):
        try:
            # Convert ROS image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            
            # Run YOLO model on the image
            results = self.model(cv_image, conf=0.5, verbose=False)

            # Draw bounding boxes and class labels on the image
            for result in results[0].boxes:
                print(result.conf.item())
                x1, y1, x2, y2 = map(int, result.xyxy[0].tolist())
                class_id = int(result.cls[0])
                label = self.model.names[class_id]
                print(label)

                cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(cv_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            self.image = cv_image
        
        except Exception as e:
            rospy.logerr(f"Error processing image: {e}")
            # Print more detailed error information
            import traceback
            traceback.print_exc()
    
    def run(self):
        print("DEBUG")
        while(True):
            # Display the depth image
            if hasattr(self, 'image') and hasattr(self, 'depth'):
                cv2.imshow('Rover Depth Camera', self.image)
                cv2.imshow('Rover Depth Image', self.depth)
            
            # Break the loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting...")
                break

if __name__ == '__main__':
    camera_display = RoverCameraDisplay()
    camera_display.run()