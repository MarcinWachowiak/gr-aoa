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
/* BINDTOOL_HEADER_FILE(head_w_rst.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(46a892956ad43421acdd2aea5aa8f4ab)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/aoa/head_w_rst.h>
// pydoc.h is automatically generated in the build directory
#include <head_w_rst_pydoc.h>

void bind_head_w_rst(py::module& m)
{

    using head_w_rst    = ::gr::aoa::head_w_rst;


    py::class_<head_w_rst, gr::block, gr::basic_block,
        std::shared_ptr<head_w_rst>>(m, "head_w_rst", D(head_w_rst))

        .def(py::init(&head_w_rst::make),
           py::arg("sizeof_stream_item"),
           py::arg("nitems"),
           D(head_w_rst,make)
        )
        




        
        .def("reset",&head_w_rst::reset,       
            py::arg("dump_buff"),
            D(head_w_rst,reset)
        )


        
        .def("set_length",&head_w_rst::set_length,       
            py::arg("nitems"),
            D(head_w_rst,set_length)
        )

        ;




}







