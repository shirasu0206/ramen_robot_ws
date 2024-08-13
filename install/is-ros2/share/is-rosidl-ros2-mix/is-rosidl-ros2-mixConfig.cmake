# - Config file for the is--ros2-mix package that enables
#    messages to be translated into the ros2 middleware

cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)

if(is-rosidl-ros2-mix_INCLUDED)
  return()
endif()
set(is-rosidl-ros2-mix_INCLUDED TRUE)

set(IS_rosidl_ros2_EXTENSION "${CMAKE_CURRENT_LIST_DIR}/is-rosidl-ros2-mix-extension.cmake")
set(IS_rosidl_ros2_TEMPLATE_DIR "${CMAKE_CURRENT_LIST_DIR}/templates")

foreach(dep )
  find_package(${dep} REQUIRED)
endforeach()
