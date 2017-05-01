set(SOURCES
    PostMeshBase.cpp
    PostMeshCurve.cpp
    PostMeshSurface.cpp  
)

set(POSTMESH_LIBRARIES POSTMESH)
add_library(POSTMESH ${SOURCES})
target_link_libraries(POSTMESH ${OCE_LIBRARIES})
set_target_properties(POSTMESH PROPERTIES
        SOVERSION ${${PROJECT_NAME}_ABI_SOVERSION}
        VERSION ${${PROJECT_NAME}_ABI_VERSION})

################################################
# Define output path for generated libraries:  #
# platform/compiler-build_type-bits            #
# for instance:                                #
#     ./win32/bin/vc7.1-release-64             #
#     ./win32/bin/vc9-debug-32                 #
#     ./Unix/i386-debug-64                     #
################################################
if(APPLE)
  set(PLATFORM Darwin)
else(APPLE)
  set(PLATFORM Unix)
endif(APPLE)

set(LIBRARY_OUTPUT_PATH ${PLATFORM}-${CMAKE_SYSTEM_PROCESSOR}-${CMAKE_BUILD_TYPE})
message(STATUS "Library output path: ${LIBRARY_OUTPUT_PATH}")

###########
# INSTALL #
###########
include(GNUInstallDirs)
install(TARGETS ${SMESH_LIBRARIES} DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY ${CMAKE_SOURCE_DIR}/inc/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/smesh)