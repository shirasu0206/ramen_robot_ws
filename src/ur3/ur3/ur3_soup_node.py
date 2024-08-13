import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
import socket
import time
import sys
import os

sys.path.append(os.path.expanduser('~/workspaces/ramen_robot_ws/ur_control'))
from ur_listener import UrListener

class UR3SoupNode(Node):
    def __init__(self):
        super().__init__('ur3_soup_node')
        self.subscription = self.create_subscription(String, 'ur3_soup_signal', self.soup_callback, 10)
        self.publisher_done = self.create_publisher(String, 'ur3_done', 10)  # AGV Commanderに完了信号を送るパブリッシャ
        self.get_logger().info('UR3 Soup Nodeが起動しました。')
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

    def soup_callback(self, msg):
        self.current_order = int(msg.data.split()[-1])
        self.get_logger().info('UR3NegiNodeからの信号を受信、スープの調理を開始')
        self.execute_soup_task()
        self.send_signal()

    def execute_soup_task(self):
        self.get_logger().info('スープの調理開始')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        
        ur_script = (
            "def myProg():" + "\n"
            + "movel(p[-0.341, -0.276, 0.072, 2.244, 2.197, -0.000], a=3, v=1.5)" + "\n"
            + "movel(p[-0.476, -0.276, 0.072, 2.244, 2.197, -0.000], a=1, v=0.3)" + "\n"
            + "movel(p[-0.476, -0.162, 0.072, 2.244, 2.197, 0.036], a=3, v=1.5)" + "\n"
            + "movel(p[-0.326, 0.084, 0.458, 2.867, 1.264, 0.034], a=3, v=1.5)" + "\n"
            + "movel(p[-0.077, 0.248, 0.484, 3.119, 0.207, 0.027], a=3, v=1.5)" + "\n"
            + "movel(p[-0.078, 0.248, 0.152, 3.119, 0.207, 0.027], a=1, v=1.5)" + "\n"
            + "sleep(2.)" + "\n"
            + "movel(p[-0.078, 0.248, 0.411, 3.119, 0.207, 0.027], a=1, v=1.5)" + "\n"
            + "sleep(2.)" + "\n"
            + "movel(p[-0.178, 0.248, 0.411, 3.119, 0.207, 0.427], a=1, v=1.5)" + "\n"
            + "sleep(2.)" + "\n"
            + "movel(p[-0.078, 0.248, 0.411, 3.119, 0.207, 0.027], a=0.5, v=0.2)" + "\n"
            + "sleep(2.)" + "\n"
            + "movel(p[0.134, 0.161, 0.412, 2.765, -1.445, 0.011], a=0.5, v=0.2)" + "\n"
            + "sleep(2.)" + "\n"
            + "set_tcp(p[-0.053,-0.092,0.325,0,0,0])" + "\n"
            + "movel(p[0.339, -0.081, 0.072, 2.182, -2.228, 0.000], a=0.5, v=0.2)" + "\n"
            + "movel(p[0.339, -0.081, 0.072, 1.226, -1.272, 1.186], a=1, v=0.2)" + "\n"
            + "movel(p[0.339, -0.081, 0.072, 2.182, -2.228, -0.000], a=1, v=0.2)" + "\n"
            +"set_tcp(p[0,0,0,0,0,0])" + "\n"
            +"movej(p[-0.025, 0.299, 0.457, 3.125, 0.024, 0.026], a=3, v=1.5)" + "\n"
        )

        if self.current_order == 2:
            ur_script += (
                "set_tcp(p[0,0,0,0,0,0])" + "\n"
                "movej(p[-0.077, 0.248, 0.411, 3.120, 0.207, 0.027], a=3, v=1.5)" + "\n"
                "movel(p[-0.078, 0.248, 0.152, 3.119, 0.207, 0.027], a=1, v=1.5)" + "\n"
                + "sleep(2.)" + "\n"
                "movel(p[-0.077, 0.248, 0.411, 3.120, 0.207, 0.027], a=0.5, v=0.2)" + "\n"
                + "sleep(2.)"
                + "movel(p[-0.177, 0.248, 0.411, 3.120, 0.207, 0.427], a=0.5, v=0.2)" + "\n"
                 "movel(p[-0.177, 0.248, 0.411, 3.120, 0.207, 0.427], a=0.5, v=0.2)" + "\n"
                + "sleep(2.)" + "\n"
                + "movel(p[-0.077, 0.248, 0.411, 3.120, 0.207, 0.027], a=1, v=1.5)" + "\n"
                + "sleep(2.)" + "\n"
                "movel(p[0.083, 0.161, 0.411, 2.975, -0.943, 0.017], a=0.5, v=0.2)" + "\n"
                + "sleep(2.)" + "\n"
                "set_tcp(p[-0.053,-0.092,0.325,0,0,0])" + "\n"
                "movel(p[0.339, -0.250, 0.072, 2.182, -2.228, -0.000], a=0.5, v=0.2)" + "\n"
                + "sleep(2.)" + "\n"
                "movel(p[0.339, -0.250, 0.072, 1.211, -1.257, 1.196], a=1, v=0.2)" + "\n"
                + "sleep(1.)" + "\n"
                "movel(p[0.339, -0.250, 0.072, 2.182, -2.228, -0.000], a=1, v=0.2)" + "\n"
                
            )

        ur_script += (
            "set_tcp(p[0,0,0,0,0,0])" + "\n"
            "movej(p[-0.025, 0.299, 0.457, 3.125, 0.024, 0.026], a=3, v=1.5)" + "\n"
            "movej(p[-0.326, 0.084, 0.458, 2.867, 1.264, 0.034], a=3, v=1.5)" + "\n"
            "movel(p[-0.476, -0.162, 0.072, 2.244, 2.197, 0.036], a=3, v=1.5)" + "\n"
            "movel(p[-0.472, -0.276, 0.072, 2.244, 2.197, -0.000], a=3, v=1)" + "\n"
            "movel(p[-0.341, -0.276, 0.072, 2.244, 2.197, -0.000], a=1, v=0.3)" + "\n"
            "movel(p[-0.181, -0.276, 0.072, 2.214, -2.197, -0.000], a=3, v=1.5)" + "\n"
            "end" + "\n"
        )

        s.send(self.to_bytes(ur_script))
       
        listener = UrListener(s)
        self.wait_till_stop(listener)
                
        time.sleep(3)
        data = s.recv(1024)
        s.close()
        print("Received", repr(data))
        print("Program finish")

    def send_signal(self):
        self.publisher_done.publish(String(data='ur3_done'))
        self.get_logger().info('AGV CommanderにUR3 done信号を送信しました。')

def main(args=None):
    rclpy.init(args=args)
    node = UR3SoupNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

