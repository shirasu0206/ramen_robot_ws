import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from collections import deque
class AGVCommander(Node):
    def __init__(self):
        super().__init__('agv_commander')
        self.publisher_ur3_order = self.create_publisher(String, 'ur3_order', 10)
        self.publisher_ur5_order = self.create_publisher(String, 'ur5_order', 10)
        self.publisher_command = self.create_publisher(String, 'agv_command', 10)
        self.publisher_ur5_arrival = self.create_publisher(String, 'ur5_arrival', 10)  # UR5への到着通知パブリッシャーを追加
        self.positions = ['F','E','D','C','B','A']
        #self.agv_positions = {'agv1': 'A','agv2': 'B'}
        self.agv_positions = {'agv1': 'A'}
        self.agv_moving = False
        self.ur5_done = False
        self.ur3_done = False
        self.order_queue = deque()
        self.processing_order = False
        self.ur3_processing = False
        self.ur5_processing = False
        self.create_subscription(String, 'ur5_done', self.ur5_callback, 10)
        self.create_subscription(String, 'ur3_done', self.ur3_callback, 10)
        self.create_subscription(Int32, 'ramen_order_count', self.order_callback, 10)
        self.create_subscription(String, 'agv_arrival', self.agv_arrival_callback, 10)
        self.timer = self.create_timer(1.0, self.check_and_move_agvs)
    def order_callback(self, msg):
        self.get_logger().info(f'Received order count message: {msg.data}')
        self.order_queue.append(msg.data)
        self.get_logger().info(f'Current order queue: {list(self.order_queue)}')
        self.process_next_order()
    def ur5_callback(self, msg):
        self.ur5_done = True
        self.ur5_processing = False
        self.process_next_order()
    def ur3_callback(self, msg):
        self.ur3_done = True
        self.ur3_processing = False
        self.process_next_order()
    def agv_arrival_callback(self, msg):
        agv_id, position = msg.data.split(' ')
        self.agv_positions[agv_id] = position
        self.agv_moving = False  # AGVが到着したら移動中フラグをリセット
        self.get_logger().info(f'Received arrival confirmation: {agv_id} at {position}')
        if position == 'F':
            self.notify_ur5(agv_id, position)  # UR5にAGVがFに到着したことを通知
        self.process_next_order()
    def process_next_order(self):
        if not self.processing_order and self.order_queue:
            self.processing_order = True
            if not self.ur5_processing and not self.ur3_processing:  # 両方が処理中でない場合
                #if self.agv_positions['agv1'] == 'F' or self.agv_positions['agv2'] == 'F':  # AGV1がF地点にいるか確認
                if self.agv_positions['agv1'] :
                    self.current_order_count = self.order_queue.popleft()
                    self.send_ur5_signal()
            self.processing_order = False
        # AGVの移動
        if self.ur5_done:
            if self.agv_positions['agv1'] == 'F' and not self.agv_moving:
                self.move_agv('agv1', 'E')
            self.ur5_done = False
            #if self.agv_positions['agv2'] == 'F' and not self.agv_moving:
             #   self.move_agv('agv2', 'E')
            #self.ur5_done = False
        if self.ur3_done:
            if self.agv_positions['agv1'] == 'E' and not self.agv_moving:
                self.move_agv('agv1', 'D')
            self.ur3_done = False
            #if self.agv_positions['agv2'] == 'E' and not self.agv_moving:
            #    self.move_agv('agv2', 'D')
            #self.ur3_done = False
    def check_and_move_agvs(self):
        if not self.agv_moving:
            if self.agv_positions['agv1'] == 'A' and 'F' not in self.agv_positions.values():
                self.move_agv('agv1', 'F')
            if self.agv_positions['agv1'] == 'D' and 'C' not in self.agv_positions.values():
                self.move_agv('agv1', 'C')
            if self.agv_positions['agv1'] == 'C' and 'B' not in self.agv_positions.values():
                self.move_agv('agv1', 'B')
            if self.agv_positions['agv1'] == 'B' and 'A' not in self.agv_positions.values():
                self.move_agv('agv1', 'A')
                '''
            if self.agv_positions['agv2'] == 'A' and 'F' not in self.agv_positions.values():
                self.move_agv('agv2', 'F')
            if self.agv_positions['agv2'] == 'D' and 'C' not in self.agv_positions.values():
                self.move_agv('agv2', 'C')
            if self.agv_positions['agv2'] == 'C' and 'B' not in self.agv_positions.values():
                self.move_agv('agv2', 'B')
            if self.agv_positions['agv2'] == 'B' and 'A' not in self.agv_positions.values():
                self.move_agv('agv2', 'A')
                '''
    def move_agv(self, agv_id, next_pos):
        if self.agv_positions[agv_id] != next_pos and next_pos not in self.agv_positions.values():
            command = f"{agv_id} move to {next_pos}"
            msg = String()
            msg.data = command
            self.publisher_command.publish(msg)
            self.get_logger().info(f'Command sent: {command}')
            self.agv_moving = True  # 移動コマンドを送信したら移動中フラグを設定
    def notify_ur5(self, agv_id, position):
        msg = String()
        msg.data = f"{agv_id} arrived at {position}"
        self.publisher_ur5_arrival.publish(msg)
        self.get_logger().info(f'Notified UR5: {msg.data}')
    def send_ur3_signal(self):
        if self.current_order_count > 0:
            self.ur3_processing = True
            msg = String()
            msg.data = f"agv arrived at E with {self.current_order_count} orders"
            self.publisher_ur3_order.publish(msg)
            self.get_logger().info(f'Sent UR3 signal: {msg.data}')
    def send_ur5_signal(self):
        if self.current_order_count > 0:
            self.ur5_processing = True
            msg = String()
            msg.data = f"agv arrived at F with {self.current_order_count} orders"
            self.publisher_ur5_order.publish(msg)
            self.get_logger().info(f'Sent UR5 signal: {msg.data}')
def main(args=None):
    rclpy.init(args=args)
    agv_commander = AGVCommander()
    rclpy.spin(agv_commander)
    agv_commander.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
