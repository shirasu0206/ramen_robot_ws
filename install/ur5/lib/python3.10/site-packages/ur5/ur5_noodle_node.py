import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import socket
import time
import sys  
import os
sys.path.append(os.path.expanduser('~/workspaces/ramen_robot_ws/ur_control'))
from ur_listener import UrListener

class UR5NoodleNode(Node):
    def __init__(self):
        super().__init__('ur5_noodle_node')
        self.subscription_order = self.create_subscription(String, 'ur5_order', self.order_callback, 10)
        self.subscription_arrival = self.create_subscription(String, 'ur5_arrival', self.arrival_callback, 10)
        self.publisher_pork = self.create_publisher(String, 'ur5_pork_signal', 10)
        self.current_order_count = None  
        self.agv_at_f = False  # AGVがFにいるかどうかを保持
        self.get_logger().info('UR5 Noodle Nodeが起動しました。')
        self.HOST = "192.168.56.101"
        self.PORT = 30002
        self.current_order = None

    def to_bytes(self, string):
        return bytes(string.encode())
        
    def wait_till_stop(self, listener):
        # ロボットが停止するまでループ
        while not listener.get_robot_state():
            self.get_logger().info('UR5動作中。。。')
            time.sleep(1)
        self.get_logger().info('UR5動作終了')
    
        
    def order_callback(self, msg):
        self.get_logger().info(f'受け取った注文数：{msg.data}')
        try:
            self.current_order_count = int(msg.data.split()[-2])  # 'orders' の前の値を取得
            self.current_order = self.current_order_count  # 現在の注文個数をself.current_orderに設定
        except ValueError as e:
            self.get_logger().error(f'Failed to parse order count: {e}')
            return
        self.check_and_start_cooking()

    def arrival_callback(self, msg):
        self.get_logger().info(f'{msg.data}の信号を受け取りました')
        if "arrived at F" in msg.data:
            self.agv_at_f = True
            self.check_and_start_cooking()
    
    def check_and_start_cooking(self):
        if self.current_order_count is not None and self.agv_at_f:
            self.get_logger().info(f'{self.current_order_count}の麺の調理を開始します')
            self.execute_noodle_task()
            self.reset_state()

    def execute_noodle_task(self):
        self.get_logger().info(f'ネギの調理開始、調理数：{self.current_order}杯')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        listener = UrListener(s)  # UrListenerのインスタンスを作成
        s.send(self.to_bytes(
        "def myProg():"+"\n"
        +"set_tcp(p[0.0,0.05,0.132,0.0,0.0,0.0])" + "\n"
        +"movej([0, -1.571, 0, -1.571, 0, 0], a=1.396, v=1.047)" + "\n" #home position
        +"movej([-3.9188,-0.8065,0.9053,-1.6469,-1.5769,-0.7866], a=1.396, v=1.047)" + "\n"
        +"movel(p[0.598, -0.452, -0.139, 2.229, -2.206, 0], a=1.200, v=0.250)" + "\n"
        +"movel(p[0.377, -0.452, -0.139, 2.229, -2.206, 0], a=1.200, v=0.250)" + "\n"  #return chashu tool
        +"movel(p[0.377, -0.251, -0.139, 2.229, -2.206, 0], a=1.200, v=0.250)" + "\n"
        +"movel(p[0.563, -0.251, -0.139, 2.229, -2.206, 0], a=1.200, v=0.250)" + "\n"  #get noodle tool
        +"movej(p[0.583, -0.095, 0.576, -1.888, 2.392, -0.047], a=1.396, v=1.047)" + "\n"
        +"movej([-2.853089728,-1.687035255,1.23150432,-1.410749634,-1.445656219,-0.153588974], a=3.00, v=1.50)" + "\n"  #move to Soup pot
        +"movej([-2.853089728,-1.16465821,1.468694566,-1.588947751,-1.444958088,-0.152890842], a=3.00, v=1.50)" + "\n"
        +"end" + "\n"))
        self.wait_till_stop(listener)
        
       #scratching
        s.send(self.to_bytes(
            "def myProg():"+"\n"
            +"movej([-2.828306053,-0.868475836,1.000946326,-1.420174412,-1.439198501,-0.129154365], a=6.00, v=3.00)" + "\n"
            +"movej([-2.853089728,-1.16465821,1.468694566,-1.588947751,-1.444958088,-0.152890842], a=6.00, v=3.00)" + "\n"
            +"movej([-2.828306053,-0.868475836,1.000946326,-1.420174412,-1.439198501,-0.129154365], a=6.00, v=3.00)" + "\n"
            +"movej([-2.853089728,-1.16465821,1.468694566,-1.588947751,-1.444958088,-0.152890842], a=6.00, v=3.00)" + "\n"
            +"movej([-2.828306053,-0.868475836,1.000946326,-1.420174412,-1.439198501,-0.129154365], a=6.00, v=3.00)" + "\n"
            +"movej([-2.853089728,-1.16465821,1.468694566,-1.588947751,-1.444958088,-0.152890842], a=6.00, v=3.00)" + "\n"
            +"end" + "\n"))
        self.wait_till_stop(listener)
        time.sleep(5) #boiling
        
        #draining1
        s.send(self.to_bytes(
        "def myProg():"+"\n"
        +"movej([-2.853089728,-1.687035255,1.23150432,-1.410749634,-1.445656219,-0.153588974], a=3.00, v=1.50)" + "\n"
        +"movej([-2.853264261,-1.7816321,1.805543111,-1.890540646,-1.444259956,-0.151494579], a=15.00, v=10.00)" + "\n"
        +"movej([-2.853089728,-1.687035255,1.23150432,-1.410749634,-1.445656219,-0.153588974], a=15.00, v=10.00)" + "\n"
        +"movej([-2.853264261,-1.7816321,1.805543111,-1.890540646,-1.444259956,-0.151494579], a=15.00, v=10.00)" + "\n"
        +"movej([-2.853089728,-1.687035255,1.23150432,-1.410749634,-1.445656219,-0.153588974], a=15.00, v=10.00)" + "\n"
        +"movej([-2.853264261,-1.7816321,1.805543111,-1.890540646,-1.444259956,-0.151494579], a=15.00, v=10.00)" + "\n"
        +"movej([-2.853089728,-1.687035255,1.23150432,-1.410749634,-1.445656219,-0.153588974], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,0.668635636,-1.158025959,-1.446354351,-0.154287106], a=3.00, v=1.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,1.707455607,-0.962898148,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,0.668635636,-1.158025959,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,1.707455607,-0.962898148,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,0.668635636,-1.158025959,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,1.707455607,-0.962898148,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"movej([-1.86453524,-1.864884306,0.668635636,-1.158025959,-1.446354351,-0.154287106], a=15.00, v=10.00)" + "\n"
        +"set_tcp(p[0, -0.165, 0.26, 0, 0, 0])" + "\n"
        +"movej([0.159697627,-1.584584428,1.766273203,-2.746101045,-1.666789436,3.275459407], a=3.00, v=1.50)" + "\n"
        +"movej([0.159697627,-1.531526419,1.917767782,-2.950828166,-1.6676621,3.276157539], a=3.00, v=1.50)" + "\n"
        +"movel([0.111047934,-0.817861287,2.379407369,-5.186769471,-1.671152758,3.115238181], a=1.00, v=0.25)" + "\n"
        +"movel([0.111047934,-0.817861287,2.243271687,-5.196769471,-1.671152758,3.115238181], a=3.00, v=1.50)" + "\n"
        +"movel([0.111047934,-0.817861287,2.379407369,-5.186769471,-1.671152758,3.115238181], a=3.00, v=1.50)" + "\n"
        +"movel([0.111047934,-0.817861287,2.379407369,-5.196769471,-1.671152758,3.115238181], a=3.00, v=1.50)" + "\n"
        +"movej([0.217642558,-1.018225086,2.137679268,-5.11154578,-1.708677338,3.042457952], a=0.500, v=0.5)" + "\n"#麺茹で終わり
        +"movej([-3.743033114,-1.018225086,2.137679268,-5.11154578,-1.708677338,3.042457952], a=3.00, v=1.50)" + "\n"
        +"movej([-3.7430331138270394, -0.6756169534470049, 1.7156586547104258, -2.6288149193538595, -1.5503759745465628, -0.6141813637768044], a=3, v=1.5)" + "\n"
        +"movel([-3.9358919961724124, -0.8187339521105399, 2.1676989309769574, -2.934247538452867, -1.5477579806685715, -0.805818515645782], a=1.200, v=0.250)" + "\n"
        +"movel([-4.168020786687658, -0.7000515629749255, 1.7774433102310254, -2.657438319086566, -1.5439182563141838, -1.0391690366374238], a=1.200, v=0.250)" + "\n"
        +"set_tcp(p[0.0,0.05,0.132,0.0,0.0,0.0])" + "\n"
        +"movel(p[0.598, -0.452, -0.139, 2.229, -2.206, 0], a=1.200, v=0.250)" + "\n"
        +"movel([-3.9188,-0.8065,0.9053,-1.6469,-1.5769,-0.7866], a=1.396, v=1.047)" + "\n"
        +"movej([0, -1.571, 0, -1.571, 0, 0], a=1.396, v=1.047)" + "\n"
        +"end" + "\n"))
        time.sleep(31)
        data = s.recv(1024)
        s.close()
        
    
        #self.get_logger().info(f"Received: {repr(data)}")
        self.get_logger().info("調理を終了しました")
        self.send_signal()

    def send_signal(self):
        if self.current_order is not None:
            msg = String()
            msg.data = f"noodle_done {self.current_order}"
            self.publisher_pork.publish(msg)
            self.get_logger().info('ur5_pork_nodeに信号を送りました')
        else:
            self.get_logger().error('Current order is None, cannot send signal.')

    def reset_state(self):
        self.current_order_count = None
        self.agv_at_f = False

def main(args=None):
    rclpy.init(args=args)
    node = UR5NoodleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
