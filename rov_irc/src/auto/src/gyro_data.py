import pyrealsense2 as rs
import rospy
from geometry_msgs.msg import Pose
import numpy as np
import time

# Initialize pipeline and config
pipeline = rs.pipeline()
config = rs.config()

# Enable motion stream
config.enable_stream(rs.stream.gyro)

pub=rospy.Publisher("rover/pose", Pose, queue_size=10)
pose=Pose()

# Initialize variables
angles = np.array([0.0, 0.0, 0.0])
bias = np.array([0.0, 0.0, 0.0])
prev_timestamp = None
samples_for_bias = 100
gyro_data_samples = []

# Time intervals for periodic printing (in seconds)
print_interval = 2
last_print_time = time.time()

try:
    print("Calibrating gyroscope...")
    pipeline.start(config)

    # Collect bias samples
    while len(gyro_data_samples) < samples_for_bias:
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        if gyro_frame:
            gyro = gyro_frame.as_motion_frame().get_motion_data()
            gyro_data_samples.append([gyro.x, gyro.y, gyro.z])

    # Compute bias (average of samples)
    bias = np.mean(gyro_data_samples, axis=0)
    print(f"Gyroscope bias: X={bias[0]:.5f}, Y={bias[1]:.5f}, Z={bias[2]:.5f}")
    print("Start moving the camera. Press Ctrl+C to stop.")

    while True:
        frames = pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)

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
            
            pose.orientation.x, pose.orientation.y, pose.orientation.z=angles_degrees[0], angles_degrees[1], angles_degrees[2]
            pub.publish(pose)
            # Periodically print angles
            if time.time() - last_print_time >= print_interval:
                angles_degrees = np.degrees(angles)
                rospy.loginfo(
                    f"Angles (degrees): X={angles_degrees[0]:.2f}, Y={angles_degrees[1]:.2f}, Z={angles_degrees[2]:.2f}"
                )
                last_print_time = time.time()

finally:
    # Stop the pipeline
    pipeline.stop()
    print("Measurement stopped.")
