#!/usr/bin/env python

import pandas as pd
import numpy as np
import seaborn as sns
import sys
import math
from pprint import pprint
import matplotlib.pyplot as plt

filename = sys.argv[1]

toggl = pd.read_csv(filename, parse_dates=[
                    "Start date", "End date", 'Start time', "End time"], index_col=['Start date'])
toggl = toggl.drop(["User", "Email", "Client", "Project",
                   "Task", "Billable", "Tags", "Amount ()"], axis=1)


def ts_to_num(ts):
    return ts.hour + ts.minute / 60


def update_hours(hours, r_start, r_end):
    start = ts_to_num(r_start)  # 15:38
    end = ts_to_num(r_end)

    left = end - start
    left, left*60  # , minutes

    # pprint((math.trunc(start), math.trunc(end)))

    for h in range(math.trunc(start), math.trunc(end)+1):  # 15:38 to 16:00
        next_h = h + 1
        if left > (next_h - start):
            # print('to',h,'add',(next_h - start)*60,'minutes')
            print('to', h, 'add', (next_h - start), 'points')
            hours[h] += next_h - start
            assert ((next_h - start) <=
                    1), f"({next_h} - {start}) > 1 ; {r_start} and {r_end}"
            left = left - (next_h - start)
        else:
            # print('to',h,'add',left*60,'minutes')
            print('to', h, 'add', left, 'points')
            hours[h] += left
            left = 0
        if left == 0:
            break
        # trunc only first time , then 15, 16,...
        start = math.trunc(start) + 1

    # XXX add left to 16:00?


heatmap_data = {}

# group by day
for date, day in toggl.groupby(toggl.index.date):
    # print('day',date)
    hours = [0] * 24
    for _, row in day.iterrows():
        # print('start',row['Start time'], 'end',row['End time'])
        update_hours(hours, row['Start time'], row['End time'])
    heatmap_data[date] = hours

# heatmap_data
heatmap = pd.DataFrame.from_dict(heatmap_data, orient='index')

fig, ax = plt.subplots(figsize=(15, 10))
# or cmap="crest"
tmp = heatmap.transpose()
tmp = tmp.reindex(index=tmp.index[::-1])
p = sns.heatmap(tmp, cmap="coolwarm", square=True,
                ax=ax, cbar=False)  # cbar=False no legend

fig = p.get_figure()
fig.savefig("out.png")
