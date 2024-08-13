# - Config file for the is-rosidl-ros2-mix package that enables
#   rosidl messages to be translated into the ros2 middleware

cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)

if(is-rosidl-ros2-builtin_interfaces-mix_INCLUDED)
  return()
endif()
set(is-rosidl-ros2-builtin_interfaces-mix_INCLUDED TRUE)

if(NOT TARGET is-rosidl-ros2-builtin_interfaces-mix)
  include("${CMAKE_CURRENT_LIST_DIR}/is-rosidl-ros2-builtin_interfaces-mix-target.cmake")
endif()

set(is-rosidl-ros2-builtin_interfaces-mix_FOUND TRUE)
