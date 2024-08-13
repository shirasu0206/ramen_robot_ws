import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32
from cv_bridge import CvBridge
import cv2
import threading

class UR5RetouchNode(Node):
    def __init__(self):
        super().__init__('ur5_retouch_node')
        self.publisher_ur5_order = self.create_publisher(String, 'ur5_order', 10)
        self.publisher_ur5_arrival = self.create_publisher(String, 'ur5_arrival', 10) 
        self.notify_ur5()
        self.send_ur5_signal()
        
    def notify_ur5(self):
        msg = String()
        msg.data = f"agv1 arrived at F"
        self.publisher_ur5_arrival.publish(msg)
        self.get_logger().info(f'Notified UR5: {msg.data}')

    def send_ur5_signal(self):
        msg = String()
        msg.data = f"agv arrived at F with 2 orders"
        self.publisher_ur5_order.publish(msg)
        self.get_logger().info(f'Sent UR5 signal: {msg.data}')
  
def main(args=None):
    rclpy.init(args=args)
    node = UR5RetouchNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

