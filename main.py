# -*- coding: utf-8 -*-
"""
@date: 02/2022

@author: Thomas Woehling, Gesche Reumann, Jonas Vollhueter, Diana Burghardt
"""
import numpy as np

import Pre
import Calculate
import Post

# Doc
# Check markers

pfile = r'in/precipitation.csv'
pfile_2 = r'in/precipitation.csv'
sfile = r'in/samples.csv'
date = 600

show_gw_age = [5, 10, 20, 40, 80]

rain = Pre.Pre.readDatas(pfile)
rain_2 = Pre.Pre.readDatas(pfile_2)
sample = Pre.Pre.readDatas(sfile)

rain = Pre.Pre.convertTimeC(rain)
rain_2 = Pre.Pre.convertTimeC(rain_2)
sample = Pre.Pre.convertTimeS(sample)

# MARKER: creating an example data set:
# rain_2[3] = rain_2[3] * 0.1


MODNUM = 2          # LPM; 1 = Piston Flow, 2 = Exponential Model,
#                     3 = Dispersion Model, 4 = Linear Model,
#                     5 = Exponential Piston Flow Model
SOILM = 0           # Unsaturated zone
step = 0        # Calculation time step (0-month,1-year)
TT = 20         # mean travel time in [years]
Thalf_1 = 12.4  #
Thalf_2 = np.inf    #
PD = 0.1        # = 1/Pe = D/vx = 0.01 .. 1,  dispersion coefficient
eta = 0.5       # V/Vem = ratio of total volume of water to volume
#                     characterized by exponential TTD
par = Pre.Par(step, TT, Thalf_1, PD, eta, Thalf_2, SOILM, MODNUM)

# unsaturaded zone

if SOILM == 0:
    GWN = rain[2]
    GWN_2 = rain_2[2]
    Cin = rain[3]
    Cin_2 = rain_2[3]
elif SOILM == 1:
    pass
elif SOILM == 2:
    pass

##############################################################################
##############################################################################
####################################Tracer####################################
##############################################################################
##############################################################################

# Pre.Pre(par)

# result = Calculate.Tracer(par, Cin, rain)

# Post.Post.tracer(result.result, rain, sample)

##############################################################################
##############################################################################
################################Tracer-Tracer#################################
##############################################################################
##############################################################################

# Pre.Pre(par)

# TTs = np.arange(2.5, 100, 2.5)

# result = Calculate.TracerTracer(par, Cin, Cin_2, rain, rain_2, TTs)

# Post.Post.tracerTracer(result.result_tt, rain, rain_2, date, show_gw_age, TTs)

##############################################################################
##############################################################################
####################################Tri-He####################################
##############################################################################
##############################################################################

Pre.Pre(par)

TTs = np.arange(2.5, 100, 2.5)

result = Calculate.TriHe(par, Cin, rain, TTs)

Post.Post.triHe1(result.result_tt, rain, date, show_gw_age, TTs)
