// generated from is-ros2/resources/convert__msg.hpp.em
// generated code does not contain a copyright notice



#ifndef _IS_SH_ROS2_ROSIDL__ROS2__BUILTIN_INTERFACES__MSG__CONVERT__MSG__TIME_HPP_
#define _IS_SH_ROS2_ROSIDL__ROS2__BUILTIN_INTERFACES__MSG__CONVERT__MSG__TIME_HPP_

#include <stdexcept>

// Include the header for the generic message type
// #include <is/core/Message.hpp>

// Include the header for the conversions
#include <is/utils/Convert.hpp>

// Include the header for the logger
#include <is/utils/Log.hpp>

// Include the header for the concrete ros2 message type
#include <builtin_interfaces/msg/time.hpp>

// Include the headers for the message conversion dependencies
// <none>

namespace eprosima {
namespace is {
namespace sh {
namespace ros2 {
namespace convert__builtin_interfaces__msg__time {

using Ros2_Msg = builtin_interfaces::msg::Time;
const std::string g_msg_name = "builtin_interfaces/Time";
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
        throw std::runtime_error("Failed while parsing type builtin_interfaces::msg::Time");
    }
    static eprosima::xtypes::StructType type(context.module().structure("builtin_interfaces::msg::Time"));
    type.name(g_msg_name);
    return type;
}

//==============================================================================
inline void convert_to_ros2(const eprosima::xtypes::ReadableDynamicDataRef& from, Ros2_Msg& to)
{
    utils::Convert<Ros2_Msg::_nanosec_type>::from_xtype_field(from["nanosec"], to.nanosec);
    utils::Convert<Ros2_Msg::_sec_type>::from_xtype_field(from["sec"], to.sec);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

//==============================================================================
inline void convert_to_xtype(const Ros2_Msg& from, eprosima::xtypes::WritableDynamicDataRef to)
{
    utils::Convert<Ros2_Msg::_nanosec_type>::to_xtype_field(from.nanosec, to["nanosec"]);
    utils::Convert<Ros2_Msg::_sec_type>::to_xtype_field(from.sec, to["sec"]);

  // Suppress possible unused variable warnings
    (void)from;
    (void)to;
}

static eprosima::is::utils::Logger logger ("is::sh::ROS2");

} //  namespace convert__builtin_interfaces__msg__time
} //  namespace ros2
} //  namespace sh

namespace utils {
template<>
struct Convert<sh::ros2::convert__builtin_interfaces__msg__time::Ros2_Msg>
    : MessageConvert<
     sh::ros2::convert__builtin_interfaces__msg__time::Ros2_Msg,
    &sh::ros2::convert__builtin_interfaces__msg__time::convert_to_ros2,
    &sh::ros2::convert__builtin_interfaces__msg__time::convert_to_xtype
    > { };

} //  namespace utils
} //  namespace is
} //  namespace eprosima

#endif // _IS_SH_ROS2_ROSIDL__ROS2__BUILTIN_INTERFACES__MSG__CONVERT__MSG__TIME_HPP_
