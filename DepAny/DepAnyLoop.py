import os
import cv2  
import numpy as np 
import torch  
import torch.nn.functional as F  
from torchvision.transforms import Compose  
from tqdm import tqdm  
import matplotlib.pyplot as plt  
from datetime import datetime
from depth_anything.dpt import DepthAnything
from depth_anything.util.transform import Resize, NormalizeImage, PrepareForNet
import argparse
import sys, io

class Negi():
    
    def main(self):
        self.Capture(2)
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        try:
            self.DepAny(self.indir)
        finally:
            sys.stdout = sys.__stdout__
        file = os.path.join(self.outdir, "Log.txt")
        with open(file, 'w', encoding='utf-8') as file:
            file.write(output_buffer.getvalue())
 
    def __init__(self):
        self.filenames = None
        self.time = None 
        self.frame = self.cropped_frame = None # raw image & cropped image
        # pixel
        self.y_min , self.y_max = 100 , 280
        self.x_min , self.x_max = 150 , 350
        self.yc_min = self.yc_max = self.xc_min = self.xc_max = None
        self.Cam_to_Plate , self.Top_to_Plate= 0.595 , 0.120
        self.indir = self.outdir = None # raw image & output image
        self.depth = self.depth_abs = self.depth_calc = None # depth tensor
        self.DEPTH = None 
        self.max_Pos = self.min_Pos = None # xy position

    def Loading(self,dir):
        if os.path.isfile(dir):
            self.filenames = open(dir).read().splitlines() if dir.endswith('txt') else [dir]
        else:
            self.filenames = sorted([os.path.join(dir, f) for f in os.listdir(dir) if not f.startswith('.')])

    def Trimming(self,y1,y2,x1,x2,subject):
        return subject[y1:y2, x1:x2]

    def TimeDir(self,subject):
        ext, date = ".jpg", self.time.strftime("%Y\\%m\\%m%d\\%H%M%S")
        self.indir, self.outdir = [os.path.join(os.getcwd(), d, date) for d in ("Test", "Tested")]
        os.makedirs(self.indir, exist_ok=True)
        os.makedirs(self.outdir, exist_ok=True)
        cv2.imwrite(os.path.join(self.indir, self.time.strftime("%H%M%S") + ext), subject)
        print("Image captured and saved successfully at:", self.indir)
    
    def Capture(self,Cam_number):
        cap = cv2.VideoCapture(Cam_number)
        self.time = datetime.now()
        if not cap.isOpened():
            print("Camera not found")
            exit()
        ret, self.frame = cap.read()
        if ret:
            self.cropped_frame = self.Trimming(self.y_min, self.y_max, self.x_min, self.x_max, self.frame)
            self.TimeDir(self.cropped_frame)
            print("success")
        else:
            print("Failed to capture image.")
        cap.release()

    def DepAny(self,subject):
        print(self.time)
        self.Loading(subject)
        parser = argparse.ArgumentParser()
        parser.add_argument('--encoder', type=str, default='vitl', choices=['vits', 'vitb', 'vitl'])
        args = parser.parse_args(['--encoder', 'vitl'])
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(DEVICE)
        depth_anything = DepthAnything.from_pretrained('LiheYoung/depth_anything_{}14'.format(args.encoder)).to(DEVICE).eval()
        transform = Compose([Resize(518, 518, False, True, 14, 'lower_bound', cv2.INTER_CUBIC),
                        NormalizeImage([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]), PrepareForNet()])
        # width,hight,resize_target,keep_aspect_ratio,ensure_multiple_of,resize_mathod,image_interpolation_mathod
        # mean & std

        for filename in tqdm(self.filenames,disable = True):
            raw_image = cv2.imread(filename)
            image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB) / 255.0
            h, w = image.shape[:2]
            image = transform({'image': image})['image']
            image = torch.from_numpy(image).unsqueeze(0).to(DEVICE)

            with torch.no_grad():
                depth = depth_anything(image)
                depth = F.interpolate(depth[None], (h, w), mode='bilinear', align_corners=False)[0, 0]
                self.depth = depth
            self.Analyse_Tensor(self.depth)
            depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
            depth = depth.cpu().numpy().astype(np.uint8)
            depth = cv2.applyColorMap(depth, cv2.COLORMAP_INFERNO)
            filename = os.path.basename(filename)
            cv2.imwrite(os.path.join(self.outdir, filename[:filename.rfind('.')] + '_depth.png'), depth)

            self.depth_abs = torch.full(self.depth.size(), self.Cam_to_Plate , device = DEVICE) - \
                (self.depth - self.depth.min()) / (self.depth.max() - self.depth.min()) *self.Top_to_Plate
            self.Analyse_Tensor(self.depth_abs)

            self.Edge(self.outdir)
            self.depth_calc = self.Trimming(self.yc_min,self.yc_max,self.xc_min,self.xc_max,self.depth_abs)
            self.Analyse_Tensor(self.depth_calc)
            self.DEPTH = self.depth_calc.mean().item()

            max_index = self.depth_calc.argmax() 
            self.max_position = np.unravel_index(max_index.cpu().numpy(), self.depth_calc.shape)
            min_index = self.depth_calc.argmin() 
            self.min_position = np.unravel_index(min_index.cpu().numpy(), self.depth_calc.shape)

            print("\nmin_calc_pos =",self.min_position,"\nmax_calc_pos =", self.max_position)
            print("\n",self.DEPTH)
            print(datetime.now())
    
    def Edge(self,subject):
        self.Loading(subject)
        for filename in tqdm(self.filenames,disable = True):
            frame = cv2.imread(filename)
            target_size = (frame.shape[1], frame.shape[0])
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 200)
            edges = cv2.resize(edges, target_size)             
            coords = np.column_stack(np.where(edges > 0))
            if coords.size > 0:
                self.yc_min, self.xc_min = coords.min(axis=0) + (10, 10)
                self.yc_max, self.xc_max = coords.max(axis=0) - (10, 10)
                print(f"\nyrange = {self.yc_min} to {self.yc_max}\nxrange = {self.xc_min} to {self.xc_max}")
            else:
                self.yc_min, self.xc_min = 30 , 130
                self.yc_max, self.xc_max = 50 , 140
                print("No edges found in the image.")
                continue  
            plt.plot(figsize=(edges.shape[1] / 100, edges.shape[0] / 100), dpi=100)
            plt.imshow(edges, cmap='gray')
            plt.axis('off')  
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            path = os.path.join(subject,"edge.png")
            plt.savefig(path)
            print("\nedge success")

    def Analyse_Tensor(self,subject):
        print(f"\nmax = {subject.max().item()}\nmin = {subject.min().item()}\nmean = {subject.mean().item()}")

run = Negi()

# ここでループを追加して、指定回数実行
num_iterations = 50  # 繰り返し回数を指定
for i in range(num_iterations):
    run.main()