
#ifndef IS_ROS2_API_H
#define IS_ROS2_API_H

#ifdef IS_ROS2_STATIC_DEFINE
#  define IS_ROS2_API
#  define IS_ROS2_NO_EXPORT
#else
#  ifndef IS_ROS2_API
#    ifdef is_ros2_EXPORTS
        /* We are building this library */
#      define IS_ROS2_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define IS_ROS2_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef IS_ROS2_NO_EXPORT
#    define IS_ROS2_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef IS_ROS2_DEPRECATED
#  define IS_ROS2_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef IS_ROS2_DEPRECATED_EXPORT
#  define IS_ROS2_DEPRECATED_EXPORT IS_ROS2_API IS_ROS2_DEPRECATED
#endif

#ifndef IS_ROS2_DEPRECATED_NO_EXPORT
#  define IS_ROS2_DEPRECATED_NO_EXPORT IS_ROS2_NO_EXPORT IS_ROS2_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef IS_ROS2_NO_DEPRECATED
#    define IS_ROS2_NO_DEPRECATED
#  endif
#endif

#endif /* IS_ROS2_API_H */
