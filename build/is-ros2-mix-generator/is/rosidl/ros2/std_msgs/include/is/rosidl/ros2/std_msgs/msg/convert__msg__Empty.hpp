// generated from is-ros2/resources/convert__msg.hpp.em
// generated code does not contain a copyright notice



#ifndef _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__EMPTY_HPP_
#define _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__EMPTY_HPP_

#include <stdexcept>

// Include the header for the generic message type
// #include <is/core/Message.hpp>

// Include the header for the conversions
#include <is/utils/Convert.hpp>

// Include the header for the logger
#include <is/utils/Log.hpp>

// Include the header for the concrete ros2 message type
#include <std_msgs/msg/empty.hpp>

// Include the headers for the message conversion dependencies
// <none>

namespace eprosima {
namespace is {
namespace sh {
namespace ros2 {
namespace convert__std_msgs__msg__empty {

using Ros2_Msg = std_msgs::msg::Empty;
const std::string g_msg_name = "std_msgs/Empty";
const std::string g_idl = R"~~~(
module std_msgs {
  module msg {
    struct Empty {
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
        throw std::runtime_error("Failed while parsing type std_msgs::msg::Empty");
    }
    static eprosima::xtypes::StructType type(context.module().structure("std_msgs::msg::Empty"));
    type.name(g_msg_name);
    return type;
}

//==============================================================================
inline void convert_to_ros2(const eprosima::xtypes::ReadableDynamicDataRef& from, Ros2_Msg& to)
{

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

//==============================================================================
inline void convert_to_xtype(const Ros2_Msg& from, eprosima::xtypes::WritableDynamicDataRef to)
{

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

static eprosima::is::utils::Logger logger ("is::sh::ROS2");

} //  namespace convert__std_msgs__msg__empty
} //  namespace ros2
} //  namespace sh

namespace utils {
template<>
struct Convert<sh::ros2::convert__std_msgs__msg__empty::Ros2_Msg>
    : MessageConvert<
     sh::ros2::convert__std_msgs__msg__empty::Ros2_Msg,
    &sh::ros2::convert__std_msgs__msg__empty::convert_to_ros2,
    &sh::ros2::convert__std_msgs__msg__empty::convert_to_xtype
    > { };

} //  namespace utils
} //  namespace is
} //  namespace eprosima

#endif // _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__EMPTY_HPP_
