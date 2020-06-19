import pandas as pd
from bokeh.plotting import figure, output_notebook, show

class EmissionsData:
    def __init__(self, input_file):
        # Load emissions data
        self.emissions = pd.read_csv(input_file)
        
    def plot(self, figsize=[750,400]):

        # output for slides
        output_notebook()

        p = figure(title="UK CO₂e Emissions & Targets", x_axis_label='Year', y_axis_label='Emissions MTCO₂e/Year', plot_width=figsize[0], plot_height=figsize[1])
        p.line(self.emissions['Year'], self.emissions['Historical emissions, excl forestry'], legend_label='Historical emissions, excl forestry', line_width=2, line_color='crimson')
        p.line(self.emissions['Year'], self.emissions['Current policy projections'], legend_label='Current policy projections', line_width=2, line_color='darkorchid')
        p.circle(self.emissions['Year'], self.emissions['2020 Pledge'], legend_label='2020 pledge', size=8, fill_color='white', line_color='darkcyan')
        p.circle(self.emissions['Year'], self.emissions['2030 Pledge'], legend_label='2030 pledge', size=8, fill_color='white', line_color='forestgreen')
        p.circle(self.emissions['Year'], self.emissions['2050 Pledge'], legend_label='2050 pledge', size=8, fill_color='white', line_color='lime')
        
        show(p)
