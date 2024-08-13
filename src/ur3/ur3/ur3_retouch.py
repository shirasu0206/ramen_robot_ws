import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32
from cv_bridge import CvBridge
import cv2
import threading

class UR3RetouchNode(Node):
    def __init__(self):
        super().__init__('ur3_retouch_node')
        self.publisher_ur3_order = self.create_publisher(String, 'ur3_order', 10)
        self.publisher_ur3 = self.create_publisher(Int32, 'ur3_order_count', 10)
        self.forward_to_ur3()
        self.send_ur3_signal()
    def forward_to_ur3(self):
        order_msg = Int32()
        order_msg.data = 2
        self.publisher_ur3.publish(order_msg)
        self.get_logger().info(f'Published to UR3: {order_msg.data}')
        
    def send_ur3_signal(self):
        msg = String()
        msg.data = f"agv arrived at E with 2 orders"
        self.publisher_ur3_order.publish(msg)
        self.get_logger().info(f'Sent UR3 signal: {msg.data}')
  
def main(args=None):
    rclpy.init(args=args)
    node = UR3RetouchNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

