# cythonize the pyx file
add_cython_target(_MixStream _MixStream.pyx)

# compile the extension with the lib
add_library(_MixStream MODULE ${_MixStream} MixStream.c vorbis.c soundtouch-c.cpp)
target_include_directories(_MixStream
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}
    PRIVATE ${GLIB2_INCLUDE_DIRS}
    PRIVATE ${GTHREAD2_INCLUDE_DIRS}   # for osx
    PRIVATE ${SDL_MIXER_INCLUDE_DIRS}
    PRIVATE ${SOUNDTOUCH_INCLUDE_DIRS}
    PRIVATE ${VORBISFILE_INCLUDE_DIRS} # for osx
)
target_link_libraries(_MixStream
    ${GLIB2_LINK_LIBRARIES}
    ${GTHREAD2_LINK_LIBRARIES}         # for osx
    ${SDL_MIXER_LIBRARIES}
    ${SOUNDTOUCH_LINK_LIBRARIES}
    ${VORBISFILE_LINK_LIBRARIES}
)
python_extension_module(_MixStream)

# install the module
install(TARGETS _MixStream
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX}/mixstream
    PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Windows: copy DLLs
if (WIN32)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/glib-2.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/libglib-2.0-0.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/gthread-2.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/libgthread-2.0-0.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/vorbisfile.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/libvorbisfile-3.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/SoundTouchDll_x64.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/SoundTouchDll_x84.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/libSoundTouch-0.dll)
    list(APPEND DEPENDENCIES_DLL ${DEPENDENCY_FOLDER}/bin/SDL_mixer.dll)
    foreach(DEP IN LISTS ${DEPENDENCIES_DLL})
        if (EXISTS ${DEP})
            install(FILES ${DEP}
                    DESTINATION ${CMAKE_INSTALL_PREFIX}/mixstream)
        else()
            message(STATUS "${DEP} not found")
        endif()
    endforeach()
endif()
