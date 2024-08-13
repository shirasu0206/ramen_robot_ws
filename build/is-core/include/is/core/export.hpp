
#ifndef IS_CORE_API_H
#define IS_CORE_API_H

#ifdef IS_CORE_STATIC_DEFINE
#  define IS_CORE_API
#  define IS_CORE_NO_EXPORT
#else
#  ifndef IS_CORE_API
#    ifdef is_core_EXPORTS
        /* We are building this library */
#      define IS_CORE_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define IS_CORE_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef IS_CORE_NO_EXPORT
#    define IS_CORE_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef IS_CORE_DEPRECATED
#  define IS_CORE_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef IS_CORE_DEPRECATED_EXPORT
#  define IS_CORE_DEPRECATED_EXPORT IS_CORE_API IS_CORE_DEPRECATED
#endif

#ifndef IS_CORE_DEPRECATED_NO_EXPORT
#  define IS_CORE_DEPRECATED_NO_EXPORT IS_CORE_NO_EXPORT IS_CORE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef IS_CORE_NO_DEPRECATED
#    define IS_CORE_NO_DEPRECATED
#  endif
#endif

#endif /* IS_CORE_API_H */
