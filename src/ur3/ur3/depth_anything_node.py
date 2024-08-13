import os
import cv2  
import numpy as np 
import torch  
import torch.nn.functional as F  
from torchvision.transforms import Compose  
from tqdm import tqdm  
import matplotlib.pyplot as plt
import sys, io
import argparse  
from datetime import datetime
from depth_anything.dpt import DepthAnything
from depth_anything.transform import Resize, NormalizeImage, PrepareForNet
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Negi(Node):
    
    def __init__(self):
        super().__init__('depth_anything_node')
        self.publisher_depth = self.create_publisher(Float32, 'negi_depth', 10)
        self.timer = self.create_timer(5.0, self.timer_callback)
        self.time = None 
        self.frame = self.cropped_frame = None
        self.y_min , self.y_max = 130 , 310
        self.x_min , self.x_max = 220 , 320
        self.yc_min = self.yc_max = self.xc_min = self.xc_max = None
        self.Cam_to_Plate , self.Top_to_Plate= 0.556 , 0.105
        self.indir = self.outdir = None
        self.depth = self.depth_abs = self.depth_calc = None
        self.DEPTH = None 
        self.max_Pos = self.min_Pos = None
        
    def timer_callback(self):
        self.capture(0)
        with io.StringIO() as output_buffer:
            sys.stdout = output_buffer
            self.dep_any(self.indir)
            file = os.path.join(self.outdir,"Log.txt")
            with open(file, 'w', encoding='utf-8') as file:
                file.write(output_buffer.getvalue())
        
        depth_msg = Float32()
        depth_msg.data = self.DEPTH
        self.publisher_depth.publish(depth_msg)
        self.get_logger().info(f'ネギの平均深さ：{self.DEPTH}')
    
    def loading(self, dir):
        if os.path.isfile(dir):
            self.filenames = open(dir).read().splitlines() if dir.endswith('txt') else [dir]
        else:
            self.filenames = sorted([os.path.join(dir, f) for f in os.listdir(dir) if not f.startswith('.')])

    def trimming(self, y1, y2, x1, x2, subject):
        return subject[y1:y2, x1:x2]

    def time_dir(self, subject):
        ext, date = ".jpg", self.time.strftime("%Y/%m/%m%d/%H%M%S")
        self.indir, self.outdir = [os.path.join(os.getcwd(), d, date) for d in ("DepAny/Test", "DepAny/Tested")]
        os.makedirs(self.indir, exist_ok=True)
        os.makedirs(self.outdir, exist_ok=True)
        cv2.imwrite(os.path.join(self.indir, self.time.strftime("%H%M%S") + ext), subject)
        #self.get_logger().info(f"Image captured and saved successfully at: {self.indir}")
    
    def capture(self, cam_number):
        cap = cv2.VideoCapture(cam_number)
        self.time = datetime.now()
        if not cap.isOpened():
            self.get_logger().error("カメラが見つかりません")
            exit()
        ret, self.frame = cap.read()
        if ret:
            self.cropped_frame = self.trimming(self.y_min, self.y_max, self.x_min, self.x_max, self.frame)
            self.time_dir(self.cropped_frame)
        else:
            self.get_logger().error("画像の撮影に失敗しました")
        cap.release()

    def dep_any(self, subject):
        #self.get_logger().info(f"Processing image at {self.time}")
        self.loading(subject)
        parser = argparse.ArgumentParser()
        parser.add_argument('--encoder', type=str, default='vitl', choices=['vits', 'vitb', 'vitl'])
        args = parser.parse_args(['--encoder', 'vitl'])
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        #self.get_logger().info(f"Using device: {DEVICE}")
        depth_anything = DepthAnything.from_pretrained('LiheYoung/depth_anything_{}14'.format(args.encoder)).to(DEVICE).eval()
        transform = Compose([Resize(518, 518, False, True, 14, 'lower_bound', cv2.INTER_CUBIC),
                        NormalizeImage([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), PrepareForNet()])

        for filename in tqdm(self.filenames, disable=True):
            raw_image = cv2.imread(filename)
            image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB) / 255.0
            h, w = image.shape[:2]
            image = transform({'image': image})['image']
            image = torch.from_numpy(image).unsqueeze(0).to(DEVICE)

            with torch.no_grad():
                depth = depth_anything(image)
                depth = F.interpolate(depth[None], (h, w), mode='bilinear', align_corners=False)[0, 0]
                self.depth = depth
            self.analyse_tensor(self.depth)
            depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
            depth = depth.cpu().numpy().astype(np.uint8)
            depth = cv2.applyColorMap(depth, cv2.COLORMAP_INFERNO)
            filename = os.path.basename(filename)
            cv2.imwrite(os.path.join(self.outdir, filename[:filename.rfind('.')] + '_depth.png'), depth)

            self.depth_abs = torch.full(self.depth.size(), self.Cam_to_Plate, device=DEVICE) - \
                (self.depth - self.depth.min()) / (self.depth.max() - self.depth.min()) * self.Top_to_Plate
            self.analyse_tensor(self.depth_abs)

            self.edge(self.outdir)
            self.depth_calc = self.trimming(self.yc_min, self.yc_max, self.xc_min, self.xc_max, self.depth_abs)
            self.analyse_tensor(self.depth_calc)
            self.DEPTH = self.depth_calc.mean().item()

            max_index = self.depth_calc.argmax() 
            self.max_position = np.unravel_index(max_index.cpu().numpy(), self.depth_calc.shape)
            min_index = self.depth_calc.argmin() 
            self.min_position = np.unravel_index(min_index.cpu().numpy(), self.depth_calc.shape)

            #self.get_logger().info(f"Min pos: {self.min_position}, Max pos: {self.max_position}")
            #self.get_logger().info(f"Mean depth: {self.DEPTH}")
            #self.get_logger().info(f"Current time: {datetime.now()}")

    def edge(self, subject):
        self.loading(subject)
        for filename in tqdm(self.filenames, disable=True):
            frame = cv2.imread(filename)
            target_size = (frame.shape[1], frame.shape[0])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges = cv2.resize(edges, target_size)
            coords = np.column_stack(np.where(edges > 0))
            if coords.size > 0:
                self.yc_min, self.xc_min = coords.min(axis=0) + (10,10)
                self.yc_max, self.xc_max = coords.max(axis=0) - (10,10)
                if self.yc_min > self.yc_max:
                	a = self.yc_min
                	self.yc_min = self.yc_max
                	self.yc_max = a
                if self.xc_min > self.xc_max:
                	a = self.xc_min
                	self.xc_min = self.xc_max
                	self.xc_max = a      	
                self.get_logger().info(f"Y range: {self.yc_min} to {self.yc_max}, X range: {self.xc_min} to {self.xc_max}")
            else:
                self.yc_min, self.xc_min = 0, 100
                self.yc_max, self.xc_max = 0, 100
                self.get_logger().warning("edgeが見つかりません")
            plt.plot(figsize=(edges.shape[1] / 100, edges.shape[0] / 100), dpi=100)
            plt.imshow(edges, cmap='gray')
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            path = os.path.join(subject, "edge.png")
            plt.savefig(path)
            #self.get_logger().info("Edge detection successful")

    def analyse_tensor(self, subject):
        if subject.size() != 0:
            self.get_logger().info(f"Tensor analysis - 最大: {subject.max().item()}, 最小: {subject.min().item()}, 平均: {subject.mean().item()}")
        else:
            self.get_logger().warning("テンソルが見つかりません")

def main(args=None):
    rclpy.init(args=args)
    negi_node = Negi()
    rclpy.spin(negi_node)
    negi_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

