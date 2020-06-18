import pandas as pd
import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class CoronaData:
    def __init__(self, cases_file, deaths_file):
        self.cases = pd.read_csv(cases_file)
        self.cases['Date'] = pd.to_datetime(self.cases['Date'], format='%d-%b-%Y')
        
        self.deaths = pd.read_csv(deaths_file)
        self.deaths['Date'] = pd.to_datetime(self.deaths['Date'], format='%d-%b-%Y')
        
    def get_cases(self):
        return self.cases
        
    def get_deaths(self):
        return self.deaths
        
    def plot_cases(self, figsize=(12,6), colors=['k', 'darkturquoise']):
        
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax1 = plt.subplots(figsize=figsize)

        ax1.set_xlabel('Date'); ax1.xaxis.set_major_locator(locator); ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('New Cases', color=colors[0])
        ax1.bar(self.cases['Date'], self.cases['New_cases'], color=colors[0])
        ax1.tick_params(axis='y', labelcolor=colors[0])
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        ax2.xaxis.set_major_locator(locator); ax2.xaxis.set_major_formatter(formatter)
        ax2.set_ylabel('Total Cases', color=colors[1])  # we already handled the x-label with ax1
        ax2.plot(self.cases['Date'], self.cases['Total_cases'], color=colors[1], linewidth=2)
        ax2.tick_params(axis='y', labelcolor=colors[1])
        
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

    def plot_deaths(self, figsize=(12,6), colors=['k', 'darkturquoise']):
        
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        formatter = mdates.ConciseDateFormatter(locator)
        
        fig, ax1 = plt.subplots(figsize=figsize)

        ax1.set_xlabel('Date'); ax1.xaxis.set_major_locator(locator); ax1.xaxis.set_major_formatter(formatter)
        ax1.set_ylabel('New Deaths', color=colors[0])
        ax1.bar(self.deaths['Date'], self.deaths['New_deaths'], color=colors[0])
        ax1.tick_params(axis='y', labelcolor=colors[0])
        
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        ax2.xaxis.set_major_locator(locator); ax2.xaxis.set_major_formatter(formatter)
        ax2.set_ylabel('Total Deaths', color=colors[1])  # we already handled the x-label with ax1
        ax2.plot(self.deaths['Date'], self.deaths['Total_deaths'], color=colors[1], linewidth=2)
        ax2.tick_params(axis='y', labelcolor=colors[1])
        
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
