# -*- coding: utf-8 -*-
"""
@date: 2022

@author: Jonas Vollhueter
"""

import pandas as pd
import numpy as np

class PreSettingOne():

    def __init__(self, par):

        self.rain = PrepareData.readDatas(par.input_c_1_path)
        self.rain_2 = PrepareData.readDatas(par.input_c_2_path)
        self.sample = PrepareData.readDatas(par.sample_file_path) 
        self.rain = PrepareData.convertTimeC(self.rain)
        self.rain_2 = PrepareData.convertTimeC( self.rain_2)
        self.sample = PrepareData.convertTimeS(self.sample)
        self.rain = PrepareData.checkZero(self.rain)
        self.rain_2 = PrepareData.checkZero(self.rain_2)
        self.c_in_1 = PrepareData.weightVolumes(par, self.rain)
        self.c_in_2 = PrepareData.weightVolumes(par, self.rain_2)
        par.TTs = np.arange(2.5, 102.5, 2.5)
        par.vis_gw_age = [5, 10, 20, 40, 80]

class PrepareData:
    """Pre processing."""

    def __init__(self, par):
        pass
        #MARKER tests (e.g. check existance of file pathes, etc.)

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
        # MARKER test the time series for outliers and print warning

    def weightVolumes(par, input_c):
        """Weight the tracer input after the volume of precipitation."""
        datas_grouped_y = input_c.groupby(input_c['Date'].dt.year)
        listed_years = []
        for y in datas_grouped_y.groups.keys():
            year = datas_grouped_y.get_group(y).copy()
            sum_y = year.loc[:, 2].sum()
            year['weighted_c'] = 12 * year[3] * year[2] / sum_y
            listed_years.append(year)
        datas_w = pd.concat(listed_years).sort_values('Date')
        par.weighted = True
        return datas_w


class Par():
    """Parameterisation for jupyter notebooks."""

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

    def rechargeEmpirical(datas, par):
        """Preprocess the input datas with an empirical factor."""
        fe = pd.read_csv(par.uz_path, sep=';')
        datas_grouped_m = datas.groupby(datas['Date'].dt.month)
        monthes = []
        for n in range(datas_grouped_m.ngroups):
            month = datas_grouped_m.get_group(n+1).copy()
            month[2] = datas_grouped_m.get_group(n+1)[2] * fe['P'][n]
            month[3] = datas_grouped_m.get_group(n+1)[3] * fe['C'][n]
            monthes.append(month)
        datas_f = pd.concat(monthes).sort_values('Date')  # MARKER sort index
        return datas_f

    def rechargeModelled(datas, par):
        """Preprocess the input datas with results of hydrological model."""
        f = pd.read_csv(par.uz_path, sep=';')
        datas[2] = datas[2] * f['P']
        datas[3] = datas[3] * f['C']
        return datas
