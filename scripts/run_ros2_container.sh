#!/usr/bin/env bash
set -euo pipefail

# Launch a ROS 2 Jazzy development container with user-matched UID/GID so
# files created inside remain editable on the host.
#
# Usage:
#   scripts/run_ros2_container.sh [additional docker args]
#
# Environment variables:
#   ROS2_IMAGE    Override the container image (default: ros2-jazzy:latest)
#   CONTAINER_WS  Override the container workspace path (default: /workspace/zwarm)

PROJECT_ROOT=$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel 2>/dev/null || pwd)
IMAGE=${ROS2_IMAGE:-ros2-jazzy:latest}
CONTAINER_WS=${CONTAINER_WS:-/workspace/zwarm}
HOST_UID=$(id -u)
HOST_GID=$(id -g)
HOST_USER=${USER:-developer}
HOST_HOME="/home/${HOST_USER}"

DOCKER_ARGS=(
  --rm
  -it
  --network host
  -v "${PROJECT_ROOT}:${CONTAINER_WS}"
  -w "${CONTAINER_WS}"
  -e HOST_UID="${HOST_UID}"
  -e HOST_GID="${HOST_GID}"
  -e HOST_USER="${HOST_USER}"
  -e HOST_HOME="${HOST_HOME}"
)

# Allow caller to append extra docker run args (ports, devices, etc.)
DOCKER_ARGS+=("$@")

exec docker run "${DOCKER_ARGS[@]}" "${IMAGE}" bash -lc '
set -euo pipefail

uid=${HOST_UID:-1000}
gid=${HOST_GID:-1000}
username=${HOST_USER:-developer}
home=${HOST_HOME:-/home/developer}

existing_group=$(getent group "${gid}" | cut -d: -f1 || true)
if [ -z "${existing_group}" ]; then
    group_name="${username}"
    if getent group "${group_name}" >/dev/null 2>&1; then
        group_name="zwarm-dev-${gid}"
    fi
    groupadd -g "${gid}" "${group_name}"
else
    group_name="${existing_group}"
fi

existing_user=$(getent passwd "${uid}" | cut -d: -f1 || true)
if [ -z "${existing_user}" ]; then
    useradd -m -d "${home}" -u "${uid}" -g "${group_name}" "${username}"
    existing_user="${username}"
else
    username="${existing_user}"
    home=$(getent passwd "${existing_user}" | cut -d: -f6)
fi

if [ ! -d "${home}" ]; then
    mkdir -p "${home}"
    chown "${uid}:${gid}" "${home}"
fi

export HOME="${home}"
export USER="${username}"
exec su --preserve-environment - "${username}"
'
