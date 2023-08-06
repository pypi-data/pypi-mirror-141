# from graph import sprintmap
from graph import Heatmap
from graph import Sprintmap
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

first_half = pd.read_csv('/Users/robertsmith/heatmap/first_half.csv')
df = first_half[first_half.tag_id==8]
df = df[['x_pos','y_pos']]
dat = df.to_numpy()

thm = Heatmap(data=dat)
# thm.set_colors(color='magma')
plt = thm.create_heatmap_plot()

# plt = sprintmap(dat)
# tsm = Sprintmap(data=dat)
# plt = tsm.create_sprintmap_plot()
plt.show()
