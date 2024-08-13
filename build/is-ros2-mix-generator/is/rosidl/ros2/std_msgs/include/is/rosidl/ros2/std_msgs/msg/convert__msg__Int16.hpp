// generated from is-ros2/resources/convert__msg.hpp.em
// generated code does not contain a copyright notice



#ifndef _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_HPP_
#define _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_HPP_

#include <stdexcept>

// Include the header for the generic message type
// #include <is/core/Message.hpp>

// Include the header for the conversions
#include <is/utils/Convert.hpp>

// Include the header for the logger
#include <is/utils/Log.hpp>

// Include the header for the concrete ros2 message type
#include <std_msgs/msg/int16.hpp>

// Include the headers for the message conversion dependencies
// <none>

namespace eprosima {
namespace is {
namespace sh {
namespace ros2 {
namespace convert__std_msgs__msg__int16 {

using Ros2_Msg = std_msgs::msg::Int16;
const std::string g_msg_name = "std_msgs/Int16";
const std::string g_idl = R"~~~(
module std_msgs {
  module msg {
    @verbatim (language="comment", text=
      "This was originally provided as an example message." "\n"
      "It is deprecated as of Foxy" "\n"
      "It is recommended to create your own semantically meaningful message." "\n"
      "However if you would like to continue using this please use the equivalent in example_msgs.")
    struct Int16 {
      int16 data;
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
        throw std::runtime_error("Failed while parsing type std_msgs::msg::Int16");
    }
    static eprosima::xtypes::StructType type(context.module().structure("std_msgs::msg::Int16"));
    type.name(g_msg_name);
    return type;
}

//==============================================================================
inline void convert_to_ros2(const eprosima::xtypes::ReadableDynamicDataRef& from, Ros2_Msg& to)
{
    utils::Convert<Ros2_Msg::_data_type>::from_xtype_field(from["data"], to.data);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

//==============================================================================
inline void convert_to_xtype(const Ros2_Msg& from, eprosima::xtypes::WritableDynamicDataRef to)
{
    utils::Convert<Ros2_Msg::_data_type>::to_xtype_field(from.data, to["data"]);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

static eprosima::is::utils::Logger logger ("is::sh::ROS2");

} //  namespace convert__std_msgs__msg__int16
} //  namespace ros2
} //  namespace sh

namespace utils {
template<>
struct Convert<sh::ros2::convert__std_msgs__msg__int16::Ros2_Msg>
    : MessageConvert<
     sh::ros2::convert__std_msgs__msg__int16::Ros2_Msg,
    &sh::ros2::convert__std_msgs__msg__int16::convert_to_ros2,
    &sh::ros2::convert__std_msgs__msg__int16::convert_to_xtype
    > { };

} //  namespace utils
} //  namespace is
} //  namespace eprosima

#endif // _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__INT16_HPP_
