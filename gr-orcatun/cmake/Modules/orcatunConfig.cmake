INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_ORCATUN orcatun)

FIND_PATH(
    ORCATUN_INCLUDE_DIRS
    NAMES orcatun/api.h
    HINTS $ENV{ORCATUN_DIR}/include
        ${PC_ORCATUN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    ORCATUN_LIBRARIES
    NAMES gnuradio-orcatun
    HINTS $ENV{ORCATUN_DIR}/lib
        ${PC_ORCATUN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(ORCATUN DEFAULT_MSG ORCATUN_LIBRARIES ORCATUN_INCLUDE_DIRS)
MARK_AS_ADVANCED(ORCATUN_LIBRARIES ORCATUN_INCLUDE_DIRS)

