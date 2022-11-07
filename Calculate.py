# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:23:22 2022

@author: Vollhüter
"""

import numpy as np
import Multis


class Tracer():
    """Calculate Tracer."""

    def __init__(self, par, Cin, rain, printing=False):

        Multis.Multis()

        par.Thalf = par.Thalf_1

        res = Multis.Multis.runMultis(Cin=Cin, time=rain[1], par=par, printing=printing)

        self.result = res[:rain.shape[0]]


class TracerTracer:
    """Calculate Tracer Tracer."""

    def __init__(self, par, Cin, Cin_2, rain, rain_2, TTs, printing=False):

        result_tt = np.zeros((2, len(TTs), rain.shape[0]))

        k = 0
        for n in TTs:

            Multis.Multis(printing)

            par.TT = n
            par.Thalf = par.Thalf_1
            res = Multis.Multis.runMultis(Cin=Cin, time=rain[1], par=par, printing=printing)
            result_tt[0, k] = res[:rain.shape[0]]

            par.Thalf = par.Thalf_2
            res = Multis.Multis.runMultis(Cin=Cin_2, time=rain_2[1], par=par, printing=printing)
            result_tt[1, k] = res[:rain_2.shape[0]]

            k += 1

        # result_tt has shape (n_tracers, n_mean_TTs, n_rain_data)
        self.result_tt = result_tt


class TriHe:
    """Calculate tritium helium."""

    def __init__(self, par, Cin, rain, TTs, printing=False):

        result_tt = np.zeros((2, len(TTs), rain.shape[0]))

        k = 0
        for n in TTs:

            Multis.Multis(printing=printing)

            par.TT = n
            par.Thalf = par.Thalf_1
            res = Multis.Multis.runMultis(Cin, rain[1], par, printing)
            result_tt[0, k] = res[:rain.shape[0]]

            par.Thalf = par.Thalf_2
            res = Multis.Multis.runMultis(Cin, rain[1], par, printing)
            result_tt[1, k] = res[:rain.shape[0]]

            k += 1

        self.result_tt = result_tt
