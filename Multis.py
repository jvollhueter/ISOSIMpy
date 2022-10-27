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

    def runMultis(Cin, par):
        """Calculate flow and decay processes in unsaturated zone."""
        n = len(Cin)
        lambda_ = np.log(2) / par.Thalf
        eta = par.eta

        lambda_ = lambda_ / 12
        TT = par.mean_gw_age * 12
        t = np.arange(1, n+1)

        TT_round = round(TT, 0)

        print('Used Model:')

        # Piston Flow Model
        if par.lpm_type == '1' or par.lpm_type == 'piston flow':
            print('PFM')
            f = np.zeros(n)
            if int(TT_round) <= n:
                f[int(TT_round)-1] = 1
            else:
                print('An error occured. TT > sim per')

        # Exponential Model
        elif par.lpm_type == '2' or par.lpm_type == 'exponential':
            print('Exponential Model')
            f = 1/TT * np.exp(-t/TT)

        # Dispersion Model
        elif par.lpm_type == '3' or par.lpm_type == 'dispersion':
            print('Dispersion Model')
            PD = par.PD
            f = (4 * np.pi * PD * t / TT)**(-0.5) * 1 / t *\
                np.exp(-(1 - t / TT)**2 / (4 * PD * t / TT))

        # Linear Model
        elif par.lpm_type == '4' or par.lpm_type == 'linear':
            print('Linear Model')
            f = np.zeros((n))
            ind = np.where(t <= (2 * TT))
            f[ind[0][0]:ind[0][-1]+1] = 1/(2*TT)

        # Exponential Piston Flow
        elif par.lpm_type == '5' or par.lpm_type == 'exponential piston flow':
            print('Exponential Piston Flow Model')
            f = eta / TT * np.exp(- (eta * t) / TT + eta - 1)
            ind = np.where(t <= (eta-1)*TT/eta)
            if ind[0].size > 0:
                f[ind[0][0]:ind[0][-1]+1] = 0

        else:
            raise KeyError("""Section lpm type in xml file has a not known value. Please check for typos and if necessary read the manual """)

        temp = np.zeros((n, (n*2)))
        for i in range(1, n+1):
            temp[i-1, i-1:n+i-1] = Cin[i-1] * np.exp(-lambda_ * t) * f
        global Cout
        Cout = np.sum(temp, axis=0)

        return Cout
