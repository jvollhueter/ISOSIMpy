# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 11:26:38 2022

@author: Vollhüter
"""

"""
Note (Max):
Some notes (mainly regarding automatic calibration):

- this structure generally does not work well with
    standard calibration / optimization algorithms
    such as scipy.optimize.least_squares
- we need to define:
    1. a function returning the residual series
        given parameter values and observations
    2. a function that actually performs the fitting
        based on the residual-function
"""

import numpy as np
import pandas as pd
from scipy.optimize import least_squares

class Multis():
    """Calculations of the flow and decay processes in unsaturated zone."""

    def __init__(self):

        print('Your calculations will start soon. Look forward to \
the results!')
        # Marker adding tests here

    def runMultis(Cin, par):
        """Calculate flow and decay processes in unsaturated zone."""

        """
        Note (Max):
        I really don't get why parameters are re-defined (e.g. eta = par.eta)
        in some places
        """
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

            # we always call this function f for all LPMs because
            #   then we can always call f without having to
            #   specify the LPM or parameters
            def tf(self, parameters=np.array([lambda_])):
                """
                The transfer function for the piston flow model.
                For given parameters etc., this function returns
                an array of floats, representing the discrete
                transfer function.

                PFM parameters:
                half life / decay time  --> 0

                :: Parameters ::
                parameters : a 1D-array of model parameters as
                    floats; np.array

                :: Returns ::
                f_arr : the discrete transfer function as an
                    array of floats; np.array
                """

                # prepare f
                tf = np.zeros((n), dtype=np.float32)
                if int(TT_round) <= n:
                    f[int(TT_round) - 1] = 1.

                # prepare full transfer function, including
                #   radioactive decay
                tf *= np.exp(-parameters[0] * t)

                return tf

            else:
                print('An error occured. TT > sim per')

        # Exponential Model
        elif par.lpm_type == '2' or par.lpm_type == 'exponential':
            print('Exponential Model')
            f = 1/TT * np.exp(-t/TT)

            def tf(self, parameters=np.array([lambda_, TT])):
                """
                The transfer function for the exponential model.
                For given parameters etc., this function returns
                an array of floats, representing the discrete
                transfer function.

                EM parameters:
                half life / decay time  --> 0
                mean travel time        --> 1

                :: Parameters ::
                parameters : a 1D-array of model parameters as
                    floats; np.array

                :: Returns ::
                f_arr : the discrete transfer function as an
                    array of floats; np.array
                """

                # prepare f
                tf = 1 / parameters[1] * np.exp(-t / parameters[1])

                # prepare full transfer function, including
                #   radioactive decay
                tf *= np.exp(-parameters[0] * t)

                return tf

        # Dispersion Model
        elif par.lpm_type == '3' or par.lpm_type == 'dispersion':
            print('Dispersion Model')
            PD = par.PD
            f = (4 * np.pi * PD * t / TT)**(-0.5) * 1 / t *\
                np.exp(-(1 - t / TT)**2 / (4 * PD * t / TT))

            def tf(self, parameters=np.array([lambda_, TT, par.PD])):
                """
                The transfer function for the dispersion model.
                For given parameters etc., this function returns
                an array of floats, representing the discrete
                transfer function.

                DM parameters:
                half life / decay time  --> 0
                mean travel time        --> 1
                dispersion coeff.       --> 2

                :: Parameters ::
                parameters : a 1D-array of model parameters as
                    floats; np.array

                :: Returns ::
                f_arr : the discrete transfer function as an
                    array of floats; np.array
                """

                # prepare f
                tf = (4 * np.pi * parameters[2] * t / parameters[1])**(-0.5) * 1 / t *\
                    np.exp(-(1 - t / parameters[1])**2 / (4 * parameters[2] * t / parameters[1]))

                # prepare full transfer function, including
                #   radioactive decay
                tf *= np.exp(-parameters[0] * t)

                return tf

        # Linear Model
        elif par.lpm_type == '4' or par.lpm_type == 'linear':
            print('Linear Model')
            f = np.zeros((n))
            ind = np.where(t <= (2 * TT))
            f[ind[0][0]:ind[0][-1]+1] = 1/(2*TT)

            def tf(self, parameters=np.array([lambda_, TT])):
                """
                The transfer function for the linear model.
                For given parameters etc., this function returns
                an array of floats, representing the discrete
                transfer function.

                LM parameters:
                half life / decay time  --> 0
                mean travel time        --> 1

                :: Parameters ::
                parameters : a 1D-array of model parameters as
                    floats; np.array

                :: Returns ::
                f_arr : the discrete transfer function as an
                    array of floats; np.array
                """

                # prepare f
                tf = np.zeros((n), dtype=np.float32)
                ind = np.where(t <= (2 * parameters[1]))
                tf[ind[0][0]:ind[0][-1]+1] = 1 / (2 * parameters[1])

                # prepare full transfer function, including
                #   radioactive decay
                tf *= np.exp(-parameters[0] * t)

                return tf

        # Exponential Piston Flow
        elif par.lpm_type == '5' or par.lpm_type == 'exponential piston flow':
            print('Exponential Piston Flow Model')
            f = eta / TT * np.exp(- (eta * t) / TT + eta - 1)
            ind = np.where(t <= (eta-1)*TT/eta)
            if ind[0].size > 0:
                f[ind[0][0]:ind[0][-1]+1] = 0

            def tf(self, parameters=np.array([lambda_, TT, par.eta])):
                """
                The transfer function for the exponential piston
                flow model.
                For given parameters etc., this function returns
                an array of floats, representing the discrete
                transfer function.

                EPFM parameters:
                half life / decay time  --> 0
                mean travel time        --> 1
                exp. flow fraction      --> 2

                :: Parameters ::
                parameters : a 1D-array of model parameters as
                    floats; np.array

                :: Returns ::
                f_arr : the discrete transfer function as an
                    array of floats; np.array
                """

                # prepare f
                tf = parameters[2] / parameters[1] * np.exp(- (parameters[2] * t) / parameters[1] + parameters[2] - 1)
                    ind = np.where(t <= (parameters[2] - 1) * parameters[1] / parameters[2])
                if ind[0].size > 0:
                    tf[ind[0][0]:ind[0][-1]+1] = 0

                # prepare full transfer function, including
                #   radioactive decay
                tf *= np.exp(-parameters[0] * t)

                return tf

        else:
            raise KeyError("""Section lpm type in xml file has a not known value. Please check for typos and if necessary read the manual """)

        # define a function to compute the residuals given
        #   the transfer function
        def residuals(self, parameters, obs, interpolate=True):
            """
            Calculate the residuals for a given transfer function
            and parameters.

            :: Parameters ::
            parameters : a 1D array of floats representing the model
                parameters; np.array
            obs : a Series representing the tracer output measurements
                with a DateTime index that is equivalent to the
                tracer input Series, pd.Series
            interpolate : a bool specifying whether to linearly
                interpolate between simulated values to obtain
                simulated values at times of observation, default is
                True; bool

            :: Returns ::
            residuals : a 1D array representing the residuals between
                observed and simulated values, np.array
            """

            # calculate model output / simulated values
            temp = np.zeros((n, (n*2)))

            if parameters is None:
                tf_ = tf()
            else:
                tf_ = tf(parameters)

            for i in range(1, n+1):
                temp[i-1, i-1:n+i-1] = Cin[i-1] * tf_
            Cout = np.sum(temp, axis=0)

            # calculate residuals
            # TODO
            residuals = [0.]

            return residuals

        def calibrate(self, init_guess, bounds):
            """
            Calibrate the model parameters using a least-squares
            algorithm.

            :: Parameters ::
            init_guess : a 1D array representing the initial guess for the
                parameter values; np.array
            bounds : a 2-tuple of 1D arrays representing the parameter
                bounds for optimization; 2-tuple of 1D arrays

            :: Returns ::
            calibrated_parameters : a 1D array representing the calibrated
                parameters; np.array

            Note: init_guess should be given taking the corresponding LPM
            intoaccount (i.e., the number of parameters)
            """

            result = least_squares(residuals, init_guess, bounds)

            return result.x


        temp = np.zeros((n, (n*2)))
        for i in range(1, n+1):
            temp[i-1, i-1:n+i-1] = Cin[i-1] * np.exp(-lambda_ * t) * f
        global Cout
        Cout = np.sum(temp, axis=0)

        return Cout
