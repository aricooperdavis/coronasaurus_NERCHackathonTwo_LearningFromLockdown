import bokeh.plotting as bkh
import bokeh.models as bkm
import pandas as pd
import datetime

class Emissions():
    
    def __init__(self, country_co2='UK_CO2Emissions.csv'):
        df = pd.read_csv('UK_CO2Emissions.csv', usecols=[2,4])
        df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y')
        df['United Kingdom'] = df['United Kingdom'].str.rstrip('%').astype('float')/100
        self.country_co2 = df
        
        self.global_co2 = pd.read_csv('GlobalDailyCO2.csv',skiprows=4)
        
    def plot_uk_daily(self, figsize=(600,300), color='firebrick'):
        p = bkh.figure(x_axis_type='datetime', plot_width=figsize[0], plot_height=figsize[1])
        
        p.line(x=self.country_co2['DATE'],
               y=self.country_co2['United Kingdom'], color=color, legend_label='UK')
        
        p.yaxis.axis_label = 'CO₂ Emissions [MtCO₂ per day]'
        p.xaxis.axis_label = 'Date'
        
        p.xaxis[0].formatter = bkm.DatetimeTickFormatter(days=['%d/%m'])

        bkh.show(p)
        
    def plot_global_daily(self, figsize=(600,300), colors=['royalblue', 'firebrick']):
        p = bkh.figure(plot_width=figsize[0], plot_height=figsize[1])
        
        p.line(x=self.global_co2['year'],
               y=self.global_co2['value'], color=colors[0], legend_label='Global')
        
        p.varea(x=self.global_co2['year'],
                y1=self.global_co2['low uncertainty'],
                y2=self.global_co2['high uncertainty'],
                alpha=0.2, legend_label='Confidence', color=colors[1])
        
        p.yaxis.axis_label = 'CO₂ Emissions [MtCO₂ per day]'
        p.xaxis.axis_label = 'Year'
        p.legend.location = 'bottom_right'

        bkh.show(p)