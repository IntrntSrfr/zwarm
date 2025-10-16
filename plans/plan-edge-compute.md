# On-Drone Edge Compute Plan

This plan covers the ROS 2 nodes that run directly on each Raspberry Pi 5 drone.

## Objectives
- Capture camera frames and expose both raw and detection-overlay video streams.
- Run Hailo-accelerated object detection with a simple toggling interface.
- Exchange telemetry and basic commands with PX4 via ROS 2.
- Participate in the drone auction protocol by announcing availability, submitting bids, and receiving approved tasks.
- Share message/service definitions with the backend via `packages/common/zwarm_msgs/`.
- Package everything so a fresh Pi can be set up with minimal manual work.

## Milestones

### M1. Bring-Up Basics
- Flash Raspberry Pi OS (64-bit) and install ROS 2 Humble.
- Install Hailo drivers/SDK and verify a sample model runs on the hat.
- Hook up the Pi Camera Module 3 and confirm frame capture using `libcamera`.
- Build the shared message package (`packages/common/zwarm_msgs/`) as part of the edge workspace.
- Commit setup steps and helper scripts under `resources/hardware-notes/`.

### M2. Camera Publisher
- Create a ROS 2 workspace in `packages/edge/` (e.g., `zwarm_edge_ws`) that overlays the shared messages.
- Implement `zwarm_camera_node` (C++ or Python) that publishes `sensor_msgs/Image`.
- Add launch file with adjustable resolution/FPS parameters.
- Record a short rosbag and stash it in `resources/datasets/` for testing.

### M3. Hailo Detection Overlay
- Choose/convert a small detection model (YOLOv5n or similar) for Hailo.
- Implement `zwarm_hailo_detector` node that subscribes to camera frames and publishes detections (`vision_msgs/Detection2DArray`).
- Add an overlay node that composites bounding boxes onto the video stream.
- Expose a ROS 2 service or parameter to switch between raw and overlay output.

### M4. PX4 Interface & Telemetry
- Use `px4_ros_com` (or MAVROS 2) to pull pose, battery, and heartbeat data.
- Publish a combined status topic (`zwarm_msgs/DroneStatus`) for the backend/dashboard.
- Expose a minimal command interface (velocity or mission waypoint) for follow-up tasks.
- Add failsafe hooks (e.g., heartbeat watchdog that triggers PX4 RTL).

### M5. Auction Participant Node
- Implement `zwarm_auction_client` that listens for auction announcements (`zwarm_msgs/AuctionEvent`).
- Evaluate tasks locally (distance, capability) and publish bids (`zwarm_msgs/AuctionBid`).
- Accept operator-approved awards, trigger mission execution, or decline politely if conditions change.
- Log auction participation for debugging and replay in simulation.

### M6. Startup & Packaging
- Create launch files that start camera, detector, PX4 bridge, and auction client together.
- Add a systemd service or simple bash script to auto-start the stack on boot.
- Document troubleshooting steps (thermal throttling, USB bandwidth, etc.).

## Deliverables
- ROS 2 packages inside `packages/edge/` with build instructions and dependency on `zwarm_msgs`.
- Launch/config files demonstrating raw vs detection streaming and auction participation.
- Sample bag files and notes for replaying them in simulation.
- Markdown setup guide in `resources/hardware-notes/edge-setup.md`.
