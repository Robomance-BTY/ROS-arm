# FindZBar.cmake

find_path(ZBAR_INCLUDE_DIR NAMES zbar.h)
find_library(ZBAR_LIBRARY NAMES zbar)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(ZBar DEFAULT_MSG ZBAR_INCLUDE_DIR ZBAR_LIBRARY)

if(ZBAR_FOUND)
  set(ZBar_LIBRARIES ${ZBAR_LIBRARY})
  set(ZBar_INCLUDE_DIRS ${ZBAR_INCLUDE_DIR})
endif()
