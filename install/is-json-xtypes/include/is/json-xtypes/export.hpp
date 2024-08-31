
#ifndef IS_JSON_XTYPES_API_H
#define IS_JSON_XTYPES_API_H

#ifdef IS_JSON_XTYPES_STATIC_DEFINE
#  define IS_JSON_XTYPES_API
#  define IS_JSON_XTYPES_NO_EXPORT
#else
#  ifndef IS_JSON_XTYPES_API
#    ifdef is_json_xtypes_EXPORTS
        /* We are building this library */
#      define IS_JSON_XTYPES_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define IS_JSON_XTYPES_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef IS_JSON_XTYPES_NO_EXPORT
#    define IS_JSON_XTYPES_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef IS_JSON_XTYPES_DEPRECATED
#  define IS_JSON_XTYPES_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef IS_JSON_XTYPES_DEPRECATED_EXPORT
#  define IS_JSON_XTYPES_DEPRECATED_EXPORT IS_JSON_XTYPES_API IS_JSON_XTYPES_DEPRECATED
#endif

#ifndef IS_JSON_XTYPES_DEPRECATED_NO_EXPORT
#  define IS_JSON_XTYPES_DEPRECATED_NO_EXPORT IS_JSON_XTYPES_NO_EXPORT IS_JSON_XTYPES_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef IS_JSON_XTYPES_NO_DEPRECATED
#    define IS_JSON_XTYPES_NO_DEPRECATED
#  endif
#endif

#endif /* IS_JSON_XTYPES_API_H */
