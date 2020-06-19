import bokeh.plotting as bkh
import bokeh.models as bkm
import pandas as pd

class Society():
    """
    Wrapper for James's society plots.
    """
    def __init__(self, wellness='./london_cv19_wellness.csv'):
        self.wellness = pd.read_csv(wellness)

    def employment_table(self, export=False):
        headings = ['UK Employment Status (ONS data)', 'Pre Lockdown (m) March 2020', 'Post Lockdown (m) Early April 2020']
        table = [
          ['Total Population', 67.9, 67.9],
          ['Total Possible Workforce', 41.4, 41.4],
          ['Employed', 31.6, 30.7],
          ['Unemployed', 1.3, 2.2],
          ['Furloughed (still employed)', 0, 9.1],
          ['Home Based worker (employed or not)', 2.8, 11.3],
          ['Students (at school/uni)', 14.7, 1.2],
          ['People at home', 33.8, 47.5],
          ['Work Based worker', 30.1, 19.2],
          ]
        employment = pd.DataFrame(columns=headings, data=table)

        if export:
            employment.to_csv('emplotment_clean.csv')

        return employment

    def plot_domestic_issues(self, figsize=(600, 300), plot_bounds=True, colors=['black', 'darkturquoise']):
        df = self.wellness

        df['Date'] = pd.to_datetime(df['Date'])
        df.index = df['Date']

        p = bkh.figure(x_axis_type='datetime', plot_width=figsize[0], plot_height=figsize[1])
        p.xaxis[0].formatter = bkm.DatetimeTickFormatter(days=['%d/%m'])
        p.xaxis.axis_label='Date'
        p.yaxis.axis_label='% of actions delivered above normal levels'

        df['avg'] = df.mean(axis=1)
        p.line(x=df.index.values, y=df['avg'].values, color=colors[0], legend_label="Mean action on domestic issues")

        if plot_bounds:
            df['min'] = df.min(axis=1)
            df['max'] = df.max(axis=1)
            p.varea(x=df.index.values,y1=df['min'].values,y2=df['max'].values,
                    alpha=0.2, color=colors[1], legend_label='Max/min bounds')

        bkh.show(p)
