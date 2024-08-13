import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
import cv2
import itertools
import socket
import time
import math
import os
sys.path.append(os.path.expanduser('~/workspaces/ramen_robot_ws/ur_control'))
from ur_listener import UrListener

class UR5PorkNode(Node):
    def __init__(self):
        super().__init__('ur5_pork_node')
        self.subscription_noodle_done = self.create_subscription(String, 'ur5_pork_signal', self.noodle_done_callback, 10)
        self.publisher_done = self.create_publisher(String, 'ur5_done', 10)
        self.publisher_ur3 = self.create_publisher(Int32, 'ur3_order_count', 10)
        self.get_logger().info('UR5 Pork Nodeが起動しました。')
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

    def noodle_done_callback(self, msg):
        try:
            parts = msg.data.split()
            if len(parts) == 2 and parts[0] == "noodle_done":
                self.current_order = int(parts[1])
                self.get_logger().info(f'ur5_noodle_nodeから{self.current_order}杯の注文を受信しました')
                self.execute_pork_task()
            else:
                raise ValueError(f"Unexpected message format: {msg.data}")
        except ValueError as e:
            self.get_logger().error(f"Received an invalid message: {msg.data}, Error: {e}")

    def get_background(self):
        cap = cv2.VideoCapture(2)
        if not cap.isOpened():
            self.get_logger().error('カメラが開きませんでした')
            return None
        for _ in range(20):
            _, _ = cap.read()
        ret, frame = cap.read()
        if not ret:
            self.get_logger().error('画像を読み込めませんでした')
            return None 
        cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg", frame)
        cap.release()

    def image_processing(self, frame):
        height, width = frame.shape[:2]
        x_start = 300
        y_start = 320
        x_end = 1600
        y_end = 760
        cropped_frame = frame[height*y_start//1080 : height*y_end//1080, width*x_start//1920 : width*x_end//1920]
        frame_gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (11, 11), 0)
        return cropped_frame, frame_gray

    def detect(self):
        cap = cv2.VideoCapture(2)
        if not cap.isOpened():
            self.get_logger().error('カメラが開きませんでした')
            return None
        for _ in range(20):
            _, _ = cap.read()
        ret, frame = cap.read()
        if not ret:
            self.get_logger().error('画像を読み込めませんでした')
            return None
        background = cv2.imread('/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg')
        cropped_frame, frame_gray = self.image_processing(frame)
        _, background_gray = self.image_processing(background)
        diff = cv2.absdiff(frame_gray, background_gray)

        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        area_center_end = {}
        if contours == ((), None):
            pass
        else:
            for contour in contours[0]:
                p_area = cv2.contourArea(contour)
                if p_area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(cropped_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    x1 = (x - 200)*(774**2 + (x - 200)**2)**0.5/774
                    y1 = (y - 97)*(774**2 + (y - 97)**2)**0.5/774
                    x2 = (x + w - 200)*(774**2 + (x + w - 200)**2)**0.5/774
                    y2 = (y + h - 97)*(774**2 + (y + h - 97)**2)**0.5/774
                    area_center_end[p_area] = [(x1+x2)/2, (y1+y2)/2, x1, y1, x2, y2]
        cv2.imshow('Frame', cropped_frame)
        cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/frame.jpg", cropped_frame)
        cv2.imshow('Difference', thresh)
        cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/thresh.jpg", thresh)
        cap.release()
        return area_center_end, frame

    def execute_pork_task(self):
        self.get_logger().info(f'チャーシュの調理開始、調理数：{self.current_order}杯')
        try:
            nr = 0
            miss_counter = 0
            area_center_end, _ = self.detect()
            last_pose = "P"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST, self.PORT))
            s.send(self.to_bytes(
            "def myProg():" + "\n"
            "set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
            "movej([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
            "end" + "\n"))
            time.sleep(4) 
            while nr < self.current_order:
                area_threshold = 1500
                
                if len(area_center_end) == 0:
                    break
                len_fork = 120*450/620
                interfere = 35*450/620
                p_NGareas = []
                n_NGareas = []
                p_near = {}
                p_near_n = {}
                n_near = {}
                n_near_p = {}
                all_areas = list(area_center_end.keys())
                allpair_areas = list(itertools.permutations(all_areas,2))
                for pair_areas in allpair_areas:
                    qA = pair_areas[0]
                    wA = pair_areas[1]
                    qcx, qcy, qx, _, qX, _ = area_center_end[qA]
                    wcx, wcy, wx, wy, wX, wY = area_center_end[wA]
                    if qcy - interfere < wy < qcy + interfere or qcy - interfere < wY < qcy + interfere or wy < qcy - interfere < qcy + interfere < wY:
                        if wx < qX + 5 < wX and qA not in p_NGareas:
                            p_NGareas.append(qA)
                        if wx < qx - 5 < wX  and qA not in n_NGareas:
                            n_NGareas.append(qA)
                    if qcy - interfere < wy < qcy + interfere or qcy - interfere < wY < qcy + interfere or wy < qcy - interfere < qcy + interfere < wY:
                        if qX < wx and (p_near.get(qA) is None or p_near.get(qA) > wx - qX):
                            p_near[qA] = wx - qX
                        elif  qx > wX and (n_near.get(qA) is None or n_near.get(qA) > qx - wX):
                            n_near[qA] = qx - wX
                    if qcy - interfere < wcy < qcy + interfere:
                        if qX > wcx and (p_near_n.get(qA) is None or p_near_n.get(qA) > qX - wcx):
                            p_near_n[qA] = qX - wcx
                        elif qx < wcx and (n_near_p.get(qA) is None or n_near_p.get(qA) > wx - qcx):
                            n_near_p[qA] = wcx - qx
                    if qA not in p_near or qA not in p_near_n:
                        pass
                    elif p_near[qA] + p_near_n[qA] < len_fork and qA not in p_NGareas:
                        p_NGareas.append(qA)
                    if qA not in n_near or qA not in n_near_p:
                        pass
                    elif n_near[qA] + n_near_p[qA] < len_fork and qA not in n_NGareas:
                        n_NGareas.append(qA)
                for qA in all_areas:
                    qcx, qcy, qx, _, qX, _ = area_center_end[qA]
                    if qA not in n_NGareas and qx < 15:
                        n_NGareas.append(qA)
                
                sort_area = sorted(all_areas)
                for i in p_NGareas:
                    for j in n_NGareas:
                        if i == j:
                            sort_area.remove(i)

                area_largest = sort_area[-1]
                self.get_logger().info(f"largest : {area_largest}")
                if area_largest > area_threshold*3:
                    self.get_logger().info('possible missidentify')
                center_ends = []
                areas = []
                i = -1
                while area_largest > area_threshold*5 and i > 1-len(sort_area):
                    i -= 1
                    area_largest = sort_area[i]
                last_sum = 0
                if area_largest < area_threshold:
                    allpair_area = list(itertools.permutations(sort_area,2))
                    for area1, area2 in allpair_area:
                        area_sum = area1 + area2
                        if area_sum > area_threshold and area_sum < area_threshold*5 and area_sum > last_sum:
                            last_sum = area_sum
                    center_ends.append(area_center_end.get(last_sum[0]))
                    center_ends.append(area_center_end.get(last_sum[1]))
                else:
                    areas = [area_largest]
                    center_ends = [area_center_end.get(area_largest)]
                if len(areas) == 0:
                    self.get_logger().info('all chashu are small, please remove all chashu and take picture')
                    break
                for n in range(len(areas)):
                    if areas[n] not in p_NGareas:
                        if p_near_n.get(areas[n]) is None or p_near_n.get(areas[n]) > len_fork:
                            x_of = (center_ends[n][4] - 220)/450*620/1000
                        else:
                            x_of = (center_ends[n][4] - p_near_n[areas[n]] + len_fork - 223)/450*620/1000
                        if x_of > 0:
                            x_of = 0
                        elif x_of < -0.465:
                            x_of = -0.465
                        y_of = (-round((center_ends[n][1]-62.9)/196.5*270/1000/0.015))*0.015
                        if last_pose == "N":
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"movej([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
                            +"end" + "\n"))
                            time.sleep(4)
                        s.send(self.to_bytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[{x_of}, {y_of}, 0.0, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +"pos_end = pose_add(begin_pos, p[0.0, 0.0, -0.140, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"                        
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +f"pos_end = pose_add(begin_pos, p[0, 0.0, 0, {math.pi/2}, 0, 0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +"pos_end = pose_add(begin_pos, p[0.0, 0.0, 0.140, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.75)" + "\n"
                        +"movel([-0.8738863564735608, -1.5159929882822747, -2.284112392084979, -2.484476190213928, 0.7115707360380882, 3.11488911603428], a=0.26, v=0.26)" + "\n"
                        +"end" + "\n"))
                        time.sleep(6)
                        data = s.recv(1024)
                        if nr == 0:
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                            +"movej([-2.041337093132568, -1.6865116562021205, -2.1197023765471132, -2.452013066126834, -0.4630358505540957, 3.0927234345339514], a=0.52, v=0.52)" + "\n"
                            +"end" + "\n"))
                            time.sleep(3.75)
                            data = s.recv(1024)
                        else:
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                            +"movej([-2.330189084337629, -1.4390239682693247, -2.3645720706019175, -2.4631831733395972, -0.7515387759087583, 3.1038935417467157], a=0.52, v=0.52)" + "\n"
                            +"end" + "\n"))
                            time.sleep(4.25)
                            data = s.recv(1024)
                        s.send(self.to_bytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[0.0, 0.0, -0.04, 0, 0, 0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[0.06, 0.0, 0, -{math.pi/3}, 0, 0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                        +"end" + "\n"))
                        time.sleep(0.75)
                        area_center_end_feedback, gray_background = self.detect()
                        s.send(self.to_bytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[0.03, 0.0, 0.0, {math.pi/3}, 0, 0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                        +"movej([-0.8738863564735608, -1.5159929882822747, -2.284112392084979, -2.484476190213928, 0.7115707360380882, 3.11488911603428], a=3.00, v=1.50)" + "\n"
                        +"movel([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
                        +"end" +"\n"))
                        time.sleep(4)
                        data = s.recv(1024)
                        if len(area_center_end) == len(area_center_end_feedback):
                            self.get_logger().info("miss picking")
                            miss_counter += 1
                        else:
                            area_center_end = area_center_end_feedback
                            nr += 1
                        last_pose = "P"
                    else:
                        if areas[n] not in n_near_p or n_near_p.get(areas[n]) or n_near_p.get(areas[n]) > len_fork:
                            x_of = (center_ends[n][2] + 187)/450*620/1000
                        else:
                            x_of = (center_ends[n][2] + n_near_p[areas[n]] - len_fork + 187)/450*620/1000
                        if x_of < 0:
                            x_of = 0
                        elif x_of > 0.465:
                            x_of = 0.465
                        y_of = (-round((center_ends[n][1]-62.9)/196.5*270/1000/0.015) + 1)*0.015
                        if last_pose == "P":
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"movej([0.833220184902093, -1.5641640756373183, 1.6943656378360952, -1.68668618912732, -1.5646876744129166, -2.33298161114082], a=3.00, v=1.50)" + "\n"
                            +"end" +"\n"))
                            time.sleep(4)
                        s.send(self.to_bytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[{x_of}, {y_of}, 0.0, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +"pos_end = pose_add(begin_pos, p[0.0, 0.0, -0.325, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +f"pos_end = pose_add(begin_pos, p[0, 0.0, 0, {math.pi/2}, 0, 0])" +"\n"
                        +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +"pos_end = pose_add(begin_pos, p[0.0, 0.0, 0.325, 0.0, 0.0, 0.0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.75)" + "\n"
                        +"end" +"\n"))
                        time.sleep(6)
                        data = s.recv(1024)
                        if nr == 0:
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"movel([0.4031710572, -0.9138543963, 1.2793263417, -0.3906046865, -1.1695451317, -3.1319933427], a=0.35, v=0.26)" + "\n"
                            +"movej([-0.2827433388, -0.9962339370, 1.525068700, -0.6106907052, -0.2827433388, -3.0951668954], a=0.35, v=0.26)" + "\n"
                            +"end" +"\n"))
                            time.sleep(6)
                            data = s.recv(1024)
                        else:
                            s.send(self.to_bytes(
                            "def myProg():"+"\n"
                            +"movel([0.4031710572106902, -0.9138543963442308, 1.2793263417118435, -0.3906046865963309, -1.1695451317614003, -3.131993342703824], a=0.35, v=0.26)" + "\n"
                            +"movej([-0.5328490206338689, -0.9253735694073936, 1.4032447186034411, -0.5239478414486977, -0.5328490206338689, -3.135134935357414], a=0.35, v=0.26)" + "\n"
                            +"end" +"\n"))
                            time.sleep(5.75)
                            data = s.recv(1024)
                        area_center_end_feedback, gray_background = self.detect()
                        s.send(self.to_bytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[0, 0.06, 0, -{math.pi/3}, 0, 0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                        "set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                        +"begin_pos = get_actual_tcp_pose()" +"\n"
                        +f"pos_end = pose_add(begin_pos, p[0, 0.03, 0.05, {math.pi/3}, 0, 0])" +"\n"
                        +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                        +"movej([0.833220184902093, -1.5641640756373183, 1.6943656378360952, -1.68668618912732, -1.5646876744129166, -2.33298161114082], a=3.00, v=1.50)" + "\n"
                        +"end" +"\n"))
                        time.sleep(5)
                        data = s.recv(1024)
                        if len(area_center_end) == len(area_center_end_feedback):
                            self.get_logger().info("miss picking")
                            miss_counter += 1
                        else:
                            area_center_end = area_center_end_feedback
                            nr += 1
                        last_pose = "N"
                if miss_counter > 1:
                    self.get_logger().info("Sorry, I couldn't pick chashu.")
                    break
                
            if len(area_center_end) == 1:
                self.get_logger().error('Prease put more chashu')
            if len(area_center_end) == 0:
                self.get_logger().error('Prease put more chashu')
                cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg", gray_background)

            s.send(self.to_bytes(
            "def myProg():" + "\n"
            "movej([0, -1.5707963, 0, -1.5707963, 0, 0], a=3.00, v=1.50)" + "\n"
            "end" + "\n"))
            data = s.recv(1024)
            s.close()
            cv2.destroyAllWindows()

            self.forward_to_ur3()  # Add this line to call forward_to_ur3
            self.reset_state()  # Add this line to call reset_state

        except Exception as e:
            self.get_logger().error(f"An error occurred: {e}")
            
    def forward_to_ur3(self):
        order_msg = Int32()
        order_msg.data = self.current_order
        self.publisher_ur3.publish(order_msg)
        self.get_logger().info(f'UR3に{order_msg.data}をpublsihしました')
        done_msg = String()
        done_msg.data = 'UR5 task completed'
        self.publisher_done.publish(done_msg)

    def reset_state(self):
        self.current_order = None

def main(args=None):
    rclpy.init(args=args)
    node = UR5PorkNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
