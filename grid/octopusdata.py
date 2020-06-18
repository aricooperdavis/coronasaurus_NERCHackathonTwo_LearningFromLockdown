import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime

import bokeh.plotting as bkh
import bokeh.models as bkm

class OctopusData:
    def __init__(self, data_file, weather_file=None):
        self.energy = pd.read_csv(data_file).rename(columns={'Unnamed: 0': 'Date'})
        self.energy['Date'] = pd.to_datetime(self.energy['Date'], format='%Y-%m-%d %H:%M:%S')
        self.energy['Date_'] = self.energy.Date.dt.date
        
        self.energy_average = self.energy.groupby('Date_').agg(electricity_daily_total = pd.NamedAgg('Electricity', 'sum'),
                                                               gas_daily_total = pd.NamedAgg('Gas (corrected)', 'sum')).reset_index()
        self.energy_average.drop(self.energy_average.tail(1).index, inplace=True)
        cols = ['electricity_daily_total','gas_daily_total']
        self.energy_average[cols] = self.energy_average[cols].replace({0.0: np.nan})
        
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
        
    def plot_timeline_bkh(self, figsize=(600,300)):
        p = bkh.figure(x_axis_type='datetime', plot_width=figsize[0], plot_height=figsize[1])
        
        p.line(x=self.energy['Date'],
               y=self.energy['Electricity'], color='royalblue', legend_label='Electricity')
        p.line(x=self.energy['Date'],
               y=self.energy['Gas (corrected)'], color='orange', legend_label='Gas (corrected)')
        
        p.yaxis.axis_label = 'kWh'
        p.xaxis.axis_label = 'Date'
        
        p.xaxis[0].formatter = bkm.DatetimeTickFormatter(days=['%d/%m'])

        bkh.output_notebook()
        bkh.show(p)

    def plot_daily_electricity(self, figsize=(24,8), plot_temperature=False, colors=['k', 'darkturquoise']):
        locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax1 = plt.subplots(figsize=figsize)

        electricity_mean = ax1.plot(self.energy_average['Date_'], 12*np.ones(len(self.energy_average)), c=colors[0], linestyle='dashed', linewidth=2)
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
            
            plt.text(0.05, 0.9, 'R = {0:.3f}'.format(self.energy_average[['electricity_daily_total', 'temperature']].corr(method='pearson').values[1,0]), 
                     ha='center', va='center', transform=ax2.transAxes)
            
            plt.legend([electricity[0], electricity_mean[0], temp[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)', 'Temperature'], loc=1)
        else:
            plt.legend([electricity[0], electricity_mean[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)'], loc=1)
            
        fig.tight_layout()
        plt.show()
        
    def plot_daily_electricity_bkh(self, figsize=(600,300), plot_temperature=False, colors=['black', 'darkturquoise']):
        p = bkh.figure(x_axis_type='datetime', plot_width=figsize[0], plot_height=figsize[1])

        p.line(x=self.energy_average['Date_'], y=12*np.ones(len(self.energy_average)), line_dash='dashed', line_color=colors[0], legend_label='Typical domestic use')
        
        p.line(x=self.energy_average['Date_'], y=self.energy_average['electricity_daily_total'], line_color=colors[0], legend_label='Mean of 115,000 UK households')
        
        p.xaxis.axis_label='Date'
        p.xaxis[0].formatter = bkm.DatetimeTickFormatter(days=['%d/%m'])
        
        p.yaxis.axis_label='Electricity Consumption (kWh)'
        p.yaxis.axis_label_text_color = colors[0]
        
        if plot_temperature and self.weather_file:
            p.extra_y_ranges = {'temperature': bkm.Range1d(start=6, end=24)}
            
            p.line(x=self.energy_average['Date_'],
                   y=self.energy_average['temperature'],
                   line_color=colors[1], legend_label='Temperature', y_range_name='temperature')
            
            p.add_layout(bkm.LinearAxis(y_range_name='temperature', axis_label='Mean Temperature (°C)',
                                        axis_label_text_color=colors[1], axis_line_color=colors[1],
                                        major_label_text_color=colors[1], major_tick_line_color=colors[1],
                                        minor_tick_line_color=colors[1]
                                       ), 'right')
            
            #plt.text(0.05, 0.9, 'R = {0:.3f}'.format(self.energy_average[['electricity_daily_total', 'temperature']].corr(method='pearson').values[1,0]), 
            #         ha='center', va='center', transform=ax2.transAxes)
            
        bkh.output_notebook()
        bkh.show(p)
        
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
            
            plt.text(0.05, 0.9, 'R = {0:.3f}'.format(self.energy_average[['gas_daily_total', 'temperature']].corr(method='pearson').values[1,0]), 
                     ha='center', va='center', transform=ax2.transAxes)
            
            plt.legend([gas[0], gas_mean[0], temp[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)', 'Temperature'], loc=1)
        else:
            plt.legend([gas[0], gas_mean[0]], ['Mean of 115 000 UK households', 'Typical domestic use (medium)'], loc=1)
            
        fig.tight_layout()
        plt.show()
