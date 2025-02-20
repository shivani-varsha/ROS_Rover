#!/usr/bin/env python3

import rospy
import pyrealsense2 as rs
from sensor_msgs.msg import Image, Imu
from std_msgs.msg import Bool
from cv_bridge import CvBridge
import cv2
import numpy as np

import pyrealsense2 as rs
import rospy
from geometry_msgs.msg import Pose
import numpy as np
import time

reset=False

def publish_realsense_data():
    global reset
    def reset_callback(msg):
        global reset
        reset=msg.data

    rospy.init_node('realsense_camera_node', anonymous=True)

    # Initialize variables
    pose=Pose()
    angles = np.array([0.0, 0.0, 0.0])
    bias = np.array([0.0, 0.0, 0.0])
    prev_timestamp = None
    samples_for_bias = 100
    gyro_data_samples = []

    # Time intervals for periodic printing (in seconds)
    print_interval = 2
    last_print_time = time.time()
    # Publishers for depth, RGB, gyro, and accelerometer data
    rgb_pub = rospy.Publisher('/camera/rgb/image_raw', Image, queue_size=10)
    depth_pub = rospy.Publisher('/camera/depth/image_raw', Image, queue_size=10)
    pub=rospy.Publisher("rover/pose", Pose, queue_size=10)
    rospy.Subscriber("camera/reset", Bool, reset_callback)

    # Initialize RealSense pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.gyro)
    config.enable_stream(rs.stream.accel)

    # Start streaming
    pipeline.start(config)

    bridge = CvBridge()
    rate = rospy.Rate(30)  # 30 Hz

    try:
        while not rospy.is_shutdown():
            frames = pipeline.wait_for_frames()

            # RGB frame
            color_frame = frames.get_color_frame()
            if color_frame:
                color_image = np.asanyarray(color_frame.get_data())
                rgb_msg = bridge.cv2_to_imgmsg(color_image, encoding='bgr8')
                rgb_pub.publish(rgb_msg)

                # Display the RGB image
                cv2.imshow('RGB Stream', color_image)

            # Depth frame
            depth_frame = frames.get_depth_frame()
            if depth_frame:
                depth_image = np.asanyarray(depth_frame.get_data())
                depth_msg = bridge.cv2_to_imgmsg(depth_image, encoding='passthrough')
                depth_pub.publish(depth_msg)

                # Display the Depth image
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                cv2.imshow('Depth Stream', depth_colormap)

            while len(gyro_data_samples) < samples_for_bias:
                frames = pipeline.wait_for_frames()
                gyro_frame = frames.first_or_default(rs.stream.gyro)
                if gyro_frame:
                    gyro = gyro_frame.as_motion_frame().get_motion_data()
                    gyro_data_samples.append([gyro.x, gyro.y, gyro.z])

            # Compute bias (average of samples)
            bias = np.mean(gyro_data_samples, axis=0)
            gyro_frame = frames.first_or_default(rs.stream.gyro)
            if reset:
                angles = np.array([0.0, 0.0, 0.0])
                reset=False
            if gyro_frame:
                # Extract gyro data and subtract bias
                gyro = gyro_frame.as_motion_frame().get_motion_data()
                gyro_corrected = np.array([gyro.x, gyro.y, gyro.z]) - bias

                timestamp = gyro_frame.get_timestamp()

                if prev_timestamp is not None:
                    # Calculate time difference in seconds
                    dt = (timestamp - prev_timestamp) / 1000.0  # Convert ms to seconds

                    # Integrate angular velocity to calculate angular displacement
                    angles += gyro_corrected * dt

                prev_timestamp = timestamp

                # Periodically print angles
                if time.time() - last_print_time >= print_interval:
                    angles_degrees = np.degrees(angles)
                    rospy.loginfo(
                        f"Angles (degrees): X={angles_degrees[0]:.2f}, Y={angles_degrees[1]:.2f}, Z={angles_degrees[2]:.2f}"
                    )
                    last_print_time = time.time()
                pose.orientation.x, pose.orientation.y, pose.orientation.z=angles_degrees[0], angles_degrees[1], angles_degrees[2]
                pub.publish(pose)

            # Wait for a key press to update frames
            key = cv2.waitKey(1)
            if key == 27:  # Escape key to exit
                break

            rate.sleep()

    except rospy.ROSInterruptException:
        pass
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()  # Close the OpenCV windows when done

if __name__ == '__main__':
    publish_realsense_data()

