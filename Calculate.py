# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:23:22 2022

@author: Vollhüter
"""

import numpy as np
import Multis


class Tracer:
    """Calculate Tracer."""

    def __init__(self, par, Cin, rain):

        Multis.Multis()

        par.Thalf = par.Thalf_1

        res = Multis.Multis.runMultis(Cin, rain[1], par)

        self.result = res[:rain.shape[0]]


class TracerTracer:
    """Calculate Tracer Tracer."""

    def __init__(self, par, Cin, Cin_2, rain, rain_2, TTs):

        result_tt = np.zeros((2, len(TTs), rain.shape[0]))

        k = 0
        for n in TTs:

            Multis.Multis()

            par.TT = n
            par.Thalf = par.Thalf_1
            res = Multis.Multis.runMultis(Cin, rain[1], par)
            result_tt[0, k] = res[:rain.shape[0]]

            par.Thalf = par.Thalf_2
            res = Multis.Multis.runMultis(Cin_2, rain_2[1], par)
            result_tt[1, k] = res[:rain_2.shape[0]]

            k += 1

        self.result_tt = result_tt


class TriHe:
    """Calculate tritium helium."""

    def __init__(self, par, Cin, rain, TTs):

        result_tt = np.zeros((2, len(TTs), rain.shape[0]))

        k = 0
        for n in TTs:

            Multis.Multis()

            par.TT = n
            par.Thalf = par.Thalf_1
            res = Multis.Multis.runMultis(Cin, rain[1], par)
            result_tt[0, k] = res[:rain.shape[0]]

            par.Thalf = par.Thalf_2
            res = Multis.Multis.runMultis(Cin, rain[1], par)
            result_tt[1, k] = res[:rain.shape[0]]

            k += 1

        self.result_tt = result_tt
