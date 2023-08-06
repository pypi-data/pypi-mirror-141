cmake_minimum_required(VERSION 3.5.0)

# scikit-build test
if(SKBUILD)
    message(STATUS "The project is built using scikit-build")
endif()

message(STATUS "The generator is: ${CMAKE_GENERATOR}")
message(STATUS "The build type is: ${CMAKE_BUILD_TYPE}")
message(STATUS "The toolchain is: ${CMAKE_TOOLCHAIN_FILE}")


# set the project name
project(mixstream)

# manage dependencies
## set vars
set(USE_WIN_DEP OFF CACHE BOOL "Use dependencies from an external package")

## find python deps
find_package(Python REQUIRED)
find_package(PythonExtensions REQUIRED)
find_package(Cython REQUIRED)

## get deps
if (WIN32 AND USE_WIN_DEP)
    message(STATUS "Use downloaded dependencies")

    set(DEPENDENCY_FOLDER "${PROJECT_SOURCE_DIR}/win_dep")

    # glib
    find_path(GLIB2_INCLUDE_DIRS_0 NAMES glib.h PATHS "${DEPENDENCY_FOLDER}/include/glib-2.0")
    find_path(GLIB2_INCLUDE_DIRS_1 NAMES glibconfig.h PATHS "${DEPENDENCY_FOLDER}/lib/glib-2.0/include")
    list(APPEND GLIB2_INCLUDE_DIRS ${GLIB2_INCLUDE_DIRS_0})
    list(APPEND GLIB2_INCLUDE_DIRS ${GLIB2_INCLUDE_DIRS_1})
    find_library(GLIB2_LINK_LIBRARIES NAMES glib-2.0 PATHS "${DEPENDENCY_FOLDER}/lib")
    # gthread
    find_path(GTHREAD2_INCLUDE_DIRS NAMES glib/gthread.h PATHS "${DEPENDENCY_FOLDER}/include/glib-2.0")
    find_library(GTHREAD2_LINK_LIBRARIES NAMES gthread-2.0 PATHS "${DEPENDENCY_FOLDER}/lib")
    # sdl_mixer
    find_package(FindSDL_mixer)
    # soundtouch
    find_path(SOUNDTOUCH_INCLUDE_DIRS NAMES SoundTouch.h SoundTouchDLL.h PATHS "${DEPENDENCY_FOLDER}/include/soundtouch")
    find_library(SOUNDTOUCH_LINK_LIBRARIES NAMES libsoundtouch soundtouch soundtouchdll_x64 soundtouchdll_x86 soundtouchdll soundtouch-c PATHS "${DEPENDENCY_FOLDER}/lib")
    # vorbisfile
    find_path(VORBISFILE_INCLUDE_DIRS NAMES vorbis/vorbisfile.h PATHS "${DEPENDENCY_FOLDER}/include")
    find_library(VORBISFILE_LINK_LIBRARIES NAMES vorbisfile PATHS "${DEPENDENCY_FOLDER}/lib")

else()
    message(STATUS "Use pkgconfig")

    find_package(PkgConfig REQUIRED)
    pkg_search_module(GLIB2 REQUIRED glib-2.0 IMPORTED_TARGET)
    pkg_search_module(GTHREAD2 REQUIRED gthread-2.0 IMPORTED_TARGET)
    pkg_search_module(SOUNDTOUCH REQUIRED soundtouch soundtouch-1.0 soundtouch-1.4 IMPORTED_TARGET)
    pkg_search_module(VORBISFILE REQUIRED vorbisfile IMPORTED_TARGET)
    find_package(SDL_mixer REQUIRED)
endif()


# build the project
add_subdirectory(mixstream)
