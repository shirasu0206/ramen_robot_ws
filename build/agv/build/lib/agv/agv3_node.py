import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep

class AGVNode(Node):
    def __init__(self, name, initial_position):
        super().__init__(name)
        self.subscription = self.create_subscription(String, 'agv_command', self.command_callback, 10)
        self.publisher_arrival = self.create_publisher(String, 'agv_arrival', 10)
        self.current_position = initial_position
        self.get_logger().info(f'{name}を起動しました。')

    def command_callback(self, msg):
        command = msg.data
        try:
            agv_id, action, _, position = command.split()  # '_' は 'to' に対応してるはず
            if self.get_name() == agv_id and action == 'move':
                self.get_logger().info(f'{agv_id}が{position}に移動中。。。')
                sleep(5)  # 5秒間のインターバル(agvが実際に動くとして適当な時間で空けてる)
                self.current_position = position
                self.publish_arrival(agv_id, position)
        except ValueError as e:
            self.get_logger().error(f'Invalid command format: {command}. Error: {e}')

    def publish_arrival(self, agv_id, position):
        msg = String()
        msg.data = f'{agv_id} {position}'
        self.publisher_arrival.publish(msg)
        self.get_logger().info(f'{agv_id}が{position}に到着しました。')

def main(args=None):
    rclpy.init(args=args)
    
    agv3_node = AGVNode('agv3', 'B')
    
    rclpy.spin(agv3_node)
    
    agv3_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

