# Assignment 2 — Starter Code

Read the assignment handout first. This README covers only the code.

## Layout

```
code/
├── generate_bag.py              # run once to create camera_bag/ (Task 3)
├── python/edge_detector/        # Python skeleton — pick this OR the C++ one
│   ├── package.xml
│   ├── setup.py / setup.cfg / resource/
│   └── edge_detector/edge_detector_node.py   # 3 TODOs
└── cpp/edge_detector_cpp/       # C++ skeleton — pick this OR the Python one
    ├── package.xml
    ├── CMakeLists.txt           # complete — no changes needed
    └── src/edge_detector_node.cpp             # 3 TODOs
```

Pick **one** language. Copy that package folder (e.g. `python/edge_detector/`)
into your workspace's `src/` directory. Grep for the TODOs:
`grep -rn TODO src/`

## Prerequisites

```
sudo apt install python3-opencv ros-jazzy-cv-bridge \
    ros-jazzy-rqt-image-view ros-jazzy-rqt-graph
```


## Suggested order

1. Build the skeleton as-is first (`colcon build`, then
   `source install/setup.bash`) and make sure it runs before touching TODOs.

2. Generate the bag from your workspace root:
   `python3 ../code/generate_bag.py` (needs your ROS 2 environment
   sourced). Do not commit/submit the bag — anyone can regenerate it.

3. Play it in a loop and explore with `ros2 topic` / `rqt_image_view` before
   writing any code. Especially:
   `ros2 topic info /camera/image_raw --verbose` — save its output to
   `qos_diagnosis.txt`, a graded deliverable.

4. Fill in the TODOs one at a time. TODO(2) — the subscription QoS — is the
   heart of the assignment: with the provided QoS profile your callback does
   not receive messages. Read your logs and use the tools from the handout to
   diagnose the issue. Welcome to DDS.

5. Verify: `ros2 topic hz /camera/edges` ≈ 10 Hz, view it in `rqt_image_view`,
   and change thresholds live with
   `ros2 param set /edge_detector canny_high 10000`.

## Hints

- `mono8` means a single-channel 8-bit image — exactly what `Canny` returns.

- If `ros2 run` can't find your executable, you probably forgot to
  `source install/setup.bash` after building.

- Bonus (`edge_stats`): no skeleton — copy the structure of your main node.
  Count edge pixels with `cv2.countNonZero` / `cv::countNonZero` and publish
  `std_msgs/Int32` on `/camera/edge_count`. Its subscription needs a plain
  default QoS — think about why that works here when it didn't for the bag.