# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:26:38 2022

@author: Vollhüter
"""

import numpy as np

class Multis():
    """
    Calculations of the flow and decay processes in unsaturated zone.
    """

    def __init__(self, printing=False):
        """
        :: Attributes ::
        printing : bool specifying whether to print information (e.g.,
            used model, rounded TT, etc.) to the screen; bool
        
        Note: printing is a global option, i.e., either all possible
            information is printed or none
        """
        
        printing = printing

        if printing:
            print('Your calculations will start soon. Look forward to \
                the results!')
        # Marker adding tests here

    def runMultis(Cin, time, par, printing=False):
        """Calculate flow and decay processes in unsaturated zone."""

        n = len(time)
        lambda_ = np.log(2) / par.Thalf
        eta = par.eta

        if par.step == 0:
            lambda_ = lambda_ / 12
            TT = par.TT * 12
        t = np.arange(1, n+1)

        TT_round = round(TT, 0)

        if printing:
            print('Used Model:')

        if par.MODNUM == 1:  # Piston Flow Model
            if printing:
                print('PFM')
            f = np.zeros(n)
            if int(TT_round) <= n:
                f[int(TT_round)-1] = 1
            else:
                print('An error occured. TT > sim per')

        elif par.MODNUM == 2:  # Exponential Model
            if printing:
                print('Exponential Model')
            f = 1/TT * np.exp(-t/TT)

        elif par.MODNUM == 3:  # Dispersion Model
            if printing:
                print('Dispersion Model')
            PD = par.PD
            f = (4 * np.pi * PD * t / TT)**(-0.5) * 1 / t *\
                np.exp(-(1 - t / TT)**2 / (4 * PD * t / TT))

        elif par.MODNUM == 4:  # Linear Model
            if printing:
                print('Linear Model')
            f = np.zeros((n))
            ind = np.where(t <= (2 * TT))
            f[ind[0][0]:ind[0][-1]+1] = 1/(2*TT)

        elif par.MODNUM == 5:
            if printing:
                print('Exponential Piston Flow Model')
            f = eta / TT * np.exp(- (eta * t) / TT + eta - 1)
            ind = np.where(t <= (eta-1)*TT/eta)
            if ind[0].size > 0:
                f[ind[0][0]:ind[0][-1]+1] = 0
        else:
            pass  # MARKER Error

        temp = np.zeros((n, (n*2)))
        for i in range(1, n+1):
            temp[i-1, i-1:n+i-1] = Cin[i-1] * np.exp(-lambda_ * t) * f
        global Cout
        Cout = np.sum(temp, axis=0)
        if printing:
            print(TT_round)

        return Cout
