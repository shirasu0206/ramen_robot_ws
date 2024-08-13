import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/saba/workspaces/ramen_robot_ws/install/dinov2'
