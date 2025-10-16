#!/usr/bin/env python3
"""Remove default ROS 2 package template test artifacts.

Run this after using ``ros2 pkg create`` to delete the auto-generated
lint/copyright tests and any related config stubs.

Usage:
    python scripts/strip_ros2_template.py [--packages-root PATH]

The script is idempotent and safe to rerun.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

DEFAULT_PACKAGES_ROOT = Path("packages/edge/zwarm_edge_ws/src")


def find_packages(root: Path) -> list[Path]:
    packages: list[Path] = []
    if not root.exists():
        return packages
    for item in root.iterdir():
        if not item.is_dir():
            continue
        if (item / "package.xml").exists():
            packages.append(item)
    return packages


def remove_test_directory(package_path: Path) -> bool:
    test_dir = package_path / "test"
    if test_dir.exists():
        shutil.rmtree(test_dir)
        return True
    return False


def clean_setup_cfg(package_path: Path) -> bool:
    cfg_path = package_path / "setup.cfg"
    if not cfg_path.exists():
        return False

    original = cfg_path.read_text()

    # Remove [options.extras_require] block entirely (usually holds pytest deps)
    content = re.sub(
        r"\n\[options\.extras_require\][\s\S]*?(?=\n\[|$)",
        "\n",
        original,
    )

    # Collapse multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    if content != original:
        cfg_path.write_text(content)
        return True
    return False


def clean_setup_py(package_path: Path) -> bool:
    setup_path = package_path / "setup.py"
    if not setup_path.exists():
        return False

    original = setup_path.read_text()
    lines = original.splitlines()
    filtered = [line for line in lines if "tests_require" not in line]
    new_content = "\n".join(filtered) + "\n"

    if new_content != original:
        setup_path.write_text(new_content)
        return True
    return False


def strip_package(package_path: Path) -> None:
    removed = False
    removed |= remove_test_directory(package_path)
    removed |= clean_setup_cfg(package_path)
    removed |= clean_setup_py(package_path)
    if removed:
        print(f"[cleaned] {package_path}")
    else:
        print(f"[ok]      {package_path} (no template artifacts found)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packages-root",
        type=Path,
        default=DEFAULT_PACKAGES_ROOT,
        help="Path containing ROS 2 packages (default: %(default)s)",
    )
    args = parser.parse_args()

    root: Path = args.packages_root
    if not root.exists():
        raise SystemExit(f"Packages root '{root}' does not exist")

    packages = find_packages(root)
    if not packages:
        print(f"No ROS 2 packages found under {root}")
        return

    for package in packages:
        strip_package(package)


if __name__ == "__main__":
    main()
