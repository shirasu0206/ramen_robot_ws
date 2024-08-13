import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        
        Node(
            package='agv',
            executable='agv_commander_node',
            name='agv_commander_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur5',
            executable='ur5_noodle_node',
            name='ur5_noodle_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur5',
            executable='ur5_pork_node',
            name='ur5_pork_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur5',
            executable='pork_image_node',
            name='dpork_image_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur3',
            executable='ur3_negi_node',
            name='ur3_negi_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur3',
            executable='ur3_soup_node',
            name='ur3_soup_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),
        Node(
            package='ur3',
            executable='depth_anything_node',
            name='depth_anything_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
        ),

    ])

