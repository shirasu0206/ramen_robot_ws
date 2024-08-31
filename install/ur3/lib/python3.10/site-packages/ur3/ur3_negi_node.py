import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Float32
import socket
import time
import sys  
import os
sys.path.append(os.path.expanduser('~/workspaces/ramen_robot_ws/ur_control'))
from ur_listener import UrListener

class UR3NegiNode(Node):
    def __init__(self):
        super().__init__('ur3_negi_node')
        self.subscription_count = self.create_subscription(Int32, 'ur3_order_count', self.count_callback, 10)
        self.subscription_arrival = self.create_subscription(String, 'agv_arrival', self.arrival_callback, 10)
        self.subscription_depth = self.create_subscription(Float32, 'negi_depth', self.depth_callback, 10)
        self.subscription_posN = self.create_subscription(Int32,'posN', self.posN_callback, 10)
        self.publisher_soup = self.create_publisher(String, 'ur3_soup_signal', 10)
        self.current_order_count = None
        self.agv_at_E = False
        self.negi_depth = None
        self.posN = None
        self.get_logger().info('UR3 Negi Nodeが起動しました。')
        self.HOST = "192.168.56.2"
        self.PORT = 30002
        self.current_order = None

    def to_bytes(self, string):
        return bytes(string.encode())
        
    def wait_till_stop(self, listener):
        # ロボットが停止するまでループ
        while not listener.get_robot_state():
            self.get_logger().info('UR3動作中。。。')
            time.sleep(1)
        self.get_logger().info('UR3動作終了')

    def count_callback(self, msg):
        self.current_order_count = msg.data
        self.current_order = msg.data  # self.current_order を設定
        self.get_logger().info(f'受信した注文数：{self.current_order_count}')
        self.check_and_start_cooking()

    def arrival_callback(self, msg):
        agv_id, position = msg.data.split(' ')
        if position == 'E':
            self.agv_at_E = True
            self.get_logger().info('AGVが位置Eに到着しました。')
            self.check_and_start_cooking()
            
    def depth_callback(self, msg):
        self.negi_depth = msg.data
        self.get_logger().info(f'最新のネギの深さ：{self.negi_depth}')
        self.check_and_start_cooking()
    def posN_callback(self, msg):
        self.posN = msg.data
        self.get_logger().info(f'最も浅い位置ナンバー：{self.posN}')
        self.check_and_start_cooking()
    def check_and_start_cooking(self):
        if self.current_order_count is not None:
            if not self.agv_at_E:
                self.get_logger().info('AGVが位置Eに到着していません。')
            if self.negi_depth is None:
                self.get_logger().info('ネギの深さが取得されていません。')
            if self.agv_at_E and self.negi_depth is not None:
                self.get_logger().info(f'{self.current_order_count}杯を調理中。。。')
                self.execute_negi_task()
                self.reset_state()
    
    def execute_negi_task(self):
        self.get_logger().info(f'ネギの調理開始、調理数：{self.current_order}杯')
        self.get_logger().info(f'ネギの深さ：{self.negi_depth}')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        listener = UrListener(s)  # UrListenerのインスタンスを作成
        if self.negi_depth >= 0.500:
            self.negi_depth = 0.480
        
        ur_script = (
            "def myProg():" + "\n"
            + "set_tcp(p[0,0,0,0,0,0])" + "\n"
            + "movej(p[-0.181, -0.276, 0.072, 2.213, -2.197, 0], a=3, v=1.5)" + "\n"  # start position
            + "movel(p[-0.020, -0.276, 0.072, 2.213, -2.197, 0], a=1, v=0.3)" + "\n"  # change negi tool
            + "movel(p[-0.020, -0.276, 0.391, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            + "movel(p[0.024, -0.415, 0.391, 2.213, -2.197, 0], a=3, v=1.5)" + "\n"
            + "pos0a = get_actual_tcp_pose()" + "\n"
            + f"pos0b = pose_add(pos0a,p[0,0,-0.05,0,0,0])" + "\n"
            + "movel(pos0b,a=1,v=0.1)" + "\n"
            + "sleep(1.)" + "\n"
            )       
        if self.posN ==0 and self.negi_depth < 0.500:
            ur_script +=(
                f"pos0c = pose_add(pos0b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                + "sleep(1.)" + "\n"
                "movel(pos0c,a=3, v=1.5)" + "\n"
            )
        elif self.posN ==1 and self.negi_depth < 0.500:
            ur_script +=(
                "pos1b = pose_add(pos0b,p[0.02,0,0,0,0,0])" + "\n"
                + f"pos1c = pose_add(pos1b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                + "movel(pos1b,a=1,v=0.1)" + "\n"
                + "sleep(1.)" + "\n"
                + "movel(pos1c,a=3,v=1.5)" + "\n"
                )
        elif self.posN ==2 and self.negi_depth < 0.500:
            ur_script +=(
                "pos2b = pose_add(pos0b,p[-0.02,0,0,0,0,0])" + "\n"
                + f"pos2c = pose_add(pos2b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                + "movel(pos2b,a=1,v=0.1)" + "\n"
                + "sleep(1.)" + "\n"
                + "movel(pos2c,a=3,v= 1.5)" + "\n"
                )
        elif self.posN == 3 and self.negi_depth < 0.500:
            ur_script +=(
                "pos3b = pose_add(pos0b,p[0.02,0,0,0,0,-1.57])" + "\n"
                + f"pos3c = pose_add(pos3b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                + "movel(pos3b,a=1,v=0.1)" + "\n"
                + "sleep(1.)" + "\n"
                + "movel(pos3c,a=3,v=1.5)" + "\n"
                )
        elif self.posN == 4 and self.negi_depth < 0.500:
            ur_script +=(
                "pos4b = pose_add(pos0b,p[0.02,0,0,0,0,-1.57])" + "\n"
                + f"pos4c = pose_add(pos4b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                + "movel(pos4b,a=1,v=0.1)" + "\n"
                + "sleep(1.)" + "\n"
                + "movel(pos4c,a=3,v=1.5)" + "\n"
                )
               
        ur_script +=(
            #"set_digital_out(0,True)" + "\n" # negi pick 1
            "sleep(2.)" + "\n"
            + "movel(p[0.038, -0.415, 0.391, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            + "sleep(1.)" + "\n"
            + "movel(p[0.337, -0.064, 0.391, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            + "movel(p[0.337, -0.064, 0.310, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            + "set_digital_out(0,False)" + "\n"  # negi place 1
            + "sleep(2.)" + "\n"
            + "movel(p[0.337, -0.064, 0.360, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            )
        if self.current_order == 2:
            ur_script += (
                # 2つ目のネギのピック＆プレース
                "movel(p[0.024, -0.415, 0.391, 2.214, -2.196, 0], a=3, v=1.5)" + "\n"
                + "pos0a = get_actual_tcp_pose()" + "\n"
                + f"pos0b = pose_add(pos0a,p[0,0,-0.05,0,0,0])" + "\n"
                + "movel(pos0b,a=1,v=0.1)" + "\n"
                + "sleep(1.)" + "\n"
                )       
            if self.posN ==0 and self.negi_depth < 0.500:
                ur_script +=(
                    f"pos0c = pose_add(pos0b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                    + "sleep(1.)" + "\n"
                    "movel(pos0c,a=3, v=1.5)" + "\n"
                )
            elif self.posN ==1 and self.negi_depth < 0.500:
                ur_script +=(
                    "pos1b = pose_add(pos0b,p[0.02,0,0,0,0,0])" + "\n"
                    + f"pos1c = pose_add(pos1b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                    + "movel(pos1b,a=1,v=0.1)" + "\n"
                    + "sleep(1.)" + "\n"
                    + "movel(pos1c,a=3,v=1.5)" + "\n"
                    )
            elif self.posN ==2 and self.negi_depth < 0.500:
                ur_script +=(
                    "pos2b = pose_add(pos0b,p[-0.02,0,0,0,0,0])" + "\n"
                    + f"pos2c = pose_add(pos2b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                    + "movel(pos2b,a=1,v=0.1)" + "\n"
                    + "sleep(1.)" + "\n"
                    + "movel(pos2c,a=3,v= 1.5)" + "\n"
                    )
            elif self.posN == 3 and self.negi_depth < 0.500:
                ur_script +=(
                    "pos3b = pose_add(pos0b,p[0,0.02,0,0,0,0])" + "\n"
                    + f"pos3c = pose_add(pos3b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                    + "movel(pos3b,a=1,v=0.1)" + "\n"
                    + "sleep(1.)" + "\n"
                    + "movel(pos3c,a=3,v=1.5)" + "\n"
                    )
            elif self.posN == 4 and self.negi_depth < 0.500:
                ur_script +=(
                    "pos4b = pose_add(pos0b,p[0,0.02,0,0,0,0])" + "\n"
                    + f"pos4c = pose_add(pos4b,p[0,0,{0.425 - self.negi_depth},0,0,0])" + "\n"
                    + "movel(pos4b,a=1,v=0.1)" + "\n"
                    + "sleep(1.)" + "\n"
                    + "movel(pos4c,a=3,v=1.5)" + "\n"
                    )
            ur_script +=(
                #"set_digital_out(0,True)" + "\n"  # negi pick 2
                "sleep(2.)" + "\n"
                + "movel(p[0.024, -0.415, 0.391, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
                + "movel(p[0.337, -0.234, 0.391, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
                + "movel(p[0.337, -0.234, 0.310, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
                + "set_digital_out(0,False)" + "\n"  # negi place 2
                + "sleep(2.)" + "\n"
                )
            
        ur_script += (
            "movel(p[-0.014, -0.275, 0.310, 2.213, -2.197, 0], a=3, v=1.5)" + "\n"
            + "movel(p[-0.014, -0.275, 0.072, 2.214, -2.197, 0], a=3, v=1.5)" + "\n"
            + "movel(p[-0.181, -0.276, 0.072, 2.214, -2.197, 0], a=1, v=0.3)" + "\n"  # start position
            + "end" + "\n"  
        )

        s.send(self.to_bytes(ur_script))
        
        # Wait for the robot to stop
        self.wait_till_stop(listener)
    
        data = s.recv(1000000)
        s.close()
        #self.get_logger().info(f"Received: {repr(data)}") #ur側にデータが遅れたかどうか確認する用
        self.get_logger().info("ネギの調理を終了しました")
        self.send_signal()

    def send_signal(self):
        if self.current_order is not None:
            msg = String()
            msg.data = f"negi_done {self.current_order}"
            self.publisher_soup.publish(msg)
            self.get_logger().info('ur3_soup_nodeに信号を送りました')
        #else:
            #self.get_logger().error('Current order is None, cannot send signal.')

    def reset_state(self):
        self.current_order_count = None
        self.agv_at_E = False
        self.negi_depth = None

def main(args=None):
    rclpy.init(args=args)
    node = UR3NegiNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

