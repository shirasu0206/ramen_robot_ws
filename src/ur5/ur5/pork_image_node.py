import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import cv2
import json

class PorkCameraNode(Node):
    def __init__(self):
        super().__init__('pork_image_node')
        self.subscription = self.create_subscription(Bool, 'pork_detection_request', self.detection_request_callback, 10)
        self.publisher = self.create_publisher(String, 'pork_detection_result', 10)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error('Camera cannot be opened')
        else:
            self.get_logger().info('Pork image node has been started.')

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
        for _ in range(20):
            _, _ = self.cap.read()
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error('Cannot get frame')
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
        if len(area_center_end) == 0: 
            cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg", frame_gray)
        return area_center_end

    def detection_request_callback(self, msg):
        if msg.data:  
            self.get_logger().info('Pork detection requested')
            area_center_end = self.detect()
            self.get_logger().info(f'Detection result: {area_center_end}')
            result_msg = String()
            result_msg.data = json.dumps(area_center_end)
            self.publisher.publish(result_msg)
            self.get_logger().info('Detection result published')

def main(args=None):
    rclpy.init(args=args)
    node = PorkCameraNode()
    rclpy.spin(node)
    node.cap.release()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

