import rclpy
from rclpy.node import Node

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.get_logger().info('Camera node stub running')

    def spin(self):
        rclpy.spin(self)


def main():
    rclpy.init()
    node = CameraNode()
    node.spin()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
