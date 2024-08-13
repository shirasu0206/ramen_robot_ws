#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "is::is-core" for configuration ""
set_property(TARGET is::is-core APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(is::is-core PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_NOCONFIG "Boost::program_options"
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libis-core.so.3.1.0"
  IMPORTED_SONAME_NOCONFIG "libis-core.so.3.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS is::is-core )
list(APPEND _IMPORT_CHECK_FILES_FOR_is::is-core "${_IMPORT_PREFIX}/lib/libis-core.so.3.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
