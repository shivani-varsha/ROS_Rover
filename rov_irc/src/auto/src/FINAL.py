import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pyrealsense2 as rs
from scipy.ndimage import gaussian_filter, binary_erosion, binary_dilation, label, median_filter
from scipy.ndimage import label, find_objects
import plotly.graph_objects as go

# Initialize Intel RealSense pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start the pipeline
pipeline.start(config)

# Camera and scene setup
lens_angle = {"down": 40}
height_camera = 77  # Camera height in cm
threshold_height = 10  # Adjusted obstacle height threshold in mm
min_obstacle_height = 10  # Minimum height difference to consider as an obstacle in mm
obs_threshold = 10

def bell_curve_weighted_mean(arr):
    """Function to calculate the weighted mean of a 1D array using a bell curve."""
    return arr  # Placeholder implementation

def detect_obstacles(depth_array, lens_angle, height_camera, obs_threshold):
    """Detect obstacles and create a segmented image."""
    depth_array = median_filter(depth_array, size=1)
    smoothed_depth_array = gaussian_filter(depth_array, sigma=2)
    nsamples_depth = smoothed_depth_array.shape[0]
    angles = np.linspace(90, (90 - lens_angle['down']), nsamples_depth)
    angles = np.radians(angles)

    # Predicted distance (per row)
    predicted_dist = np.zeros_like(depth_array, dtype=float)
    for i in range(depth_array.shape[0]):
        predicted_dist[i, :] = height_camera * (1. / np.cos(angles[i]))

    # Actual depth (per row, using the weighted mean)
    actual_depth = np.zeros_like(depth_array, dtype=float)
    for i in range(depth_array.shape[0]):
        actual_depth[i, :] = bell_curve_weighted_mean(depth_array[i])

    hyp = predicted_dist - actual_depth
    obstacle_height = hyp * np.cos(np.radians(90 - np.degrees(angles[i])))
    obstacle_height = np.where((obstacle_height > 1000) | (obstacle_height < -100), 0, obstacle_height)

    min_depth_threshold = 10  # Relaxed minimum distance
    max_depth_threshold = 300.0  # Relaxed maximum distance
    obstacle_mask = (obstacle_height > threshold_height) & (actual_depth > min_depth_threshold) & (actual_depth < max_depth_threshold)

    # Create a segmentation image with two colors
    segmented_image_obstacles = np.zeros((*depth_array.shape, 3), dtype=np.uint8)
    for i in range(depth_array.shape[0]):
        for j in range(depth_array.shape[1]):
            if obstacle_mask[i, j]:
                segmented_image_obstacles[i, j] = [255, 0, 0]  # Red for obstacles
            else:
                segmented_image_obstacles[i, j] = [0, 0, 255]  # Blue for background

    return segmented_image_obstacles, predicted_dist, obstacle_mask, obstacle_height, actual_depth

# Detect obstacles

def on_click(event):
    """Handle click events on the plots to return height from obstacle_height array."""
    if event.inaxes is not None:
        # Get the clicked pixel coordinates
        y, x = int(event.xdata), int(event.ydata)
       
        
        # Ensure the coordinates are within bounds
        if x >= depth_array.shape[0] or y >= depth_array.shape[1]:
            print(f"Clicked Pixel: ({x}, {y}) is out of bounds!")
            return

        # Check if the pixel is in the obstacle mask
        if obstacle_mask[x, y]:
            # Get the height from the obstacle_height array for the clicked pixel
            clicked_obstacle_height = obstacle_height[x, y]
            #if clicked_obstacle_height>0:
            print(f"Clicked Pixel: ({x}, {y}), Obstacle Height: {clicked_obstacle_height:.2f} mm")
            print(f"Predicted Distance: {predicted_dist[x, y]:.2f} mm")
            print(f"Actual Depth: {actual_depth[x, y]:.2f} mm")
        else:
            print(f"Clicked Pixel: ({x}, {y}), No obstacle detected at this location.")

plt.ion()
fig, axs = plt.subplots(1, 4, figsize=(15, 5))
fig.canvas.mpl_connect('button_press_event', on_click)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        depth_array = np.asanyarray(depth_frame.get_data()) * 0.001  # Convert depth to meters
        depth_array = depth_array[239:] * 70  # Adjust depth scaling as needed
        segmented_image_obstacles, predicted_dist, obstacle_mask, obstacle_height, actual_depth = detect_obstacles(
            depth_array, lens_angle, height_camera, threshold_height
        )
        labeled_mask, num_features = label(obstacle_mask)

# Identify the closest obstacle
        min_depth = float('inf')
        closest_obstacle_slice = []
        min_size_threshold = 10000  # Minimum size threshold for an obstacle

        for i in range(1, num_features + 1):
            slices = find_objects(labeled_mask == i)
            if slices:
                sl = slices[0]
                region_depth = actual_depth[sl[0], sl[1]]
                mean_depth = np.mean(region_depth)

                # Check the size of the obstacle
                region_size = (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start)

                if region_size > min_size_threshold:
                    closest_obstacles.append((sl, mean_depth))

        # Sort the obstacles by depth (ascending) and select the two closest
        closest_obstacles = sorted(closest_obstacles, key=lambda x: x[1])

        segmented_image_between_obstacles = np.zeros_like(segmented_image_obstacles)
        if len(closest_obstacles)<2:
            sl1,_=closest_obstacles[0]
            x_start1, x_stop1 =sl1[1].start, sl1[1].stop
            mid=(x_start1+x_stop1)//2
            print(mid)
            if mid<=239:
                segmented_image_between_obstacles[:, x_stop1:x_stop1+1] = [0, 255, 0] 
                segmented_image_between_obstacles[:, x_stop1+100:x_stop1+101] = [0, 255, 0]
            else:
                segmented_image_between_obstacles[:, x_start1:x_start1+1] = [0, 255, 0] 
                segmented_image_between_obstacles[:, x_start1-200:x_start1-199] = [0, 255, 0]

        else:
            sl1,_=closest_obstacles[0]
            sl2,_=closest_obstacles[1]
            if sl1[1].start<sl2[1].start:
                
                x_start1, x_stop1 =sl1[1].start, sl1[1].stop
                x_start2, x_stop2 =sl2[1].start, sl2[1].stop
                # Only fill the area between the closest obstacles with green, without overriding the obstacles
                segmented_image_between_obstacles[:, x_stop1:x_stop1+1] = [0, 255, 0] 
                segmented_image_between_obstacles[:, x_start2:x_start2+1] = [0, 255, 0]  # Green for the area between the obstacles
                if (x_start2-x_stop1)>=100:
                    print("Rover can go through")
                else:
                    print("Rover can't go through")

            else:
                x_start1, x_stop1 =sl1[1].start, sl1[1].stop
                x_start2, x_stop2 =sl2[1].start, sl2[1].stop
                # Only fill the area between the closest obstacles with green, without overriding the obstacles
                segmented_image_between_obstacles[:, x_stop2:x_stop2+1] = [0, 255, 0] 
                segmented_image_between_obstacles[:, x_start1:x_start1+1] = [0, 255, 0] 
                if (x_start1-x_stop2)>=100:
                    print("Rover can go through")
                else:
                    print("Rover can't go through")


        #bounding_boxes_with_widths, nearest_obstacle = find_bounding_boxes_and_widths(obstacle_mask, depth_array)

        axs[0].clear()
        axs[0].imshow(depth_array, cmap='viridis')
        axs[0].axis('off')
        axs[0].set_title("Original Depth Map")

        axs[1].clear()
        axs[1].imshow(obstacle_height, cmap='viridis')
        axs[1].axis('off')
        axs[1].set_title("Object vs Background Segmentation")

        axs[2].clear()
        axs[2].imshow(segmented_image_obstacles)
        axs[2].axis('off')
        axs[2].set_title("Obstacle Detection")

        axs[3].clear()
        axs[3].imshow(segmented_image_between_obstacles)
        axs[3].set_title("Area Between Two Closest Obstacles")
        axs[3].axis('off')

        for i in range(1, num_features + 1):
            slices = find_objects(labeled_mask == i)
            if slices:
                sl = slices[0]
                y_start, y_stop = sl[0].start, sl[0].stop
                x_start, x_stop = sl[1].start, sl[1].stop
                axs[2].add_patch(plt.Rectangle((x_start, y_start), x_stop - x_start, y_stop - y_start, edgecolor='yellow', facecolor='none', lw=2))

        # Highlight the closest obstacle in green
        if closest_obstacle_slice:
            y_start, y_stop = closest_obstacle_slice[0].start, closest_obstacle_slice[0].stop
            x_start, x_stop = closest_obstacle_slice[1].start, closest_obstacle_slice[1].stop
            axs[2].add_patch(plt.Rectangle((x_start, y_start), x_stop - x_start, y_stop - y_start, edgecolor='green', facecolor='none', lw=2))
            #axs[2].add_patch(rect)

        top_two_closest=closest_obstacles[:2]
        
        for obstacle in top_two_closest:
            sl, _ = obstacle
            print("Coordinates",sl,_)
            y_start, y_stop = sl[0].start, sl[0].stop
            x_start, x_stop = sl[1].start, sl[1].stop

            # Draw a yellow rectangle around each closest obstacle
            plt.gca().add_patch(
                plt.Rectangle(
                    (x_start, y_start),
                    x_stop - x_start,
                    y_stop - y_start,
                    edgecolor='yellow',
                    facecolor='none',
                    lw=2
                )
            )

        plt.pause(0.01)

except KeyboardInterrupt:
    print("Stream stopped.")
finally:
    pipeline.stop()
