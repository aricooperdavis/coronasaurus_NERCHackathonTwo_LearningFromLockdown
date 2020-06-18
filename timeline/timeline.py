# Some essential libraries
import numpy as np
import pandas as pd
import datetime

# For Bokeh
from collections import OrderedDict

from bokeh.plotting import *
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool
from bokeh.transform import factor_cmap, factor_mark

class TimelineData:
    def __init__(self, timeline_file):
        self.timeline = pd.read_csv(timeline_file).fillna('')
        self.timeline.Date = pd.to_datetime(self.timeline.Date, format='%d-%b-%y').dt.date
        
    def plot_timeline(self, colors= ['darkgrey', 'tomato', 'darkgrey'], transport = [False, True, False]):
        
        output_notebook()
        
        source = ColumnDataSource(
            data=dict(
                date=self.timeline.Date,
                date_tooltip = [x.strftime("%d-%m-%Y") for x in self.timeline.Date],
                y=np.zeros(len(self.timeline)),
                headline=self.timeline.Headline,
                colors=self.timeline.Transport.apply(lambda c: colors[c]),
                transport=self.timeline.Transport.apply(lambda c: transport[c])
            )
        )
        
        TOOLS='pan,wheel_zoom,box_zoom,reset'
        p = figure(title='Timeline', tools=TOOLS, width=1100,height=300)
        
        p.add_tools(HoverTool(
            tooltips=[
                ( 'Date',      '@date_tooltip'),
                ( 'Headline',  '@headline'    ),
                ( 'Transport Analysis',    '@transport'),
            ],
            
            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        ))
        
        p.circle('date', 'y', size=10, source=source, color='colors')
        
        p.xaxis.formatter=DatetimeTickFormatter(
                hours=["%d %B %Y"],
                days=["%d %B %Y"],
                months=["%d %B %Y"],
                years=["%d %B %Y"],
            )
        
        p.yaxis.visible = False
        
        show(p)
