import pickle

import numpy as np
import pandas as pd
import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import GPy

class GridData:
    def __init__(self, grid_file):
        self.grid = pd.read_csv(grid_file)
        self.grid['DATE'] = pd.to_datetime(self.grid['SETTLEMENT_DATE'], format='%d-%b-%Y')
        
        self.grid_average = self.grid.groupby('DATE').agg(DEMAND_AVERAGE=pd.NamedAgg('ND',aggfunc=np.mean)).reset_index()
        self.grid_average['YEAR'] = self.grid_average['DATE'].dt.year
        self.grid_average['DOY'] = self.grid_average['DATE'].dt.dayofyear
        
        # Prepare the modelling data
        OFFSET = 0
        X = []
        for year in np.unique(self.grid_average.YEAR.values):
            DOY = OFFSET + self.grid_average.DOY[self.grid_average.YEAR.values==year]
            X += [i for i in DOY]
            OFFSET += max(self.grid_average.DOY[self.grid_average.YEAR.values==year])

        # Get X in years from the beginning, instead of days and transpose.
        self.X = np.expand_dims(np.array(X)/365, axis=1)
        
        # Get Y in GW instead of MW and transpose.
        self.Y = np.expand_dims(self.grid_average.DEMAND_AVERAGE.values/1000, axis=1)
        
    def get_data(self):
        return self.grid
        
    def get_data_average(self):
        return self.grid_average
        
    def plot_demand(self, collapse=True, figsize=(16,8), color='k'):
        
        plt.figure(figsize=figsize)
        
        if collapse:
            for year in np.unique(self.grid_average.YEAR.values):
                plt.plot(self.grid_average.DOY[self.grid_average.YEAR.values==year], 
                         self.grid_average.DEMAND_AVERAGE[self.grid_average.YEAR.values==year], linewidth=2, alpha=0.9, label=str(year))
            plt.xlabel('Day of the Year'), plt.ylabel('Demand (MW)')
            plt.legend()
        
        else:
            plt.plot(self.grid_average.DATE, self.grid_average.DEMAND_AVERAGE, c=color)
            plt.xlabel('Year'), plt.ylabel('Demand (MW)')
        
        plt.tight_layout()
        plt.show()
        
    def load_model(self, model_file, forecast_limit=7):
        
        # Set the datapoint cutoff index for lockdown.
        self.COVID_CUTOFF = 1881
        
        # Set the forecasting limit.
        self.forecast_limit = forecast_limit
        
        # Open a pickled model.
        with open(model_file, 'rb') as f:
            self.model = pickle.load(f)
        
        # Predict the model from 0 to the forecasting limit
        self.X_PREDICT = np.expand_dims(np.linspace(0, self.forecast_limit, 1000), axis=1)
        self.Y_PREDICT_mean, self.Y_PREDICT_conf = self.model.predict(self.X_PREDICT)
        
        # Get the datapoints after the lockdown.
        self.X_COVID = self.X[self.COVID_CUTOFF:]
        self.Y_COVID = self.Y[self.COVID_CUTOFF:]
        
        # Predict the datapoints after the lockdown.
        self.Y_COVID_PREDICT_mean, self.Y_COVID_PREDICT_conf = self.model.predict(self.X_COVID)
    
    def plot_model(self, figsize=(16,8)):
        
        plt.figure(figsize=figsize)
        
        plt.fill_between(self.X_PREDICT.flatten(), 
                        (self.Y_PREDICT_mean-self.Y_PREDICT_conf).flatten(), 
                        (self.Y_PREDICT_mean+self.Y_PREDICT_conf).flatten(), alpha=0.2, label='Confidence')
        
        plt.plot(self.X_PREDICT, self.Y_PREDICT_mean, label='Mean')
        
        plt.scatter(self.X[:self.COVID_CUTOFF], self.Y[:self.COVID_CUTOFF], c='k', marker='x', alpha=0.5, label='Before Lockdown')
        
        plt.scatter(self.X[self.COVID_CUTOFF:], self.Y[self.COVID_CUTOFF:], c='red', marker='x', alpha=0.5, label='After Lockdown')
        
        plt.xlabel('Year'); plt.ylabel('Net Demand (GW)')
        plt.xticks(np.arange(self.forecast_limit+1), np.arange(self.forecast_limit+1)+2015)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
    def plot_demand_discrepancy(self, figsize=(16,8), plot_confidence=True):
        
        locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax = plt.subplots(figsize=figsize)

        if plot_confidence:
            conf_min = self.Y_COVID.flatten()/(self.Y_COVID_PREDICT_mean.flatten()+self.Y_COVID_PREDICT_conf.flatten())
            conf_max = self.Y_COVID.flatten()/(self.Y_COVID_PREDICT_mean.flatten()-self.Y_COVID_PREDICT_conf.flatten())
            plt.fill_between(self.grid_average.DATE[self.COVID_CUTOFF:], conf_min, conf_max, alpha=0.2, label='Confidence')
        
        ax.plot(self.grid_average.DATE[self.COVID_CUTOFF:], np.ones(len(self.grid_average.DATE[self.COVID_CUTOFF:])), c='k', linestyle='dotted')
        ax.plot(self.grid_average.DATE[self.COVID_CUTOFF:], self.Y_COVID.flatten()/self.Y_COVID_PREDICT_mean.flatten(), c='k', label='Mean')
        
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlabel('Date'); ax.set_ylabel('$\\frac{Net \\: Demand \\: (True)}{Net \\: Demand \\: (Expected)}$')
        plt.legend()
        plt.tight_layout()
        plt.show()
