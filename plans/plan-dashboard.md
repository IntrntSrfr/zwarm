# Operator Dashboard Plan

This plan outlines the user interface and lightweight backend needed to observe the fleet and approve follow-up missions.

## Objectives
- Display the list of drones with basic status info (connected, battery, mission state).
- Stream live video from selected drones with a raw/detection toggle.
- Alert the operator when a drone flags a detection. The drone should launch an
  "auction" in which any drone can accept a follow-up task, where the latter drone
  asks for the operators permission. The operator's response is captured and sent
  to the second drone, either allowing it or not allowing it to do the task.
- Send a simple follow-up task back to another drone through the ROS2 drone auction system.
- Reuse the shared ROS 2 interfaces from `packages/common/zwarm_msgs/` so edge and backend stay in sync.

## Milestones

### M1. UX Sketch & Data Contracts
- Roughly sketch the fleet overview and per-drone view (pen-and-paper or Figma).
- Define the minimal JSON payloads for drones, detections, and missions.
- Document topic/API mappings in `plans/plan-dashboard.md` as they evolve.

### M2. Backend Bridge (packages/backend/)
- Scaffold a small FastAPI service that talks to ROS 2 via `rclpy`.
- Build/install `packages/common/zwarm_msgs/` in the backend environment for shared message types.
- Expose REST endpoints: `/drones`, `/detections`, `/missions`.
- Add a WebSocket endpoint for push updates to the dashboard.
- Store state in memory first; plan for SQLite if persistence becomes useful.

### M3. Dashboard UI (packages/dashboard/)
- Create a simple SPA (React/Vite) with routes for Fleet and Drone detail views.
- Show status cards, map placeholder (Leaflet), and telemetry readouts.
- Integrate the video player using WebRTC/RTSP; start with plain MJPEG if easier.
- Add controls for raw/detection toggle and mission dispatch.

### M4. Detection Review Workflow
- Render detection alerts in the UI with snapshot/metadata.
- Allow operator to confirm or dismiss and log the decision.
- On confirmation, send a message to the drone auction task system, notifying of
  an open task that anyone can do. A drone can then respond, and a dialog to
  either allow or deny that drone from taking on the task is shown, which responds
  to the request.
- Display mission timeline so the operator can see progress.

### M5. Polishing & Deploy Scripts
- Provide scripts and Docker Compose for running dashboard and backend together.
- Write a README in each package folder explaining setup, config, and dev workflow.
- Capture demo scenarios (screen recordings or screenshots) for documentation.

## Deliverables
- Backend service in `packages/backend/` with REST + WS API and ROS 2 integration using `zwarm_msgs`.
- Frontend app in `packages/dashboard/` with live video and detection review.
- Documentation for running both locally and connecting to real/simulated drones.
