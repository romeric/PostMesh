
cmake_minimum_required(VERSION 3.0)

set(POSTMESH_VERSION_MAJOR 6)
set(POSTMESH_VERSION_MINOR 7)
set(POSTMESH_VERSION_PATCH)
set(POSTMESH_VERSION_TWEAK)

#####################
# Set ABI SOVERSION #
#####################
set(POSTMESH_ABI_SOVERSION 3)
set(POSTMESH_ABI_VERSION ${POSTMESH_ABI_SOVERSION}.0.0)

set(BUILD_SHARED_LIBS ON)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(Include)

#################
# Setup options #
#################
option(POSTMESH_TESTING "Enable unittest" ON)

set(CXX_OPT_FLAGS "-O3 -march=native -mtune=native -mfpmath=sse -ffast-math -funroll-loops")
set(CXX_WARN_FLAGS "-Wall -Wextra -Wno-unused")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 ${CXX_OPT_FLAGS} ${CXX_WARN_FLAGS}")

set(SOURCE_FILES
    src/PostMeshBase.cpp
    src/PostMeshCurve.cpp
    src/PostMeshSurface.cpp
    )

#############
# Unittest  #
#############
#if(POSTMESH_TESTING)
#    include(CTest)
#    enable_testing()
#    subdirs(test)
#endif(POSTMESH_TESTING)
#
################################
# OCE include and lib location #
################################
set(OCE_REQUIRED_LIBS TKernel TKMath TKBRep TKG2d TKG3d TKMeshVS TKPrim TKGeomBase TKGeomAlgo TKTopAlgo TKShHealing pthread)
find_package(OCE COMPONENTS ${OCE_REQUIRED_LIBS} CONFIG)

if(OCE_FOUND)
    message(STATUS "OpenCASCADE Community Edition found.")
    include_directories(${OCE_INCLUDE_DIRS})
    set(OCE_LIBRARIES ${OCE_REQUIRED_LIBS})
else()
    set( OCE_INCLUDE_PATH /usr/local/include/oce CACHE
        PATH "OCE headers location" )
    set( OCE_LIB_PATH /usr/local/lib CACHE
        PATH "OCE libraries location" )
    set(OCE_LIBRARIES TKernel TKMath TKBRep TKG2d TKG3d TKMeshVS TKPrim TKGeomBase TKGeomAlgo TKTopAlgo TKShHealing pthread)
    # Tells CMake where are the required headers
    include_directories(${OCE_INCLUDE_PATH})
    LINK_DIRECTORIES(${OCE_LIB_PATH})
endif()

set( EIGEN_INCLUDE_PATH /usr/local/include/eigen3 CACHE PATH "Eigen headers location" )
include_directories(${EIGEN_INCLUDE_PATH})

############################
# Default to release build #
############################
if(NOT DEFINED CMAKE_BUILD_TYPE )
  set(CMAKE_BUILD_TYPE "Release")
endif()
message(STATUS "Built type will be ${CMAKE_BUILD_TYPE}")


#################
# Check Fortran #
#################
#if(UNIX)
#  include(CMakeDetermineFortranCompiler)
#endif(UNIX)


############################
# Check 32/64 bit platform #
############################
#if(${CMAKE_SIZEOF_VOID_P} MATCHES "8") # It is 64bit, 32 bit systems returns 4
#    add_definitions(-D_OCC64)
#    message(STATUS "Build 64bit")
#    set(BIT 64)
##else()
#    message(STATUS "Build 32bit")
#    set(BIT 32)
#endif()


######################################################
# Configure Build settings according to the platform #
######################################################
if(UNIX)
    # Same settings are used for both MacOSX and Unix/Linux
    add_definitions(-DHAVE_CONFIG_H -DLIN -DCSFDB -DOCC_CONVERT_SIGNALS)
else(UNIX)
    message("Unknown platform")
endif(UNIX)


#################
# POSTMESH library #
#################
add_subdirectory(src)

#######################
# POSTMESH Documentation #
#######################
# add_subdirectory(doc/src)