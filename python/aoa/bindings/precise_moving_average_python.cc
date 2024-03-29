/*
 * Copyright 2022 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(precise_moving_average.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(f125576897e27474452e1f44b0f73375)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/aoa/precise_moving_average.h>
// pydoc.h is automatically generated in the build directory
#include <precise_moving_average_pydoc.h>

void bind_precise_moving_average(py::module& m)
{

    using precise_moving_average    = ::gr::aoa::precise_moving_average;


    py::class_<precise_moving_average, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<precise_moving_average>>(m, "precise_moving_average", D(precise_moving_average))

        .def(py::init(&precise_moving_average::make),
           py::arg("length"),
           py::arg("max_iter") = 4096,
           D(precise_moving_average,make)
        )
        



        ;




}








