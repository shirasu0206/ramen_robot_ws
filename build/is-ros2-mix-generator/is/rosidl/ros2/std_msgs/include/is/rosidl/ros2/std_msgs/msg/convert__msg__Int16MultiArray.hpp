// generated from is-ros2/resources/convert__msg.hpp.em
// generated code does not contain a copyright notice



#ifndef _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_MULTI_ARRAY_HPP_
#define _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_MULTI_ARRAY_HPP_

#include <stdexcept>

// Include the header for the generic message type
// #include <is/core/Message.hpp>

// Include the header for the conversions
#include <is/utils/Convert.hpp>

// Include the header for the logger
#include <is/utils/Log.hpp>

// Include the header for the concrete ros2 message type
#include <std_msgs/msg/int16_multi_array.hpp>

// Include the headers for the message conversion dependencies
#include <is/rosidl/ros2/std_msgs/msg/convert__msg__MultiArrayLayout.hpp> // layout

namespace eprosima {
namespace is {
namespace sh {
namespace ros2 {
namespace convert__std_msgs__msg__int16_multi_array {

using Ros2_Msg = std_msgs::msg::Int16MultiArray;
const std::string g_msg_name = "std_msgs/Int16MultiArray";
const std::string g_idl = R"~~~(
module std_msgs {
  module msg {
    @verbatim (language="comment", text=
      "This was originally provided as an example message." "\n"
      "It is deprecated as of Foxy" "\n"
      "It is recommended to create your own semantically meaningful message." "\n"
      "However if you would like to continue using this please use the equivalent in example_msgs.")
    struct MultiArrayDimension {
      @verbatim (language="comment", text=
        "label of given dimension")
      string label;
      @verbatim (language="comment", text=
        "size of given dimension (in type units)")
      uint32 size;
      @verbatim (language="comment", text=
        "stride of given dimension")
      uint32 stride;
    };
  };
};
module std_msgs {
  module msg {
    @verbatim (language="comment", text=
      "This was originally provided as an example message." "\n"
      "It is deprecated as of Foxy" "\n"
      "It is recommended to create your own semantically meaningful message." "\n"
      "However if you would like to continue using this please use the equivalent in example_msgs.")
    struct MultiArrayLayout {
      @verbatim (language="comment", text=
        "The multiarray declares a generic multi-dimensional array of a" "\n"
        "particular data type.  Dimensions are ordered from outer most" "\n"
        "to inner most." "\n"
        "" "\n"
        "Accessors should ALWAYS be written in terms of dimension stride" "\n"
        "and specified outer-most dimension first." "\n"
        "" "\n"
        "multiarray(i,j,k) = data[data_offset + dim_stride[1]*i + dim_stride[2]*j + k]" "\n"
        "" "\n"
        "A standard, 3-channel 640x480 image with interleaved color channels" "\n"
        "would be specified as:" "\n"
        "" "\n"
        "dim[0].label  = \"height\"" "\n"
        "dim[0].size   = 480" "\n"
        "dim[0].stride = 3*640*480 = 921600  (note dim[0] stride is just size of image)" "\n"
        "dim[1].label  = \"width\"" "\n"
        "dim[1].size   = 640" "\n"
        "dim[1].stride = 3*640 = 1920" "\n"
        "dim[2].label  = \"channel\"" "\n"
        "dim[2].size   = 3" "\n"
        "dim[2].stride = 3" "\n"
        "" "\n"
        "multiarray(i,j,k) refers to the ith row, jth column, and kth channel." "\n"
        "Array of dimension properties")
      sequence<std_msgs::msg::MultiArrayDimension> dim;
      @verbatim (language="comment", text=
        "padding bytes at front of data")
      uint32 data_offset;
    };
  };
};
module std_msgs {
  module msg {
    @verbatim (language="comment", text=
      "This was originally provided as an example message." "\n"
      "It is deprecated as of Foxy" "\n"
      "It is recommended to create your own semantically meaningful message." "\n"
      "However if you would like to continue using this please use the equivalent in example_msgs.")
    struct Int16MultiArray {
      @verbatim (language="comment", text=
        "Please look at the MultiArrayLayout message definition for" "\n"
        "documentation on all multiarrays." "\n"
        "specification of data layout")
      std_msgs::msg::MultiArrayLayout layout;
      @verbatim (language="comment", text=
        "array of data")
      sequence<int16> data;
    };
  };
};

)~~~";

//==============================================================================
inline const eprosima::xtypes::StructType& type()
{
    eprosima::xtypes::idl::Context context;
    context.allow_keyword_identifiers = true;
    context.ignore_redefinition = true;
    eprosima::xtypes::idl::parse(g_idl, context);
    if (!context.success)
    {
        throw std::runtime_error("Failed while parsing type std_msgs::msg::Int16MultiArray");
    }
    static eprosima::xtypes::StructType type(context.module().structure("std_msgs::msg::Int16MultiArray"));
    type.name(g_msg_name);
    return type;
}

//==============================================================================
inline void convert_to_ros2(const eprosima::xtypes::ReadableDynamicDataRef& from, Ros2_Msg& to)
{
    utils::Convert<Ros2_Msg::_data_type>::from_xtype_field(from["data"], to.data);
    utils::Convert<Ros2_Msg::_layout_type>::from_xtype_field(from["layout"], to.layout);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

//==============================================================================
inline void convert_to_xtype(const Ros2_Msg& from, eprosima::xtypes::WritableDynamicDataRef to)
{
    utils::Convert<Ros2_Msg::_data_type>::to_xtype_field(from.data, to["data"]);
    utils::Convert<Ros2_Msg::_layout_type>::to_xtype_field(from.layout, to["layout"]);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

static eprosima::is::utils::Logger logger ("is::sh::ROS2");

} //  namespace convert__std_msgs__msg__int16_multi_array
} //  namespace ros2
} //  namespace sh

namespace utils {
template<>
struct Convert<sh::ros2::convert__std_msgs__msg__int16_multi_array::Ros2_Msg>
    : MessageConvert<
     sh::ros2::convert__std_msgs__msg__int16_multi_array::Ros2_Msg,
    &sh::ros2::convert__std_msgs__msg__int16_multi_array::convert_to_ros2,
    &sh::ros2::convert__std_msgs__msg__int16_multi_array::convert_to_xtype
    > { };

} //  namespace utils
} //  namespace is
} //  namespace eprosima

#endif // _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_MULTI_ARRAY_HPP_
