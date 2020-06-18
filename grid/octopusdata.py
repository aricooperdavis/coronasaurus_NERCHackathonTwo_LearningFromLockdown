import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime

class OctopusData:
    def __init__(self, data_file, weather_file=None):
        self.energy = pd.read_csv(data_file).rename(columns={'Unnamed: 0': 'Date'})
        self.energy['Date'] = pd.to_datetime(self.energy['Date'], format='%Y-%m-%d %H:%M:%S')
        self.energy['Date_'] = self.energy.Date.dt.date
        
        self.energy_average = self.energy.groupby('Date_').agg(electricity_daily_total = pd.NamedAgg('Electricity', np.sum),
                                                               gas_daily_total = pd.NamedAgg('Gas (corrected)', np.sum)).reset_index()
        self.energy_average.drop(self.energy_average.tail(1).index, inplace=True)
        
        if weather_file:
            weather = pd.read_csv(weather_file)
            weather.date = pd.to_datetime(weather['date'], format='%d/%m/%Y')
            self.energy_average = self.energy_average.join(weather)
            self.weather_file = True
        
    def get_data(self):
        return self.energy
        
    def get_data_average(self):
        return self.energy_average

    def plot_timeline(self, figsize=(24,8)):
        ax = self.energy.plot('Date', ['Electricity', 'Gas (corrected)'], figsize=figsize)
        ax.set_ylabel('kWh')
        plt.show()

    def plot_daily_electricity(self, figsize=(24,8), plot_temperature=False, colors=['k', 'darkturquoise']):
        locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax1 = plt.subplots(figsize=figsize)

        electricity_mean = ax1.plot(self.energy_average['Date_'], 10*np.ones(len(self.energy_average)), c=colors[0], linestyle='dashed', linewidth=2)
        electricity = ax1.plot(self.energy_average['Date_'], self.energy_average['electricity_daily_total'], c=colors[0], linewidth=2)
        
        ax1.tick_params(axis='y', labelcolor=colors[0])
        ax1.set_xlabel('Date'); ax1.xaxis.set_major_locator(locator); ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('Electricity Consumption $(kWh)$', color=colors[0])
        
        if plot_temperature and self.weather_file:
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            
            ax2.xaxis.set_major_locator(locator); ax2.xaxis.set_major_formatter(formatter)
            ax2.set_ylabel('Mean Temperature ($^\\circ$C)', color=colors[1])  # we already handled the x-label with ax1
            temp = ax2.plot(self.energy_average['Date_'], self.energy_average['temperature'], color=colors[1], linewidth=2)
            
            ax2.tick_params(axis='y', labelcolor=colors[1])
            
            plt.text(0.05, 0.9, 'R = {0:.3f}'.format(np.corrcoef(self.energy_average['electricity_daily_total'], self.energy_average['temperature'])[0,1]), 
                     ha='center', va='center', transform=ax2.transAxes)
            
            plt.legend([electricity[0], electricity_mean[0], temp[0]], ['Mean of 115 000 UK households', 'Typical domestic use (high)', 'Temperature'], loc=1)
        else:
            plt.legend([electricity[0], electricity_mean[0]], ['Mean of 115 000 UK households', 'Typical domestic use (high)'], loc=1)
            
        fig.tight_layout()
        plt.show()
        
    def plot_daily_gas(self, figsize=(24,8), plot_temperature=False, colors=['k', 'darkturquoise']):
        locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax1 = plt.subplots(figsize=figsize)

        gas_mean = ax1.plot(self.energy_average['Date_'], 32*np.ones(len(self.energy_average)), c=colors[0], linestyle='dashed', linewidth=2)
        gas = ax1.plot(self.energy_average['Date_'], self.energy_average['gas_daily_total'], c=colors[0], linewidth=2)
        
        ax1.tick_params(axis='y', labelcolor=colors[0])
        ax1.set_xlabel('Date'); ax1.xaxis.set_major_locator(locator); ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('Gas Consumption (Corrected) $(\\frac{kWh}{ALP})$', color=colors[0])
        
        if plot_temperature and self.weather_file:
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            
            ax2.xaxis.set_major_locator(locator); ax2.xaxis.set_major_formatter(formatter)
            ax2.set_ylabel('Mean Temperature ($^\\circ$C)', color=colors[1])  # we already handled the x-label with ax1
            temp = ax2.plot(self.energy_average['Date_'], self.energy_average['temperature'], color=colors[1], linewidth=2)
            
            ax2.tick_params(axis='y', labelcolor=colors[1])
            
            plt.text(0.05, 0.9, 'R = {0:.3f}'.format(np.corrcoef(self.energy_average['gas_daily_total'], self.energy_average['temperature'])[0,1]), 
                     ha='center', va='center', transform=ax2.transAxes)
            
            plt.legend([gas[0], gas_mean[0], temp[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)', 'Temperature'], loc=1)
        else:
            plt.legend([gas[0], gas_mean[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)'], loc=1)
            
        fig.tight_layout()
        plt.show()
