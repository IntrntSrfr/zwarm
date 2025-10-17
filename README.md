# ZWARM Hobby Drone Swarm Project

ZWARM is a personal project exploring how a small fleet of Raspberry Pi 5 drones (with Hailo AI hats and Pi Camera Module 3 sensors) can share video, detect interesting events, and cooperate on follow-up missions using ROS 2 and PX4.

The goal is to keep things practical for an internship-scale build while leaving room to experiment with new ideas like drone-to-drone task auctions.

## Project Scope

- Monitor multiple drones from a simple browser-based dashboard.
- Stream each drone's camera feed and toggle between raw video and detection overlays.
- Let a human confirm detections while a lightweight drone auction proposes follow-up responders.
- Keep the operator in the loop as drones negotiate tasks, approving/denying bids before execution.
- Experiment with basic swarm behaviors such as collision-aware path adjustments.

## Repository Structure (Working Draft)

```
README.md
plans/
  plan-edge-compute.md       # On-drone ROS 2 stack and video/inference nodes
  plan-dashboard.md          # Operator dashboard, backend bridge, and auction UX
  plan-swarm-coordination.md # Mission handoffs, drone auction logic, and multi-drone behavior
  plan-operations.md         # Dev tools, provisioning scripts, and testing setup
docs/
  architecture.md            # End-to-end component diagrams and data flows
packages/
  common/
    zwarm_msgs/              # Shared ROS 2 interfaces used by edge, backend, and auction nodes
  edge/                      # ROS 2 workspace for Pi-side nodes (to be added)
  backend/                   # Small FastAPI (or similar) service + ROS 2 bridge
  dashboard/                 # Web UI (React/Svelte) with WebRTC/WS clients
  sim/                       # PX4 SITL + Gazebo scenes and test harness
resources/
  hardware-notes/            # Wiring, calibration, and field checklists
  datasets/                  # Sample recordings and detection model assets
```

> **Note:** Only the documentation exists right now. Code directories will be added as the project matures.

## How It Fits Together

1. **Edge Nodes (ROS 2)** capture video, run Hailo detections, publish telemetry, and listen for auction announcements/bids.
2. **Shared Messages** live in `packages/common/zwarm_msgs/` so every component uses identical ROS 2 message/service definitions.
3. **Backend Bridge** subscribes to ROS 2 topics, exposes a REST/WebSocket API, tracks auctions, and relays operator approvals.
4. **Dashboard** displays fleet status, plays live streams (WebRTC/RTSP), shows auction bids, and lets the operator approve or decline drone proposals.
5. **Coordination Logic** launches auctions when detections are confirmed, scores bids, and issues follow-up tasks while keeping drones separated.
6. **Simulation Setup** mirrors the real system so new ideas (including auction mechanics) can be tested safely before field flights.

## Getting Started

1. Read through the plans in `plans/` to understand the proposed approach for each piece.
2. Bring up the simulation stack under `packages/sim/` (once created) to validate ROS 2 topics, auction flow, and video streams.
3. Develop the edge ROS 2 nodes on a single Raspberry Pi and confirm camera + detection switching works.
4. Build the dashboard + backend loop, then iterate toward the multi-drone auction behaviors.

## Contribution Notes

- Keep configs and launch files under version control so setups remain reproducible.
- Document ROS 2 message types, topics, services, and auction flows as they are added to `packages/common/zwarm_msgs/`.
- Prefer small, testable modules and include simulation tests where possible.
- Use the `resources/` folder for hardware-specific instructions, calibration data, and demo assets.

## License

To be decided.
