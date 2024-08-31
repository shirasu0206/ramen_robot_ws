// generated from is-ros2/resources/convert__msg.hpp.em
// generated code does not contain a copyright notice



#ifndef _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__HEADER_HPP_
#define _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__HEADER_HPP_

#include <stdexcept>

// Include the header for the generic message type
// #include <is/core/Message.hpp>

// Include the header for the conversions
#include <is/utils/Convert.hpp>

// Include the header for the logger
#include <is/utils/Log.hpp>

// Include the header for the concrete ros2 message type
#include <std_msgs/msg/header.hpp>

// Include the headers for the message conversion dependencies
#include <is/rosidl/ros2/builtin_interfaces/msg/convert__msg__Time.hpp> // stamp

namespace eprosima {
namespace is {
namespace sh {
namespace ros2 {
namespace convert__std_msgs__msg__header {

using Ros2_Msg = std_msgs::msg::Header;
const std::string g_msg_name = "std_msgs/Header";
const std::string g_idl = R"~~~(
module builtin_interfaces {
  module msg {
    @verbatim (language="comment", text=
      "This message communicates ROS Time defined here:" "\n"
      "https://design.ros2.org/articles/clock_and_time.html")
    struct Time {
      @verbatim (language="comment", text=
        "The seconds component, valid over all int32 values.")
      int32 sec;
      @verbatim (language="comment", text=
        "The nanoseconds component, valid in the range [0, 10e9).")
      uint32 nanosec;
    };
  };
};
module std_msgs {
  module msg {
    @verbatim (language="comment", text=
      "Standard metadata for higher-level stamped data types." "\n"
      "This is generally used to communicate timestamped data" "\n"
      "in a particular coordinate frame.")
    struct Header {
      @verbatim (language="comment", text=
        "Two-integer timestamp that is expressed as seconds and nanoseconds.")
      builtin_interfaces::msg::Time stamp;
      @verbatim (language="comment", text=
        "Transform frame with which this data is associated.")
      string frame_id;
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
        throw std::runtime_error("Failed while parsing type std_msgs::msg::Header");
    }
    static eprosima::xtypes::StructType type(context.module().structure("std_msgs::msg::Header"));
    type.name(g_msg_name);
    return type;
}

//==============================================================================
inline void convert_to_ros2(const eprosima::xtypes::ReadableDynamicDataRef& from, Ros2_Msg& to)
{
    utils::Convert<Ros2_Msg::_frame_id_type>::from_xtype_field(from["frame_id"], to.frame_id);
    utils::Convert<Ros2_Msg::_stamp_type>::from_xtype_field(from["stamp"], to.stamp);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

//==============================================================================
inline void convert_to_xtype(const Ros2_Msg& from, eprosima::xtypes::WritableDynamicDataRef to)
{
    utils::Convert<Ros2_Msg::_frame_id_type>::to_xtype_field(from.frame_id, to["frame_id"]);
    utils::Convert<Ros2_Msg::_stamp_type>::to_xtype_field(from.stamp, to["stamp"]);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

static eprosima::is::utils::Logger logger ("is::sh::ROS2");

} //  namespace convert__std_msgs__msg__header
} //  namespace ros2
} //  namespace sh

namespace utils {
template<>
struct Convert<sh::ros2::convert__std_msgs__msg__header::Ros2_Msg>
    : MessageConvert<
     sh::ros2::convert__std_msgs__msg__header::Ros2_Msg,
    &sh::ros2::convert__std_msgs__msg__header::convert_to_ros2,
    &sh::ros2::convert__std_msgs__msg__header::convert_to_xtype
    > { };

} //  namespace utils
} //  namespace is
} //  namespace eprosima

#endif // _IS_SH_ROS2_ROSIDL__ROS2__STD_MSGS__MSG__CONVERT__MSG__HEADER_HPP_
