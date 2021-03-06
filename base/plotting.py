#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List of all desired plottings for GP code

Author: Federica Rescigno
Version: 25-01-2022
"""
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.interpolate
import auxiliary as aux


def data_plot(time, y, xlabel="time, BJD", ylabel="RVs", err_y=None, seasonbreaks=None, smooth_model_x=None, smooth_model_y=None, model_y=None, residuals=False):
    """
    Basic plot for the data. Errors are plotted when given. Can be split in seasons by entering the end time of each season 9no need to enter the last one).

    Parameters
    ----------
    time : array, floats
        X-axis array, usually time
    y : array, floats
        Y-axis array, usually rvs
    xlabel : string, optional
        Label of x axis. In case of initial subtraction can add "-#" to indicate the initial value. The default "time, BJD"
    ylabel : string, optional
        Label of y axis. The default "timeRVs"
    err_y : array, floats, optional
        Array of y errors, by default None
    seasonbreaks : list of floats, optional
        End times of each season, if you want to plot it. By default None
    smooth_model_x : array, floats, optional
        X-axis array for the smoothed model, by default None
    smooth_model_y : array, floats, optional
        Y values of the model, if you want to plot it. By default None (not plotting it)
    model_y : array, floats, optional
        Y values of the model. Not for plotting (not smooth). By default None (not plotting it)
    residuals : bool, optional
        If True, plot residuals. The default is False. Will require model_y to be given.
    """
    
    if residuals and model_y is None:
        raise ValueError("You need to give model_y to plot residuals")
    
    if (smooth_model_x is not None and smooth_model_y is None) or (smooth_model_x is None and smooth_model_y is not None):
        raise ValueError("You need to give both x and y to plot a model")
    
    if not residuals:
        plt.figure(figsize=(15,7))
        plt.ylabel(ylabel)
    if residuals:
        fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True)
        fig.subplots_adjust(hspace=0)
        axs[0].set_ylabel(ylabel)
        
    
    
    if not seasonbreaks:
        if residuals:
            axs[0].scatter(time, y, marker='.', color='purple')
            if err_y is not None:
                axs[0].errorbar(time, y, yerr=err_y, fmt='none', color='purple')
        else:
            plt.scatter(time, y, marker='.', color='purple')
            if err_y is not None:
                plt.errorbar(time, y, yerr=err_y, fmt='none', color='purple')
    
    if seasonbreaks:
        z = np.zeros_like(y)
        for i in reversed(seasonbreaks):
            for t in range(len(time)):
                if time[t] <= i:
                    z[t] += 1
        cmap = cm.tab10
        norm=Normalize(vmin=z.min(), vmax=z.max())
        if residuals:
            axs[0].scatter(time, y, marker='.', c=cmap(norm(z)))
            if err_y is not None:
                axs[0].errorbar(time, y, yerr=err_y, fmt='none', ecolor=cmap(norm(z)))
        else:
            plt.scatter(time, y, marker='.', c=cmap(norm(z)))
            if err_y is not None:
                plt.errorbar(time, y, yerr=err_y, fmt='none', ecolor=cmap(norm(z)))
        
    
    if model_y is not None:
        if residuals:
            if smooth_model_x is not None:
                axs[0].plot(smooth_model_x, smooth_model_y, color='sandybrown', label='Model')
                axs[0].legend()
            
            res = y-model_y
        
            if seasonbreaks:
                axs[1].scatter(time, res, marker='.', c=cmap(norm(z)))
            else:
                axs[1].scatter(time, res, marker='.', c="blue")
            axs[1].set_ylabel('Residuals')
            
    if smooth_model_x is not None:
        plt.plot(smooth_model_x, smooth_model_y, color='sandybrown', label='Model')
        plt.legend()

        
    
    
    plt.xlabel(xlabel)
    plt.show()

#data_plot(x,y, model_y=model_y, residuals=True)




import scipy.interpolate as interp

def GP_plot(time_obs, y_obs, y_err, model_y, pred_time, pred_y, pred_err, residuals=False, xlabel='Time [BJD]', ylabel='RV [m s-1]'):
    """
    Plots the oberved rv - model, as well as the prediction of the GP model. Can plot residuals.

    Parameters
    ----------
    time_obs : array, floats
        X-axis array, time of the observations
    y_obs : _type_
        _description_
    y_err : _type_
        _description_
    model_y : _type_
        _description_
    pred_time : _type_
        _description_
    pred_y : _type_
        _description_
    pred_err : _type_
        _description_
    residuals : bool, optional
        _description_, by default False
    xlabel : str, optional
        _description_, by default 'Time [BJD]'
    ylabel : str, optional
        _description_, by default 'RV [m s-1]'
    """
    
    "Residuals (Data-Model) vs GP"
    if not residuals:
        plt.figure(figsize=(15,15))
        plt.scatter(time_obs, y_obs-model_y, color='purple', label='Data - Model')
        plt.plot(pred_time, pred_y, color='orange', label='Predicted GP')
        plt.fill_between(pred_time, pred_y+pred_err, pred_y-pred_err, alpha=0.5, color='orange')
        plt.legend()
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()
        
    if residuals:
        fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True, figsize=(15,7), gridspec_kw={'height_ratios': [3,1]})
        fig.subplots_adjust(hspace=0)
        
        axs[0].scatter(time_obs, y_obs-model_y, color='purple', label='Data - Model')
        axs[0].plot(pred_time, pred_y, label='Predicted GP', color='orange')
        axs[0].fill_between(pred_time, pred_y+pred_err, pred_y-pred_err, alpha=0.5, color='orange')
        axs[0].set_ylabel(ylabel)
        axs[0].legend()
        
        f = interp.interp1d(pred_time, pred_y, kind='cubic')
        new_pred_y = f(time_obs)
        res = ((y_obs-model_y)-new_pred_y)#/rv_err[0]
        
        axs[1].scatter(time_obs, res, c='purple')
        axs[1].set_ylabel("Residuals")
        axs[1].set_xlabel(xlabel)
        plt.show()






def mixing_plot(iterations, numb_chains, hparam_chain, kernel_name, model_param_chain, model_name, LogL_chain):
    '''
    Parameters
    ----------
    iterations : integer
        Number of iterations in MCMC
    numb_chains : integer
        Number of chains
    hparam_chain : array
        Array of all the sets of hyperparameters of the MCMC, now in chains
    kernel_name : string
        Name of the kernel
    model_param_chain : array
        Array of all the sets of model parameters of the MCMC, now in chains
    model_name : string
        Name of the model
    LogL_chain : array
        Array containing all the Log Likelihood
    '''
    
    
    hparam_names = aux.hparam_names(kernel_name)
    model_param_names = aux.model_param_names(model_name, SkCk=True)
    
    xs = list(range(iterations+1))
    n_subplots = len(hparam_chain[0])+len(model_param_chain[0])+1
    
    fig, axs = plt.subplots(n_subplots, sharex=True, figsize=(15,15))
    fig.subplots_adjust(hspace=0.)
    axs[0].set_title("Mixing Chains")
    plt.xlabel("Number of iterations")
    
    for chain in range(numb_chains):
        for i in range(n_subplots):
            if i == 0:
                axs[i].plot(xs, LogL_chain[chain][:], c='xkcd:bluish', alpha=0.2)
                axs[i].set_ylabel("logL")
            if i != 0 and i <= len(hparam_chain[0]):
                axs[i].plot(xs, hparam_chain[chain][i-1][:], c='xkcd:bluish', alpha=0.2)
                axs[i].set_ylabel("{}".format(hparam_names[i-1]))
            if i != 0 and i > len(hparam_chain[0]):
                #print(model_param_chain[chain][i-1-len(hparam_chain[0])][:])
                axs[i].plot(xs, model_param_chain[chain][i-1-len(hparam_chain[0])][:], c='xkcd:bluish', alpha=0.2)
                axs[i].set_ylabel("{}".format(model_param_names[i-1-len(hparam_chain[0])]))
    plt.show()
    


def corner_plot(hparam_chain, kernel_name, model_param_chain, model_name):
    '''
    Parameters
    ----------
    hparam_chain : array
        Array of all the sets of hyperparameters of the MCMC
    kernel_name : string
        Name of the kernel
    model_param_chain : array
        Array of all the sets of model parameters of the MCMC.
    model_name : string
        Name of the model
    '''
    
    
    import corner
    
    
    hparam_names = aux.hparam_names(kernel_name)
    model_param_names = aux.model_param_names(model_name, SkCk=True)
    
    
    # Resizing of arrays: create 2d array, nrows=iteration*chians, ncols = nparam
    hp = np.array(hparam_chain)
    shapes = hp.shape
    #print("shape",shapes)
    numb_chains = shapes[0]
    nparam = shapes[1]
    depth = shapes[2]
    
    
    hparams = np.zeros((((depth)*numb_chains),nparam))
    for p in range(nparam):
        numb=0
        for c in range(numb_chains):
            for i in range(depth):
                hparams[numb][p] = hparam_chain[c][p][i]
                numb += 1
    
    
    par = np.array(model_param_chain)
    shapes2 = par.shape
    #print("shape",shapes)
    numb_chains2 = shapes2[0]
    nparam2 = shapes2[1]
    depth2 = shapes2[2]
    
    modpar = np.zeros((((depth2)*numb_chains2),nparam2))
    for p in range(nparam2):
        numb=0
        for c in range(numb_chains2):
            for i in range(depth2):
                modpar[numb][p] = model_param_chain[c][p][i]
                numb += 1
    
    
    
    # Corner plot of the hyperparameters
    fig = corner.corner(hparams, labels = hparam_names, show_titles=True)
    plt.show()
    
    
    try:
        # Corner plot of model parameters
        fig = corner.corner(modpar, labels=model_param_names, show_titles=True)
        plt.show()
    except ValueError:
        print("Inside: No dynamic range in model")
    
    # Full corner plot
    try:
        full_param_chain = np.concatenate((hparams, modpar), axis=1)
        full_names = hparam_names + model_param_names
        fig = corner.corner(full_param_chain, labels=full_names, show_titles=True)
        plt.show()
        
        final_param_values = []
        
        for a in range(len(hparam_chain[0])):
            quantile = corner.quantile(hparams[:,a], 0.5)
            final_param_values.append(quantile)
        for b in range(len(model_param_chain[0])):
            quantile = corner.quantile(modpar[:,b], 0.5)
            final_param_values.append(quantile)
    except ValueError:
        plt.show()
        print("Inside: No dynamic range in model")
        
        final_param_values = []
        
        for a in range(len(hparam_chain[0])):
            quantile = corner.quantile(hparam_chain[:,a], 0.5)
            final_param_values.append(quantile)
    
    print("Parameter values after MCMC: ", final_param_values)
    
    return final_param_values





def Keplerian_only_plot(time_obs, y_obs, y_err, pred_time, pred_y, model_y=None, smooth_model_x=None, smooth_model_y=None, residuals=False, xlabel='Time [BJD]', ylabel='RV [m s-1]'):
    """
    Plot of the stellar activity subtracted RVs, to compare with the model.

    Parameters
    ----------
    time_obs : array, floats
        X-axis of the observed data.
    y_obs : array, floats
        Y-axis of the observed data.
    y_err : array, floats
        Error of the observed data.
    pred_time : array, floats
        X-axis of the GP prediction data.
    pred_y : array, floats
        Y-axis of the GP prediction data.
    model_y : array, floats, optional
        Y-axis values of the model (it has the same amount of datapoints as the y_obs). It is used to compute the residuals. By default None
    smooth_model_x : array, floats, optional
        X-axis values of the smooth model. For plotting purposes. By default None
    smooth_model_y : array, floats, optional
        Y-axis values of the smooth model. For plotting purposes. By default None
    residuals : bool, optional
        Computing and plotting residuals? By default False
    xlabel : str, optional
        X label, by default 'Time [BJD]'
    ylabel : str, optional
        Y label, by default 'RV [m s-1]'

    Raises
    ------
    ValueError
        In case the residuals are requested but no proper model is given
    ValueError
        In case the plotting model misses one axis
    """
    
    if residuals and model_y is None:
        raise ValueError("You need to give model_y to plot residuals")
    
    if (smooth_model_x is not None and smooth_model_y is None) or (smooth_model_x is None and smooth_model_y is not None):
        raise ValueError("You need to give both x and y to plot a model")
    
    
    # Plot observations after subtracting the stellar activity alongside the model Keplerian
    f = interp.interp1d(pred_time, pred_y, kind='cubic')
    new_pred_y = f(time_obs)
    planet_only_rv = (y_obs-new_pred_y)
    
    if not residuals:
        plt.figure(figsize=(15,15))
        plt.scatter(time_obs, planet_only_rv, c='purple', label='Keplerian only RV', marker='.')
        plt.errorbar(time_obs, planet_only_rv, yerr=y_err, fmt='none', color='purple')
        if smooth_model_y is not None:
            plt.plot(smooth_model_x, smooth_model_y, color='sandybrown', label='Model')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()
        
        
    if residuals:
        fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True, figsize=(15,7), gridspec_kw={'height_ratios': [3,1]})
        fig.subplots_adjust(hspace=0)
        axs[0].scatter(time_obs, planet_only_rv, c='purple', label='Keplerian only RV', marker='.', zorder=2)
        axs[0].errorbar(time_obs, planet_only_rv, yerr=y_err, fmt='none', color='purple')
        if smooth_model_y is not None:
            axs[0].plot(smooth_model_x, smooth_model_y, color='sandybrown', label='Model')
        axs[0].set_ylabel(ylabel)
        axs[0].legend()
        
        res = planet_only_rv - model_y
        axs[1].scatter(time_obs, res, c='purple', label='Residuals', marker='.')
        axs[1].set_ylabel("Residuals")
        axs[1].set_xlabel(xlabel)
        plt.show()







def phase_plot(phase, y, yerr, model_y=None, smooth_model_phase=None, smooth_model_y=None, residuals=False, xlabel='Time [BJD]', ylabel='RV [m s-1]'):
    """
    Plot of phase folded data. Will require the phase folding done separately.
    
    Parameters
    ----------
    phase : array, floats
        X-axis of the phase folded data.
    y : array, floats
        Y-axis of the data. Must be only the model (only keplerian)
    yerr : array, floats
        Error of the data.
    model_y : array, floats, optional
        Y-axis of the model, must have the same length as the y, by default None
    smooth_model_phase : array, floats, optional
        X-axis of the smooth_model, by default None
    smooth_model_y : array, floats, optional
        Y-axis of the smooth_model, by default None
    residuals : bool, optional
        Plotting residuals? Requires model_y to be given, by default False
    xlabel : str, optional
        Xlabel, by default 'Time [BJD]'
    ylabel : str, optional
        Ylabel, by default 'RV [m s-1]'

    Raises
    ------
    ValueError
        In case the residuals are requested but no proper model is given
    ValueError
        In case the plotting model misses one axis
    """
    
    if residuals and model_y is None:
        raise ValueError("You need to give model_y to plot residuals")
    
    if (smooth_model_phase is not None and smooth_model_y is None) or (smooth_model_phase is None and smooth_model_y is not None):
        raise ValueError("You need to give both x and y to plot a model")
    
    
    # Start with getting the arrays in the proper order
    order = np.argsort(phase)
    # Observation data
    phase = phase[order]
    y = y[order]
    # Model for residuals
    if model_y is not None:
        model_y = model_y[order]
    # Smooth model
    if smooth_model_phase is not None:
        smooth_order = np.argsort(smooth_model_phase)
        smooth_model_phase = smooth_model_phase[smooth_order]
        smooth_model_y = smooth_model_y[smooth_order]
    
    if not residuals:
        plt.figure(figsize=(15,15))
        plt.scatter(phase, y, c='purple', label='Observations', marker='.')
        plt.errorbar(phase, y, yerr=yerr, fmt='none', color='purple')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if smooth_model_y is not None:
            plt.plot(smooth_model_phase, smooth_model_y, color='sandybrown', label='Model')
            plt.legend()
        
    if residuals:
        fig, axs = plt.subplots(ncols=1, nrows=2, sharex=True, figsize=(15,7), gridspec_kw={'height_ratios': [3,1]})
        fig.subplots_adjust(hspace=0)
        axs[0].scatter(phase, y, c='purple', label='Observations', marker='.')
        axs[0].errorbar(phase, y, yerr=yerr, fmt='none', color='purple')
        axs[0].set_ylabel(ylabel)
        if smooth_model_y is not None:
            axs[0].plot(smooth_model_phase, smooth_model_y, color='sandybrown', label='Model')
            axs[0].legend()
        
        res = y - model_y
        axs[1].scatter(phase, res, c='purple', label='Residuals', marker='.')
        axs[1].set_ylabel("Residuals")
        axs[1].set_xlabel(xlabel)
    
    plt.show()
        
    
    
    





####  OTHER STUFF TO IMPLEMENT #################################################################
# Save plots in functions, with sized, resolutions and aces text sized
# When multiple planets make it possible to have multiple phase folded plots
# Add extra long term trend??
    











