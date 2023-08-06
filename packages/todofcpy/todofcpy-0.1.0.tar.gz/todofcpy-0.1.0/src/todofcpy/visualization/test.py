from graph import sprintmap

import pandas as pd
import numpy as np

first_half = pd.read_csv('/Users/robertsmith/heatmap/first_half.csv')
df = first_half[first_half.tag_id==8]
df = df[['x_pos','y_pos']]
df = df.reset_index()
dat = df.to_numpy()

sprintmap(dat)
