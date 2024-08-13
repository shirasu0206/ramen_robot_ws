# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/saba/workspaces/ramen_robot_ws/build/is-mock

# Include any dependencies generated for this target.
include CMakeFiles/is-mock.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/is-mock.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/is-mock.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/is-mock.dir/flags.make

CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o: CMakeFiles/is-mock.dir/flags.make
CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o: /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock/src/SystemHandle.cpp
CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o: CMakeFiles/is-mock.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/saba/workspaces/ramen_robot_ws/build/is-mock/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o -MF CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o.d -o CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o -c /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock/src/SystemHandle.cpp

CMakeFiles/is-mock.dir/src/SystemHandle.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/is-mock.dir/src/SystemHandle.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock/src/SystemHandle.cpp > CMakeFiles/is-mock.dir/src/SystemHandle.cpp.i

CMakeFiles/is-mock.dir/src/SystemHandle.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/is-mock.dir/src/SystemHandle.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock/src/SystemHandle.cpp -o CMakeFiles/is-mock.dir/src/SystemHandle.cpp.s

# Object files for target is-mock
is__mock_OBJECTS = \
"CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o"

# External object files for target is-mock
is__mock_EXTERNAL_OBJECTS =

is/mock/lib/libis-mock.so.3.1.0: CMakeFiles/is-mock.dir/src/SystemHandle.cpp.o
is/mock/lib/libis-mock.so.3.1.0: CMakeFiles/is-mock.dir/build.make
is/mock/lib/libis-mock.so.3.1.0: /home/saba/workspaces/ramen_robot_ws/install/is-core/lib/libis-core.so.3.1.0
is/mock/lib/libis-mock.so.3.1.0: /usr/lib/x86_64-linux-gnu/libyaml-cpp.so.0.7.0
is/mock/lib/libis-mock.so.3.1.0: CMakeFiles/is-mock.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/saba/workspaces/ramen_robot_ws/build/is-mock/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared library is/mock/lib/libis-mock.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/is-mock.dir/link.txt --verbose=$(VERBOSE)
	$(CMAKE_COMMAND) -E cmake_symlink_library is/mock/lib/libis-mock.so.3.1.0 is/mock/lib/libis-mock.so.3.1 is/mock/lib/libis-mock.so

is/mock/lib/libis-mock.so.3.1: is/mock/lib/libis-mock.so.3.1.0
	@$(CMAKE_COMMAND) -E touch_nocreate is/mock/lib/libis-mock.so.3.1

is/mock/lib/libis-mock.so: is/mock/lib/libis-mock.so.3.1.0
	@$(CMAKE_COMMAND) -E touch_nocreate is/mock/lib/libis-mock.so

# Rule to build all files generated by this target.
CMakeFiles/is-mock.dir/build: is/mock/lib/libis-mock.so
.PHONY : CMakeFiles/is-mock.dir/build

CMakeFiles/is-mock.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/is-mock.dir/cmake_clean.cmake
.PHONY : CMakeFiles/is-mock.dir/clean

CMakeFiles/is-mock.dir/depend:
	cd /home/saba/workspaces/ramen_robot_ws/build/is-mock && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock /home/saba/workspaces/ramen_robot_ws/src/Integration-Service/utils/test/mock /home/saba/workspaces/ramen_robot_ws/build/is-mock /home/saba/workspaces/ramen_robot_ws/build/is-mock /home/saba/workspaces/ramen_robot_ws/build/is-mock/CMakeFiles/is-mock.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/is-mock.dir/depend

