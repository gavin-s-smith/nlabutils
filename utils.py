'''
Utilities for Time Series tutorials.

@author: Gavin Smith (gavin.smith@nottingham.ac.uk)
'''

import pandas as pd
import matplotlib.pylab as plt
import numpy as np

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
pandas2ri.activate()

from statsmodels.tsa.stattools import adfuller

def invboxcox(y,ld):
    if ld == 0:
        return(np.exp(y))
    else:
        return(np.exp(np.log(ld*y+1)/ld))


def auto_arima_plot(dataseries, predict_forward):
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    r('aa <- auto.arima') # create an alias for the auto.arima function since we can't call dot methods from r2py
    r.plot(r.forecast(r.aa(dataseries,seasonal=False),h=predict_forward))


def arima_forecast(model, predict_forward):
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    out = r.forecast(model,h=predict_forward)
    return out[ [i for i,x in enumerate(out.names) if x=='mean'][0] ]

def auto_arima_determine_params(dataseries):
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    r('aa <- auto.arima') # create an alias for the auto.arima function since we can't call dot methods from r2py
    out = r.aa(dataseries,seasonal=False)
    
    ar_p = out[6][0]
    ma_q = out[6][1]
    non_season_diff = out[6][5]

    
    return out, (ar_p, ma_q, non_season_diff)

def manual_arima( dataseries, ar_p, ma_q, non_season_diff ):
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    return r.Arima(dataseries,order=np.asarray([ar_p, ma_q, non_season_diff]))


def stl_forecast(dataseries, freq, predict_forward, s_window = 'periodic', t_window = None, robust = True):
    importr('stlplus') # only for convenience functions for extracting components (stlplus has no forecast ability at the moment)
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    extra_args = {}
    
    if t_window != None:
        extra_args['t_window'] = t_window
    
    out = r.forecast(r.stl(r.ts(dataseries,freq=freq), s_window=s_window, robust=robust, **extra_args), method = "arima", h = predict_forward)
    
    ar_p = out[1][6][0]
    ma_q = out[1][6][1]
    non_season_diff = out[1][6][5]
    
    print('ARMIA parameters used were: p {}, q {}, d {}'.format(ar_p, ma_q, non_season_diff))
    
    return out[ [i for i,x in enumerate(out.names) if x=='mean'][0] ]


def stl_plot_forecast(dataseries, freq, predict_forward, s_window = 'periodic', t_window = None, robust = True):
    importr('stlplus') # only for convenience functions for extracting components (stlplus has no forecast ability at the moment)
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    extra_args = {}
    
    if t_window != None:
        extra_args['t_window'] = t_window
    
    out = r.forecast(r.stl(r.ts(dataseries,freq=freq), s_window=s_window, robust=robust, **extra_args), method = "arima", h = predict_forward)
    
    r.plot(out)



def stl_components( dataseries, freq, s_window = 'periodic', t_window = None, robust = True ):
    importr('stlplus') # only for convenience functions for extracting components (stlplus has no forecast ability at the moment)
    importr('forecast') # provides stl and it's forecast method
    r = robjects.r
    extra_args = {}
    
    if t_window != None:
        extra_args['t_window'] = t_window
    
        
    fit = r.stl(r.ts(dataseries,freq=freq), s_window=s_window, robust=robust, **extra_args)

    seasonal = r.seasonal(fit)
    trend = r.trend(fit)
    remainder = r.remainder(fit)
    
    
    return pd.Series(seasonal,index=dataseries.index), pd.Series(trend,index=dataseries.index),pd.Series(remainder,index=dataseries.index)

def stl_plot_components( dataseries, freq, s_window = 'periodic', t_window = None, robust = True  ):
    seasonal, trend, remainder = stl_components( dataseries, freq, s_window = 'periodic', t_window = None, robust = True )
    # declare plot all four subplot, share the x-axis, returns figure (f) and
    # array of axis, one for each subplot.
    f, axarr = plt.subplots(5, sharex=True)
    
    
    # .plot per axis creates the plot in each subplot (axis)
    axarr[0].plot(np.asarray(dataseries), color='blue',label='Original')
    axarr[1].plot(np.asarray(seasonal), color='red', label='Seasonal')
    axarr[2].plot(np.asarray(trend), color='black', label = 'Trend')
    axarr[3].plot(np.asarray(remainder), color='black', label = 'Remainder')
    axarr[4].plot(np.asarray(dataseries)-np.asarray(seasonal), color='black', label = 'Non-seasonal')
    
    # .legend per axis creates the legend based on the label information
    axarr[0].legend(loc='best')
    axarr[1].legend(loc='best')
    axarr[2].legend(loc='best')
    axarr[3].legend(loc='best')
    axarr[4].legend(loc='best')



def plot_rolling( timeseries, overlay = True, window = 6 ):
    rolmean = timeseries.rolling(window=window,center=False).mean()
    rolstd = timeseries.rolling(window=window,center=False).std()
    
    if overlay:
        orig = plt.plot(timeseries, color='blue',label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean & Standard Deviation')
    else:
        f, axarr = plt.subplots(3, sharex=True)
        axarr[0].plot(timeseries, color='blue',label='Original')
        axarr[1].plot(rolmean, color='red', label='Rolling Mean')
        axarr[2].plot(rolstd, color='black', label = 'Rolling Std')
        axarr[0].legend(loc='best')
        axarr[1].legend(loc='best')
        axarr[2].legend(loc='best')

