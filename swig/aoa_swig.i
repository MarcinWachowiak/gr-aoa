/* -*- c++ -*- */

#define BEAMFORMING_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "aoa_swig_doc.i"

%{
#include "aoa/MUSIC_lin_array.h"
#include "aoa/rootMUSIC_linear_array.h"
#include "aoa/shift_phase.h"
#include "aoa/calc_phase_diff.h"
#include "aoa/precise_moving_average.h"
#include "aoa/head_w_rst.h"
#include "aoa/correlate.h"
%}


%include "aoa/MUSIC_lin_array.h"
GR_SWIG_BLOCK_MAGIC2(aoa, MUSIC_lin_array);
%include "aoa/rootMUSIC_linear_array.h"
GR_SWIG_BLOCK_MAGIC2(aoa, rootMUSIC_linear_array);

%include "aoa/shift_phase.h"
GR_SWIG_BLOCK_MAGIC2(aoa, shift_phase);
%include "aoa/calc_phase_diff.h"
GR_SWIG_BLOCK_MAGIC2(aoa, calc_phase_diff);


%include "aoa/precise_moving_average.h"
GR_SWIG_BLOCK_MAGIC2(aoa, precise_moving_average);

%include "aoa/head_w_rst.h"
GR_SWIG_BLOCK_MAGIC2(aoa, head_w_rst);
%include "aoa/correlate.h"
GR_SWIG_BLOCK_MAGIC2(aoa, correlate);
