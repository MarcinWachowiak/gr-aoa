# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT aoa_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT aoa_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND aoa_python_files
    calc_phase_diff_python.cc
    correlate_python.cc
    head_w_rst_python.cc
    MUSIC_lin_array_python.cc
    precise_moving_average_python.cc
    rootMUSIC_linear_array_python.cc
    shift_phase_python.cc
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(aoa
   ../../..
   gr::aoa
   "${aoa_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/aoa/
  DEPENDS aoa_python)

install(TARGETS aoa_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/aoa COMPONENT pythonapi)
