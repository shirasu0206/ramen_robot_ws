import sys
import cv2
from ultralytics import YOLO
import itertools
import socket
import time
import math

def toBytes(string):
    return bytes(string.encode())

def detect():
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print('camera can not be open')
        exit()
    for _ in range(20):
        _, _ = cap.read()
    ret, frame = cap.read()
    if not ret:
        print('can not get frame')
        exit()
    height, width = frame.shape[:2]
    x_start = 300
    y_start = 320
    x_end = 1600
    y_end = 760
    cropped_frame = frame[height*y_start//1080 : height*y_end//1080, width*x_start//1920 : width*x_end//1920]
    results = model(cropped_frame, conf=0.7)
    img_annotated = results[0].plot()
    cv2.imwrite('pic.jpg', img_annotated)
    cap.release()
    return results

def results_input(results):
    boxes = results[0].boxes
    classes = results[0].boxes.cls

    area_center_end = {}
    for box, _ in zip(boxes, classes):
        x1p, y1p, x2p, y2p = [int(i) for i in box.xyxy[0]]
        x1 = (x1p - 200)*(774**2 + (x1p - 200)**2)**0.5/774
        y1 = (y1p - 97)*(774**2 + (y1p - 97)**2)**0.5/774
        x2 = (x2p - 200)*(774**2 + (x2p - 200)**2)**0.5/774
        y2 = (y2p - 97)*(774**2 + (y2p - 97)**2)**0.5/774
        area_center_end[(x1-x2)*(y1-y2)] = [(x1+x2)/2, (y1+y2)/2, x1, y1, x2, y2]
    
    return area_center_end

if __name__ == "__main__":
    try:
        model = YOLO('best.pt')

        if len(sys.argv) != 2:
            print("Usage: python3 chashu.py <n_ramen>")
            sys.exit(1)
        
        n_ramen = int(sys.argv[1])
        results = detect()
        nr = 0
        miss_counter = 0
        last_pose = "P"

        HOST = "192.168.56.101"
        PORT = 30002
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(toBytes(
        "def myProg():" + "\n"
        "set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
        "movej([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
        "end" + "\n"))
        time.sleep(4)
        data = s.recv(1024)
        print("Received")

        while nr < n_ramen:
            area_center_end = results_input(results)

            area_threshold = 6000
            
            if len(area_center_end) == 0:
                print('put more chashu')
                break
            len_fork = 120*450/620
            interfere = 35*450/620
            p_NGareas = []
            n_NGareas = []
            p_near = {}
            p_near_n = {}
            n_near = {}
            n_near_p = {}
            p_area_largest = 0
            n_area_largest = 0
            all_areas = list(area_center_end.keys())
            allpair_areas = list(itertools.permutations(all_areas,2))
            for pair_areas in allpair_areas:
                qA = pair_areas[0]
                wA = pair_areas[1]
                qcx, qcy, qx, qy, qX, qY = area_center_end[qA]
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
                qcx, qcy, qx, qy, qX, qY = area_center_end[qA]
                if qA not in n_NGareas and qx < 15:
                    n_NGareas.append(qA)
            
            sort_area = sorted(all_areas)
            for i in p_NGareas:
                for j in n_NGareas:
                    if i == j:
                        sort_area.remove(i)

            print("sort_areas", sort_area)
            area_largest = sort_area[-1]
            center_ends = []
            areas = []
            i = -1
            while area_largest > area_threshold*2 and i > 1-len(sort_area):
                i -= 1
                area_largest = sort_area[i]
            
            last_sum = 0

            if area_largest > area_threshold*2:
                print("possible misidentify")
                break
            if area_largest < area_threshold:
                allpair_area = list(itertools.permutations(sort_area,2))
                for area1, area2 in allpair_area:
                    area_sum = area1 + area2
                    if area_sum > area_threshold and area_sum < area_threshold*2 and area_sum > last_sum:
                        last_sum = area_sum
                center_ends.append(area_center_end.get(last_sum[0]))
                center_ends.append(area_center_end.get(last_sum[1]))
            else:
                areas = [area_largest]
                center_ends = [area_center_end.get(area_largest)]
            if len(areas) == 0:
                print('all chashu are small')
                break
            print("~~~",len(areas),'chashu will be picked',areas,"~~~")
            for n in range(len(areas)):
                if areas[n] not in p_NGareas:
                    print("positive", areas[n])
                    if p_near_n.get(areas[n]) is None or p_near_n.get(areas[n]) > len_fork:
                        x_of = (center_ends[n][4] - 220)/450*620/1000
                    else:
                        x_of = (center_ends[n][4] - p_near_n[areas[n]] + len_fork - 223)/450*620/1000
                    if x_of > 0:
                        x_of = 0
                    elif x_of < -0.465:
                        x_of = -0.465
                    y_of = (-round((center_ends[n][1]-62.9)/196.5*270/1000/0.015) + 1)*0.015
                    if last_pose == "N":
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"movej([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
                        +"end" + "\n"))
                        time.sleep(4)
                    s.send(toBytes(
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
                    print("Received")
                    if nr == 0:
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +"movej([-2.0313887163962003, -1.7770942443806264, -2.152340033559407, -2.3266984258336407, -0.4532620067429274, 3.090454506506359], a=0.52, v=0.52)" + "\n"
                        +"end" + "\n"))
                        time.sleep(3.75)
                        data = s.recv(1024)
                        print("Received")
                    else:
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                        +"movej([-2.3588124840703366, -1.5610224829837283, -2.4015730507441972, -2.3036600797073157, -0.7799876427162659, 3.103020877120718], a=0.52, v=0.52)" + "\n"
                        +"end" + "\n"))
                        time.sleep(4.25)
                        data = s.recv(1024)
                        print("Received")
                    s.send(toBytes(
                    "def myProg():"+"\n"
                    +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +f"pos_end = pose_add(begin_pos, p[0.06, 0.0, 0, -{math.pi/3}, 0, 0])" +"\n"
                    +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                    +"end" + "\n"))
                    time.sleep(0.75)
                    results = detect()
                    area_center_end_feedback = results_input(results)
                    s.send(toBytes(
                    "def myProg():"+"\n"
                    +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +f"pos_end = pose_add(begin_pos, p[0.03, 0.0, 0.0, {math.pi/3}, 0, 0])" +"\n"
                    +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                    +"movej([-0.8738863564735608, -1.5159929882822747, -2.284112392084979, -2.484476190213928, 0.7115707360380882, 3.11488911603428], a=3.00, v=1.50)" + "\n"
                    +"movel([-0.8463101542920504, -1.7421876593407395, -2.0601866490541068, -0.8862781941627205, 1.6123351629923617, 2.27451308119901], a=3.00, v=1.50)" + "\n"
                    +"end" + "\n"))
                    time.sleep(4)
                    data = s.recv(1024)
                    if len(area_center_end) == len(area_center_end_feedback):
                        print("miss picking")
                        miss_counter += 1
                    else:
                        print("~~~finish~~~")
                        nr += 1
                    last_pose = "P"
                else:
                    print("negative", areas[n])
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
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"movej([0.8330456519768935, -1.5009831567151235, 1.894380370114645, -1.9497073074028655, -1.5643386085625175, -2.3317598806644244], a=3.00, v=1.50)" + "\n"
                        +"end" +"\n"))
                        time.sleep(4)
                    s.send(toBytes(
                    "def myProg():"+"\n"
                    +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +f"pos_end = pose_add(begin_pos, p[{x_of}, {y_of}, 0.0, 0.0, 0.0, 0.0])" +"\n"
                    +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +"pos_end = pose_add(begin_pos, p[0.0, 0.0, -0.225, 0.0, 0.0, 0.0])" +"\n"
                    +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +"set_tcp(p[0, 0.050, 0.132, 0, 0, 0])" + "\n"
                    +f"pos_end = pose_add(begin_pos, p[0, 0.0, 0, {math.pi/2}, 0, 0])" +"\n"
                    +"movel(pos_end , a=1.40, v=1.04)" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +"pos_end = pose_add(begin_pos, p[0.0, 0.0, 0.225, 0.0, 0.0, 0.0])" +"\n"
                    +"movel(pos_end , a=0.5, v=0.75)" + "\n"
                    +"end" +"\n"))
                    time.sleep(6)
                    data = s.recv(1024)
                    if nr == 0:
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"movel([0.11222467090323537, -1.0979866324296326, 1.5803956376808654, -0.5066690818539539, -1.4067353771074294, -3.138625593861403], a=0.35, v=0.26)" + "\n"
                        +"movej([-0.2827433388230814, -0.9962339370383633, 1.525068700392645, -0.6106907052728159, -0.2827433388230814, -3.0951668954867437], a=0.35, v=0.26)" + "\n"
                        +"end" +"\n"))
                        time.sleep(6)
                        data = s.recv(1024)
                        print("Received")
                    else:
                        s.send(toBytes(
                        "def myProg():"+"\n"
                        +"movel([0.11222467090323537, -1.0979866324296326, 1.5803956376808654, -0.5066690818539539, -1.4067353771074294, -3.138625593861403], a=0.35, v=0.26)" + "\n"
                        +"movej([-0.5328490206338689, -0.9253735694073936, 1.4032447186034411, -0.5239478414486977, -0.5328490206338689, -3.135134935357414], a=0.35, v=0.26)" + "\n"
                        +"end" +"\n"))
                        time.sleep(5.75)
                        data = s.recv(1024)
                        print("Received")
                    results = detect()
                    area_center_end_feedback = results_input(results)
                    s.send(toBytes(
                    "def myProg():"+"\n"
                    +"set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +f"pos_end = pose_add(begin_pos, p[0, 0.06, 0, -{math.pi/3}, 0, 0])" +"\n"
                    +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                    "set_tcp(p[0, 0.050, 0.215, 0, 0, 0])" + "\n"
                    +"begin_pos = get_actual_tcp_pose()" +"\n"
                    +f"pos_end = pose_add(begin_pos, p[0, 0.03, 0.05, {math.pi/3}, 0, 0])" +"\n"
                    +"movel(pos_end , a=0.5, v=0.26)" + "\n"
                    +"movej([0.8330456519768935, -1.5009831567151235, 1.894380370114645, -1.9497073074028655, -1.5643386085625175, -2.3317598806644244], a=3.00, v=1.50)" + "\n"
                    +"end" +"\n"))
                    time.sleep(5)
                    data = s.recv(1024)
                    if len(area_center_end) == len(area_center_end_feedback):
                        print("miss picking")
                        miss_counter += 1
                    else:
                        print("~~~finish~~~")
                        nr += 1
                    last_pose = "N"
            if miss_counter > 1:
                print("Humans pick")
                break

        s.send(toBytes(
        "def myProg():" + "\n"
        "movej([0, -1.5707963, 0, -1.5707963, 0, 0], a=3.00, v=1.50)" + "\n"
        "end" + "\n"))
        data = s.recv(1024)
        s.close()
        print("Received", repr(data))
        print("Program finish")
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

