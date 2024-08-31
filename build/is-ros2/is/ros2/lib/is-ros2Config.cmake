# - Config file for the is-ros2 package
#
# This package helps is middleware interface extensions to link against

cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)

if(is-ros2_CONFIG_INCLUDED)
  return()
endif()
set(is-ros2_CONFIG_INCLUDED TRUE)

if(NOT TARGET is::is-ros2)
  include("${CMAKE_CURRENT_LIST_DIR}/is-ros2-target.cmake")
endif()

if(NOT TARGET is::ros2)
  add_library(is::ros2 INTERFACE IMPORTED)
  set_target_properties(is::ros2 PROPERTIES
    INTERFACE_LINK_LIBRARIES is::is-ros2
  )
endif()

include(CMakeFindDependencyMacro)
find_dependency(is-core)

foreach(extension )
  include(${CMAKE_CURRENT_LIST_DIR}/extensions/${extension})
endforeach()

foreach(dep rclcpp)
  find_package(${dep} REQUIRED)
endforeach()

set(is-ros2_FOUND TRUE)
