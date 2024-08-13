# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.6)
   message(FATAL_ERROR "CMake >= 2.6.0 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.6...3.20)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Protect against multiple inclusion, which would fail when already imported targets are added once more.
set(_targetsDefined)
set(_targetsNotDefined)
set(_expectedTargets)
foreach(_expectedTarget is-rosidl-ros2-builtin_interfaces-mix)
  list(APPEND _expectedTargets ${_expectedTarget})
  if(NOT TARGET ${_expectedTarget})
    list(APPEND _targetsNotDefined ${_expectedTarget})
  endif()
  if(TARGET ${_expectedTarget})
    list(APPEND _targetsDefined ${_expectedTarget})
  endif()
endforeach()
if("${_targetsDefined}" STREQUAL "${_expectedTargets}")
  unset(_targetsDefined)
  unset(_targetsNotDefined)
  unset(_expectedTargets)
  set(CMAKE_IMPORT_FILE_VERSION)
  cmake_policy(POP)
  return()
endif()
if(NOT "${_targetsDefined}" STREQUAL "")
  message(FATAL_ERROR "Some (but not all) targets in this export set were already defined.\nTargets Defined: ${_targetsDefined}\nTargets not yet defined: ${_targetsNotDefined}\n")
endif()
unset(_targetsDefined)
unset(_targetsNotDefined)
unset(_expectedTargets)


# Create imported target is-rosidl-ros2-builtin_interfaces-mix
add_library(is-rosidl-ros2-builtin_interfaces-mix SHARED IMPORTED)

set_target_properties(is-rosidl-ros2-builtin_interfaces-mix PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "/home/saba/workspaces/ramen_robot_ws/build/is-ros2-mix-generator/is/rosidl/ros2/builtin_interfaces/include;/opt/ros/humble/include/builtin_interfaces;/opt/ros/humble/include/rosidl_runtime_c;/opt/ros/humble/include/rosidl_typesupport_interface;/opt/ros/humble/include/rcutils;/opt/ros/humble/include/rosidl_runtime_cpp;/opt/ros/humble/include/rosidl_typesupport_fastrtps_c;/opt/ros/humble/include/rosidl_typesupport_fastrtps_cpp;/opt/ros/humble/include/rosidl_typesupport_c;/opt/ros/humble/include/rmw;/opt/ros/humble/include/rosidl_typesupport_cpp;/opt/ros/humble/include/rcpputils;/opt/ros/humble/include/rosidl_typesupport_introspection_c;/opt/ros/humble/include/rosidl_typesupport_introspection_cpp"
  INTERFACE_LINK_LIBRARIES "is::core;is::ros2;/opt/ros/humble/lib/libbuiltin_interfaces__rosidl_generator_c.so;/opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_c.so;/opt/ros/humble/lib/libbuiltin_interfaces__rosidl_typesupport_cpp.so;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;rcutils::rcutils;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rosidl_runtime_c::rosidl_runtime_c;rmw::rmw;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rmw::rmw;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librmw.so;/opt/ros/humble/lib/librosidl_typesupport_fastrtps_cpp.so;fastcdr;rmw::rmw;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librosidl_typesupport_cpp.so;rosidl_runtime_c::rosidl_runtime_c;rosidl_typesupport_c::rosidl_typesupport_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librosidl_typesupport_cpp.so;rosidl_runtime_c::rosidl_runtime_c;rosidl_typesupport_c::rosidl_typesupport_c;rosidl_typesupport_c::rosidl_typesupport_c;/opt/ros/humble/lib/librcutils.so;dl;/opt/ros/humble/lib/librcpputils.so;/opt/ros/humble/lib/librosidl_typesupport_c.so;/opt/ros/humble/lib/librosidl_typesupport_cpp.so;/opt/ros/humble/lib/librosidl_runtime_c.so;rcutils::rcutils;rosidl_typesupport_interface::rosidl_typesupport_interface;rosidl_runtime_c::rosidl_runtime_c;/opt/ros/humble/lib/librosidl_typesupport_introspection_c.so;/opt/ros/humble/lib/librosidl_typesupport_introspection_cpp.so"
)

# Import target "is-rosidl-ros2-builtin_interfaces-mix" for configuration ""
set_property(TARGET is-rosidl-ros2-builtin_interfaces-mix APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(is-rosidl-ros2-builtin_interfaces-mix PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/home/saba/workspaces/ramen_robot_ws/build/is-ros2-mix-generator/is/rosidl/ros2/lib/libis-rosidl-ros2-builtin_interfaces-mix.so"
  IMPORTED_SONAME_NOCONFIG "libis-rosidl-ros2-builtin_interfaces-mix.so"
  )

# This file does not depend on other imported targets which have
# been exported from the same project but in a separate export set.

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
cmake_policy(POP)
