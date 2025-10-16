# Swarm Coordination Plan

This plan focuses on lightweight logic that reacts to confirmed detections and coordinates basic multi-drone maneuvers through a simple drone auction protocol.

## Objectives
- Track drone availability and simple capabilities (e.g., camera payload, remaining battery).
- When the operator confirms a detection, launch an auction that lets drones volunteer for follow-up.
- Keep the operator in the loop by routing bids for approval before missions start.
- Send follow-up waypoint/missions to the winning drone while avoiding conflicts with other aircraft.
- Validate auction and mission behaviors in simulation before sending to the real fleet.
- Maintain a single source of truth for ROS 2 interfaces via `packages/common/zwarm_msgs/`.

## Milestones

### M1. Message Definitions
- Expand `packages/common/zwarm_msgs/` with messages/services for `DroneStatus`, `DetectionEvent`, `AuctionEvent`, `AuctionBid`, `AuctionResult`, and `MissionCommand`.
- Document topic names, expected publish rates, and QoS settings.
- Provide sample messages in `resources/datasets/` for manual testing.

### M2. Auction Coordinator (backend)
- Implement ROS 2 node (likely within the backend) that listens for confirmed detections and creates auction events.
- Publish auction announcements to drones and collect incoming bids.
- Score bids (distance, battery, current load) and rank them for operator review.
- Timeout auctions gracefully if no bids arrive.

### M3. Operator Approval Loop
- Expose auction state through the backend API/WebSocket so the dashboard can display bids.
- Accept operator approval/denial and publish `AuctionResult` messages back onto ROS 2.
- Notify losing bidders about the outcome so they can stand down.

### M4. Follow-Up Task Execution
- On approval, translate the winning bid into a `MissionCommand` for the chosen drone.
- Track acceptance/ack via PX4 telemetry and update mission status.
- Add a safety timeout that cancels the mission if acknowledgements stop arriving.

### M5. Collision Awareness (Minimal)
- Keep a rolling list of planned waypoints for each drone.
- If two missions would bring drones within a configurable radius, adjust the auction outcome (e.g., prefer a farther drone or insert a loiter command).
- Log these adjustments for later tuning.

### M6. Simulation Loop
- Reuse `packages/sim/` SITL setup to spawn at least two drones with auction clients enabled.
- Script scenarios where detections trigger auctions, operators approve bids, and drones execute missions.
- Collect metrics (mission completion time, nearest distance between drones, bid latency) and document results.

## Deliverables
- Shared message/package definitions under `packages/common/zwarm_msgs/` used by edge, backend, and dashboard code.
- Auction coordinator logic integrated into the backend service.
- Simulation demos and short write-up in `resources/hardware-notes/` or a dedicated `docs/` page.
