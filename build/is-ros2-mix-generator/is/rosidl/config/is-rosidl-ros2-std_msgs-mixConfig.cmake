# - Config file for the is-rosidl-ros2-mix package that enables
#   rosidl messages to be translated into the ros2 middleware

cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)

if(is-rosidl-ros2-std_msgs-mix_INCLUDED)
  return()
endif()
set(is-rosidl-ros2-std_msgs-mix_INCLUDED TRUE)

if(NOT TARGET is-rosidl-ros2-std_msgs-mix)
  include("${CMAKE_CURRENT_LIST_DIR}/is-rosidl-ros2-std_msgs-mix-target.cmake")
endif()

set(is-rosidl-ros2-std_msgs-mix_FOUND TRUE)
