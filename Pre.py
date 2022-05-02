# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:20:52 2022

@author: Vollhüter
"""

import pandas as pd
import numpy as np

class Pre:
    """Pre processing."""

    def __init__(self, par):
        try:
            par.SOILM != 0
        except KeyError:
            print("""Parameter SOILM has to be 0. There is no pre processing
 of the vadose zone integrated in this program. Check your input!""")
        try:
            par.step != 0 or par.step != 1
        except KeyError:
            print("""Parameter step has to be 0 (for yearly values) or 1 (for
 monthly values. Check your input!""")
            exit()


    def readDatas(path):
        """Read in datas."""
        path = pd.read_csv(path, sep=';', header=None)
        return path


    def convertTimeC(input_c):
        """Convert time column in tracer input concentration file."""
        input_c['Date'] = input_c[1].astype(str) +\
            input_c[0].astype(str).str.zfill(2)
        input_c['Date'] = pd.to_datetime(input_c['Date'], format='%Y%m')
        return input_c

    def convertTimeS(input_c):
        """Convert time column in sample input concentration file."""
        input_c['Date'] = pd.to_datetime(input_c[0], format='%d.%m.%Y')
        return input_c

    def checkZero(input_c):
        """Check the input values for <= 0."""
        index_zeros_P = input_c.index[input_c[2] <= 0]
        for n in index_zeros_P:
            input_c.loc[n, 2] = 1e-50
        return input_c

    def checkOutliers(input_c):
        """Check the input values for outliers."""
        pass

    def weightVolumes(input_c):
        """Weight the tracer input after the volume of precipitation."""
        datas_grouped_y = input_c.groupby(input_c['Date'].dt.year)
        listed_years = []
        for y in datas_grouped_y.groups.keys():
            year = datas_grouped_y.get_group(y).copy()
            sum_y = year.loc[:, 2].sum()
            year['weighted_c'] = 12 * year[3] * year[2] / sum_y
            listed_years.append(year)
        datas_w = pd.concat(listed_years).sort_values('Date')
        return datas_w


class Par():
    """Parameterisation."""

    def __init__(self, step=0, TT=30, Thalf_1=12.43, PD=0.1, eta=0.5,
                 Thalf_2=np.inf, SOILM=1, MODNUM=1):
        self.step = step
        self.TT = TT
        self.Thalf_1 = Thalf_1
        self.PD = PD
        self.eta = eta
        self.Thalf_2 = Thalf_2
        self.SOILM = SOILM
        self.MODNUM = MODNUM


class VadoseZone():
    """Calculations in the soil and vadose zone."""

    def rechargeEmpirical(datas, fe_p):
        """Preprocess the input datas with an empirical factor."""
        fe_c = 1.02 - fe_p / 50
        datas_grouped_m = datas.groupby(datas['Date'].dt.month)
        monthes = []
        for n in range(datas_grouped_m.ngroups):
            month = datas_grouped_m.get_group(n+1).copy()
            month[2] = datas_grouped_m.get_group(n+1)[2] * fe_p[n]
            month[3] = datas_grouped_m.get_group(n+1)[3] * fe_c[n]
            monthes.append(month)
        datas_f = pd.concat(monthes).sort_values('Date')  # MARKER sort index
        return datas_f

    def rechargeModelled(datas, f_p):
        """Preprocess the input datas with results of hydrologic model."""
        f_c = 1.02 - f_p / 50
        datas[2] = datas[2] * f_p
        datas[3] = datas[3] * f_c
        return datas
