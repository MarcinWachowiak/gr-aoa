find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_AOA gnuradio-aoa)

FIND_PATH(
    GR_AOA_INCLUDE_DIRS
    NAMES gnuradio/aoa/api.h
    HINTS $ENV{AOA_DIR}/include
        ${PC_AOA_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_AOA_LIBRARIES
    NAMES gnuradio-aoa
    HINTS $ENV{AOA_DIR}/lib
        ${PC_AOA_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-aoaTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_AOA DEFAULT_MSG GR_AOA_LIBRARIES GR_AOA_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_AOA_LIBRARIES GR_AOA_INCLUDE_DIRS)
