# Operations & Tooling Plan

This plan keeps the project manageable for a small team by focusing on repeatable workflows instead of heavy production tooling.

## Objectives
- Make it easy to set up dev machines, edge devices, and the simulation stack.
- Provide scripts for building and running ROS 2 packages, backend, and dashboard.
- Capture useful logs/metrics without standing up a full enterprise observability stack.
- Document checklists for field tests and hardware maintenance.
- Ensure the shared ROS 2 interface package (`packages/common/zwarm_msgs/`) is built consistently across environments, including new auction messages.

## Milestones

### M1. Repo Conventions
- Decide on monorepo layout (current structure) and document workspace setup.
- Add `.editorconfig`, lint configs, and basic formatting scripts for Python/JS/C++.
- Create `Makefile` or `taskfile.yml` with shortcuts (e.g., `make sim`, `make backend`, `make msgs`, `make auction-demo`).

### M2. Dev Environment Setup
- Provide scripts (bash or Ansible-lite) to install ROS 2, Hailo SDK, and dependencies on Ubuntu + Raspberry Pi OS.
- Include steps for building/installing `packages/common/zwarm_msgs/` so both edge and backend nodes share definitions.
- Document VS Code extensions and launch configurations in `resources/hardware-notes/dev-setup.md`.
- Store sample environment variables in `.env.example` per package.

### M3. Testing & Simulation
- Build PX4 SITL + Gazebo/Ignition launch files in `packages/sim/`.
- Create automated tests where practical (pytest for backend, vitest/jest for frontend, ROS 2 launch tests).
- Add integration test that walks through a simulated detection → auction → operator approval → mission execution loop.
- Set up GitHub Actions (or local CI script) that runs lint + unit tests on push, including a job to build `zwarm_msgs`.

### M4. Deployment Shortcuts
- Write a simple deployment script to sync edge package updates to a Pi (e.g., `rsync` + remote build).
- Containerization is optional; document manual steps first, then add Dockerfiles if needed.
- Capture field test checklist (pre-flight checks, log collection) in `resources/hardware-notes/field-checklist.md`.

### M5. Lightweight Observability
- Enable ROS 2 logging to files and ensure logs are easy to retrieve.
- Expose Prometheus-style metrics only if they help debugging; otherwise rely on ROS diagnostics and simple shell scripts.
- Provide instructions for recording rosbags during flights and organizing them under `resources/datasets/`.

## Deliverables
- Setup scripts and helper tooling in the repo root or `resources/`.
- CI configuration (even if minimal) stored in `.github/workflows/`.
- Markdown guides for dev setup, deployment, and field operations.
