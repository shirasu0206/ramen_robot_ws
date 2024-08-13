import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import threading

class AccountantNode(Node):
    def __init__(self):
        super().__init__('accountant_node')
        self.publisher_ = self.create_publisher(Int32, 'ramen_order_count', 10)
        self.get_logger().info('Accountant Node has been started.')
        threading.Thread(target=self.input_thread, daemon=True).start()

    def input_thread(self):
        while True:
            try:
                count = int(input("ラーメンの購入個数を入力してください: "))
                self.publish_ramen_count(count)
            except ValueError:
                self.get_logger().error("入力が間違っています。整数を入れてください.")

    def publish_ramen_count(self, count):
        while count > 0:
            publish_count = min(2, count)
            msg = Int32()
            msg.data = publish_count
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: {publish_count}')
            count -= publish_count

def main(args=None):
    rclpy.init(args=args)
    node = AccountantNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
