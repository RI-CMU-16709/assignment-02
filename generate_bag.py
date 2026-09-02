#!/usr/bin/env python3
"""Generate camera_bag/ — a rosbag2 recording of synthetic camera images.

Publishes 15 seconds of 320x240 color frames (a red ball bouncing over a
static scene) on /camera/image_raw at 10 Hz, recorded with `ros2 bag record`.
The publisher uses the standard sensor-data QoS profile, so the bag replays
with the same QoS a real camera driver would use.

Usage (with your ROS 2 environment sourced):
    python3 generate_bag.py

Requires: python3-opencv (sudo apt install python3-opencv)
"""
import math
import os
import signal
import subprocess
import sys
import time

import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image

WIDTH, HEIGHT = 320, 240
FPS = 10
SECONDS = 15
BAG_NAME = "camera_bag"
TOPIC = "/camera/image_raw"


def make_frame(i):
    """Renders frame i: a red ball bouncing over a static scene."""
    frame = np.full((HEIGHT, WIDTH, 3), 230, np.uint8)

    # Static scene elements (give Canny something constant to find).
    cv2.rectangle(frame, (20, 150), (90, 220), (60, 60, 60), 2)
    cv2.line(frame, (0, 120), (WIDTH, 100), (120, 120, 120), 2)
    cv2.putText(frame, "cam0", (250, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (100, 100, 100), 1, cv2.LINE_AA)

    # Moving ball.
    t = i / FPS
    x = int(WIDTH / 2 + (WIDTH / 2 - 40) * math.sin(0.8 * t))
    y = int(HEIGHT / 2 + (HEIGHT / 2 - 40) * math.sin(1.3 * t))
    cv2.circle(frame, (x, y), 25, (0, 0, 220), cv2.FILLED)
    return frame


def to_image_msg(frame, node):
    msg = Image()
    msg.header.stamp = node.get_clock().now().to_msg()
    msg.header.frame_id = "camera"
    msg.height, msg.width = frame.shape[:2]
    msg.encoding = "bgr8"
    msg.step = msg.width * 3
    msg.data = frame.tobytes()
    return msg


def main():
    if os.path.exists(BAG_NAME):
        sys.exit(f"error: {BAG_NAME}/ already exists — remove it first "
                 f"(rm -rf {BAG_NAME}) and rerun.")

    rclpy.init()
    node = Node("bag_generator")
    pub = node.create_publisher(Image, TOPIC, qos_profile_sensor_data)

    print(f"Recording {SECONDS}s of {TOPIC} into {BAG_NAME}/ ...")
    recorder = subprocess.Popen(
        ["ros2", "bag", "record", TOPIC, "-o", BAG_NAME])
    time.sleep(3.0)  # let the recorder discover the topic

    n_frames = FPS * SECONDS
    for i in range(n_frames):
        pub.publish(to_image_msg(make_frame(i), node))
        time.sleep(1.0 / FPS)

    time.sleep(1.0)  # let the recorder drain
    recorder.send_signal(signal.SIGINT)
    recorder.wait(timeout=15)

    node.destroy_node()
    rclpy.shutdown()
    print(f"\nDone. Inspect it with:  ros2 bag info {BAG_NAME}")
    print(f"Play it back with:      ros2 bag play {BAG_NAME} --loop")


if __name__ == "__main__":
    main()
