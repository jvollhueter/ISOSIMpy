# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:26:38 2022

@author: Vollhüter
"""

import numpy as np

class Multis():
    """Calculations of the flow and decay processes in unsaturated zone."""

    def __init__(self):

        print('Your calculations will start soon. Look forward to \
the results!')
        # Marker adding tests here

    def runMultis(Cin, time, par):
        """Calculate flow and decay processes in unsaturated zone."""
        n = len(time)
        lambda_ = np.log(2) / par.Thalf
        eta = par.eta

        if par.step == 0:
            lambda_ = lambda_ / 12
            TT = par.TT * 12
        t = np.arange(1, n+1)

        TT_round = round(TT, 0)

        print('Used Model:')

        if par.MODNUM == 1:  # Piston Flow Model
            print('PFM')
            f = np.zeros(n)
            if int(TT_round) <= n:
                f[int(TT_round)-1] = 1
            else:
                print('An error occured. TT > sim per')

        elif par.MODNUM == 2:  # Exponential Model
            print('Exponential Model')
            f = 1/TT * np.exp(-t/TT)

        elif par.MODNUM == 3:  # Dispersion Model
            print('Dispersion Model')
            PD = par.PD
            f = (4 * np.pi * PD * t / TT)**(-0.5) * 1 / t *\
                np.exp(-(1 - t / TT)**2 / (4 * PD * t / TT))

        elif par.MODNUM == 4:  # Linear Model
            print('Linear Model')
            f = np.zeros((n))
            ind = np.where(t <= (2 * TT))
            f[ind[0][0]:ind[0][-1]+1] = 1/(2*TT)

        elif par.MODNUM == 5:
            print('Exponential Piston Flow Model')
            f = eta / TT * np.exp(- (eta * t) / TT + eta - 1)
            ind = np.where(t <= (eta-1)*TT/eta)
            if ind[0].size > 0:
                f[ind[0][0]:ind[0][-1]+1] = 0

        else:
            pass  # MARKER Error

        """
        Notes on the solution routine / general Multis:
        - why are errors never really raised but only print statements are
            used instead?
        - why not make this a function (of a base-class)?
        - why not use scipy.signal.convolve / scipy.signal.fftconvolve?
            - ultimately, all the LPMs in ISOSIMpy are just an application
                of the convolution integral with different response functions
        - who not have an attribute of the parent object (Multis), which
            stores everything (e.g., results, inputs, etc.) and makes it
            available everywhere
        """

        temp = np.zeros((n, (n*2)))
        for i in range(1, n+1):
            temp[i-1, i-1:n+i-1] = Cin[i-1] * np.exp(-lambda_ * t) * f
        global Cout
        Cout = np.sum(temp, axis=0)
        print(TT_round)

        return Cout
