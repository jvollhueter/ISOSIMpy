# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:11:44 2022

@author: Jonas Vollhüter
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time


class Post():
    """Post processing."""

    def tracer(result, rain, sample, par):
        """Postprocess result of calcs in mode tracer"""
        if par.write_output == 'True':
            temp = pd.DataFrame(rain['Date'], columns=['Date'])
            temp['Result'] = result
            with open(
                    r'out/results_' + time.strftime("%Y%m%d_%H%M%S") + '.csv',
                    'a', newline='\n') as f:
                f.write('\n')
                f.write('New model run:\n')
                f.write('\n')
                f.write(';;Date:;Setup name:;LPM:;Mean GW Age:;Halftime:;PD:;eta:\n')
                f.write(';;' + str(datetime.now()))
                f.write(';' + str(par.name))
                f.write(';' + str(par.lpm_type))
                f.write(';' + str(par.mean_gw_age))
                f.write(';' + str(par.halftime_1))
                f.write(';' + str(par.PD))
                f.write(';' + str(par.eta) + '\n')
                f.write('\n')
                temp.to_csv(f, sep=';', index=False)
                f.write('\n')
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

        plt.show()
        if par.write_output == 'True':
            fig.savefig('out/fig/'+time.strftime("%Y%m%d_%H%M%S")+'.png')

    def tracerTracer(result_tt, data_frames, par):
        """Visualize the result of the tracer tracer calculations."""
        result_tt = np.transpose(result_tt, axes=[2, 1, 0])

        # MARKER integrate output here

        rain = data_frames.c_in_1
        rain_2 = data_frames.c_in_2
        fig = plt.figure(figsize=(10, 20), constrained_layout=True)
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax1.plot(rain['Date'], rain[3], label='Input Tracer 1')
        ax1.plot(rain_2['Date'], rain_2[3], label='Input Tracer 2')
        ax2.plot(result_tt[rain[rain['Date'] == par.date].index, :, 0],
                 result_tt[rain[rain['Date'] == par.date].index, :, 1])
        ax2.scatter(result_tt[rain[rain['Date'] == par.date].index, :, 0],
                    result_tt[rain[rain['Date'] == par.date].index, :, 1])
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
        tau = np.zeros((2, 4, len(par.vis_gw_age)))
        for i in par.TTs:
            if i in par.vis_gw_age:
                plt.text(result_tt[rain[rain['Date'] ==
                                        par.date].index, k, 0]*1.02,
                          result_tt[rain_2[rain_2['Date'] ==
                                            par.date].index, k, 1],
                          str(i), backgroundcolor='black',
                          color='white')
                ax2.plot([0,result_tt[rain[rain['Date'] ==
                                            par.date].index, k, 0]],
                          [0, result_tt[rain_2[rain_2['Date'] ==
                                                par.date].index, k, 1]],
                          color='black')
                for n in range(1, 5):
                    tau[:, n-1, j] = (n * 0.25 *
                                      result_tt[rain[rain['Date'] ==
                                                      par.date].index, k, 0],
                                      n * 0.25 *
                                      result_tt[rain_2[rain_2['Date'] ==
                                                        par.date].index, k, 1])
                j += 1
            k += 1
            ('out/fig/'+time.strftime("%Y%m%d_%H%M%S")+'.png')

        for n in range(tau.shape[1]-1):
            ax2.plot(tau[0, n, :], tau[1, n, :], label=str(75 - n * 25))

        ax1.grid()
        ax2.grid()
        ax1.legend()
        ax2.legend(title='Tritium free water [%]:')

        plt.show()
        if par.write_output == 'True':
            fig.savefig('out/fig/'+time.strftime("%Y%m%d_%H%M%S")+'.png')


    def triHe(result_tt, data_frames, par):
        """Visualize the result of the tritium helium calculations."""
        rain = data_frames.c_in_1

        # MARKER integrate output here

        fig = plt.figure(figsize=(10, 20), constrained_layout=True)
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)

        ax1.plot(rain['Date'], rain[3])

        ax2.plot(par.TTs,
                  result_tt[0, :, par.date] / result_tt[1, :, par.date])
        ax2.scatter(par.TTs,
                    result_tt[0, :, rain[rain['Date'] == par.date].index] /
                    result_tt[1, :, rain[rain['Date'] == par.date].index])

        ax1.set(title='Input concentration',
                ylabel='$c_{Trithium}$ [TU]',
                xlabel='t',
                ylim=0)
        ax2.set(title='Output concentration on ' +
                str(rain['Date'][rain[rain['Date'] == par.date].index]),
                xlabel='$T$ [a]',
                ylabel='$c_{3H/(3H+4He)}$',
                xlim=0,
                ylim=0)

        ax1.grid()
        ax2.grid()

        plt.show()
        if par.write_output == 'True':
            fig.savefig('out/fig/'+time.strftime("%Y%m%d_%H%M%S")+'.png')
