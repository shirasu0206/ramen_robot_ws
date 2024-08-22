import cv2

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
frame_gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
frame_gray = cv2.GaussianBlur(frame_gray, (11, 11), 0)
cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg", frame_gray)

cap.release()
cv2.destroyAllWindows()
