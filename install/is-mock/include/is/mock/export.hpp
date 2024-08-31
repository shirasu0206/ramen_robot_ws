
#ifndef IS_MOCK_API_H
#define IS_MOCK_API_H

#ifdef IS_MOCK_STATIC_DEFINE
#  define IS_MOCK_API
#  define IS_MOCK_NO_EXPORT
#else
#  ifndef IS_MOCK_API
#    ifdef is_mock_EXPORTS
        /* We are building this library */
#      define IS_MOCK_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define IS_MOCK_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef IS_MOCK_NO_EXPORT
#    define IS_MOCK_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef IS_MOCK_DEPRECATED
#  define IS_MOCK_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef IS_MOCK_DEPRECATED_EXPORT
#  define IS_MOCK_DEPRECATED_EXPORT IS_MOCK_API IS_MOCK_DEPRECATED
#endif

#ifndef IS_MOCK_DEPRECATED_NO_EXPORT
#  define IS_MOCK_DEPRECATED_NO_EXPORT IS_MOCK_NO_EXPORT IS_MOCK_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef IS_MOCK_NO_DEPRECATED
#    define IS_MOCK_NO_DEPRECATED
#  endif
#endif

#endif /* IS_MOCK_API_H */
