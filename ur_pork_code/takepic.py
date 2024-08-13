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
cv2.imwrite("/home/saba/workspaces/ramen_robot_ws/ur_pork_code/background.jpg", frame)
    
cap.release()
cv2.destroyAllWindows()
