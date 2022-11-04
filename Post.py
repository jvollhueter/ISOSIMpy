# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:11:44 2022

@author: Vollhüter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Post():
    """Post processing."""

    def tracer(result, rain, sample):
        """Visualize the result of the tracer calculations."""
        sample_vis = sample.drop(sample[sample[3] == 0].index)

        fig = plt.figure(figsize=(8, 5), constrained_layout=True)
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        ax1.plot(rain['Date'], rain[3], color='green')
        ax1.plot(sample_vis['Date'], sample_vis[1], visible=False)
        ax2.plot(rain['Date'], result, color='red')
        ax2.plot(sample_vis['Date'], sample_vis[1], 'x')
        ax1.set(title='Tracer Source',
                ylabel='$c$ [TU]',
                xlabel='t',
                ylim=0)
        ax2.set(title='Tracer Sink',
                ylabel='$c$ [TU]',
                xlabel='t',
                ylim=0)
        ax1.grid()
        ax2.grid()

    def tracerTracer(result_tt, rain, rain_2, date, show_gw_age, TTs):
        """Visualize the result of the tracer tracer calculations."""
        result_tt = np.transpose(result_tt, axes=[2, 1, 0])

        fig = plt.figure(figsize=(10, 20), constrained_layout=True)
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax1.plot(rain['Date'], rain[3], label='Input Tracer 1')
        ax1.plot(rain_2['Date'], rain_2[3], label='Input Tracer 2')
        ax2.plot(result_tt[date, :, 0], result_tt[date, :, 1])
        ax2.scatter(result_tt[date, :, 0], result_tt[date, :, 1])
        ax1.set(title='Tracer input',
                ylabel='$c_{Tracers}$ [TU]',
                xlabel='t',
                ylim=0)

        ax2.set(title='Tracer output',
                xlabel='$c_{Tracer\ 1}$ [TU]',
                ylabel='$c_{Tracer\ 2}$ [TU]',
                xlim=0,
                ylim=0)
        k = 0
        j = 0

        # tau parameterizes the isolines in the diagram
        #     corresponding to certain percentages of
        #     tracer removal, i.e., the lines represent
        #     water in which the tracers have been
        #     reduced by a certain percentage relative
        #     to young / recharging / precipitation water
        tau = np.zeros((2, 4, len(show_gw_age)))
        for i in TTs:
            # if the currently handeled mean TT corresponds to
            #     a gw-age that should be handled, a line is
            #     drawn from the origin to the corresponding
            #     point in the diagram
            if i in show_gw_age:
                # plot a text-box labelling the gw-age
                plt.text(result_tt[date, k, 0]*1.02,
                         result_tt[date, k, 1],
                         str(i), backgroundcolor='black',
                         color='white')
                # plot the line from the origin to the
                #     corresponding point in the diagram
                ax2.plot([0, result_tt[date, k, 0]],
                         [0, result_tt[date, k, 1]],
                         color='black')
                for n in range(1, 5):
                    tau[:, n-1, j] = (n*0.25*result_tt[date, k, 0],
                                      n*0.25*result_tt[date, k, 1])
                j += 1
            k += 1

        for n in range(tau.shape[1]-1):
            ax2.plot(tau[0, n, :], tau[1, n, :], label=str(75 - n * 25))

        ax1.grid()
        ax2.grid()
        ax1.legend()
        ax2.legend(title='Tritium free water [%]:')

    def triHe1(result_tt, rain, date, show_gw_age, TTs):
        """Visualize the result of the tritium helium calculations."""
        fig = plt.figure(figsize=(10, 20), constrained_layout=True)
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)

        ax1.plot(rain['Date'], rain[3])

        ax2.plot(TTs,
                 result_tt[0, :, date] / result_tt[1, :, date])
        ax2.scatter(TTs,
                    result_tt[0, :, date] / result_tt[1, :, date])

        ax1.set(title='Input concentration',
                ylabel='$c_{Trithium}$ [TU]',
                xlabel='t',
                ylim=0)
        ax2.set(title='Output concentration on ' + str(rain['Date'][date]),
                xlabel='$T$ [a]',
                ylabel='$c_{3H/(3H+4He)}$',
                xlim=0,
                ylim=0)

        ax1.grid()
        ax2.grid()
