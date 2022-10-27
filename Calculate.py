# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:23:22 2022

@author: Jonas Vollhueter
"""

import numpy as np
import Multis


class Tracer:
    """Calculate Tracer."""

    def __init__(self, par, data_frame):

        Multis.Multis()

        par.Thalf = par.halftime_1

        if par.weighted is True:
            c = data_frame['weighted_c']
        else:
            c = data_frame[3]

        res = Multis.Multis.runMultis(c, par)

        self.result = res[:data_frame.shape[0]]


class TracerTracer:
    """Calculate Tracer Tracer."""

    def __init__(self, par, data_frame_1, data_frame_2):

        result_tt = np.zeros((2, len(par.TTs), data_frame_1.shape[0]))

        if par.weighted is True:
            c_1 = data_frame_1['weighted_c']
            c_2 = data_frame_2['weighted_c']
        else:
            c_1 = data_frame_1[3]
            c_2 = data_frame_2[3]

        k = 0
        for n in par.TTs:

            Multis.Multis()

            par.mean_gw_age = n
            par.Thalf = par.halftime_1
            res = Multis.Multis.runMultis(c_1, par)
            result_tt[0, k] = res[:c_1.shape[0]]

            par.Thalf = par.halftime_2
            res = Multis.Multis.runMultis(c_2, par)
            result_tt[1, k] = res[:c_2.shape[0]]

            k += 1

        self.result = result_tt


class TriHe:
    """Calculate tritium helium."""

    def __init__(self, par, data_frame_1, data_frame_2):

        result_tt = np.zeros((2, len(par.TTs), data_frame_1.shape[0]))

        if par.weighted is True:
            c_1 = data_frame_1['weighted_c']
            c_2 = data_frame_2['weighted_c']
        else:
            c_1 = data_frame_1[3]
            c_2 = data_frame_2[3]

        k = 0
        for n in par.TTs:

            Multis.Multis()

            par.mean_gw_age = n
            par.Thalf = par.halftime_2
            res = Multis.Multis.runMultis(c_1, par)
            result_tt[0, k] = res[:c_1.shape[0]]

            par.Thalf = np.inf
            res = Multis.Multis.runMultis(c_2, par)
            result_tt[1, k] = res[:c_2.shape[0]]

            k += 1

        self.result = result_tt
