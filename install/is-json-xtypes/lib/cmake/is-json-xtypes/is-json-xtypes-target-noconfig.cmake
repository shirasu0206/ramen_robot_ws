#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "is::is-json-xtypes" for configuration ""
set_property(TARGET is::is-json-xtypes APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(is::is-json-xtypes PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libis-json-xtypes.so.3.1.0"
  IMPORTED_SONAME_NOCONFIG "libis-json-xtypes.so.3.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS is::is-json-xtypes )
list(APPEND _IMPORT_CHECK_FILES_FOR_is::is-json-xtypes "${_IMPORT_PREFIX}/lib/libis-json-xtypes.so.3.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
