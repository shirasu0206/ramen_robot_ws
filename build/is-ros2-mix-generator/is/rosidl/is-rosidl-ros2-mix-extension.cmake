
set(_ros2_${package}_use_templates TRUE)

set(_base_ros2_msg_cpp convert__msg.cpp.em)
set(_base_ros2_msg_hpp convert__msg.hpp.em)
set(_base_ros2_srv_cpp convert__srv.cpp.em)
set(_base_ros2_srv_hpp )

# Add the template directory prefix to the template filenames
foreach(transport_type msg srv)
  foreach(file_type cpp hpp)

    set(_ros2_${package}_${transport_type}_${file_type})

    foreach(base ${_base_ros2_${transport_type}_${file_type}})

      list(
        APPEND
        _ros2_${package}_${transport_type}_${file_type}
        "${IS_rosidl_ros2_TEMPLATE_DIR}/${base}"
      )

    endforeach()

  endforeach()
endforeach()
