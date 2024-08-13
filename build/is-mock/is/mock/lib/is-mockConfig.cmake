# - Config file for the is-mock package
#
# This package helps is middleware interface extensions to link against

cmake_minimum_required(VERSION 3.5.1 FATAL_ERROR)

if(is-mock_CONFIG_INCLUDED)
  return()
endif()
set(is-mock_CONFIG_INCLUDED TRUE)

if(NOT TARGET is::is-mock)
  include("${CMAKE_CURRENT_LIST_DIR}/is-mock-target.cmake")
endif()

if(NOT TARGET is::mock)
  add_library(is::mock INTERFACE IMPORTED)
  set_target_properties(is::mock PROPERTIES
    INTERFACE_LINK_LIBRARIES is::is-mock
  )
endif()

include(CMakeFindDependencyMacro)
find_dependency(is-core)

foreach(extension )
  include(${CMAKE_CURRENT_LIST_DIR}/extensions/${extension})
endforeach()

foreach(dep )
  find_package(${dep} REQUIRED)
endforeach()

set(is-mock_FOUND TRUE)
