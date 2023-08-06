# imports
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.image import NonUniformImage
from matplotlib.patches import ConnectionPatch, Arc
from matplotlib import markers

from math import hypot

# from multimethod import multimethod

from itertools import groupby
from operator import itemgetter

# ----- Global Helper Definitions (Start) ------

def _is_ndarray(array):
	if type(array) is np.ndarray:
		if len(array.shape) == 2 and len(array[0]) == 2:
			return True
		else:
			return False
	else:
		return False

# ----- Global Helper Definitions (Finish) ------


# ----- Heatmap (Start) -----

def draw_lines(axes):
		plt.xlim([0,100])
		plt.ylim([0,68])
		axes.add_line(plt.Line2D([50, 50], [100, 0], c='w'))
		axes.add_patch(plt.Rectangle((82.3, 20.24), 15.71, 29.5, ec='w', fc='none'))
		axes.add_patch(plt.Rectangle((0, 20.24), 15.71, 29.53, ec='w', fc='none'))
		axes.add_patch(plt.Rectangle((94.8, 23.05), 5.2, 26.9, ec='w', fc='none'))
		axes.add_patch(plt.Rectangle((0, 23.05), 5.2, 26.9, ec='w', fc='none'))
		axes.add_patch(Ellipse((50, 35), 17.43, 26.91, ec='w', fc='none'))

		return axes

# helper definitions
def _create_histogram(array):
	x, y = array[:,0], array[:,1]
	heatmap, xedges, yedges = np.histogram2d(x, y, bins=50, range=[[0, 105], [0, 68]])
	heatmap = heatmap.T
	fig = plt.figure(figsize=(105/15, 68/15))
	axes = fig.add_subplot(1, 1, 1)
	im = NonUniformImage(axes, interpolation='bilinear',cmap='gnuplot')
	xcenters = (xedges[:-1] + xedges[1:]) / 2
	ycenters = (yedges[:-1] + yedges[1:]) / 2
	im.set_data(xcenters, ycenters,heatmap)
	axes.images.append(im)
	axes = draw_lines(axes)
	plt.axis('off')

	return plt

# public definitions

# takes a numpy.ndarray
def heatmap(array):
	"""
	Parameters
	----------
	array: numpy array
		A 2d numpy array.
	"""
	try:
		ndarray = _is_ndarray(array)
		if(ndarray):
			pass
		else:
			raise ValueError()
	except ValueError:
		print("Heatmap takes ndarray")
		sys.exit()

	plot = _create_histogram(array)

	return plot

# ----- Heatmap (Finish) -----

# ----- Sprintmap (Start) -----

def draw_pitch(ax):
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = plt.Rectangle([0,0], width = 120, height = 80,color="white", fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = plt.Rectangle([0,22.3], width = 14.6, height = 35.3, color="white",fill = False)
    RightPenalty = plt.Rectangle([105.4,22.3], width = 14.6, height = 35.3, color="white",fill = False)
    midline = ConnectionPatch([60,0], [60,80], "data", "data",color="white")

    #Left, Right 6-yard Box
    LeftSixYard = plt.Rectangle([0,32], width = 4.9, height = 16, color="white",fill = False)
    RightSixYard = plt.Rectangle([115.1,32], width = 4.9, height = 16, color="white",fill = False)

    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="white", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="white")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="white")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="white")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="white")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="white")

    element = [Pitch, LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle,
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    for i in element:
        ax.add_patch(i)

def graph_sprints(connected):
	fig=plt.figure() #set up the figures
	fig.set_size_inches(7, 5)
	ax=fig.add_subplot(1,1,1)
	fig.set_facecolor('black')
	draw_pitch(ax) #overlay our different objects on the pitch
	plt.ylim(-2, 82)
	plt.xlim(-2, 122)
	plt.axis('off')
	for sprint in connected:
		all_x = []
		all_y = []
		for i in sprint:
			all_x.append(i[:,0])
			all_y.append(i[:,1])

			ax.plot(i[0,0],i[0,1],'r',marker=(3, 0, ((i[1,1]-i[0,1]))/(i[1,0]-i[0,0])),markersize=10,zorder=2)
			ax.plot(i[-1,0],i[-1,1],'r', marker=(3, 0, ((i[-1,1]-i[-2,1]))/(i[-1,0]-i[-2,0])),markersize=10,zorder=2)
		ax.plot(all_x,all_y,'.b',zorder=1)


	return plt

def connect_seconds(all_sprints):
	indexes = []
	for sprint in all_sprints:
		indexes.append(sprint['index'])

	connected_seconds = []
	for k, g in groupby( enumerate(indexes), lambda x: x[1]-x[0] ) :
		consequtive_seconds = list(map(itemgetter(1), g))
		tot_sprint = []
		for sprint in all_sprints:
			if sprint['index'] in consequtive_seconds:
				tot_sprint.append(sprint['second'])
		connected_seconds.append(tot_sprint)

	return connected_seconds

def calculate_speed(second):
	x1 = 0
	y1 = 0
	total_distance = 0
	for index, frame in enumerate(second):
		if index == 0:
			x1 = frame[0]
			y1 = frame[1]
		x2 = frame[0]
		y2 = frame[1]
		distance = hypot(x2 - x1, y2 - y1)
		total_distance = total_distance + distance
		# initial point to this ending point
		x1 = x2
		y1 = y2

	return total_distance

def analyze_seconds(spl_array):
	all_sprints = []
	for index, second in enumerate(spl_array):
		speed = calculate_speed(second)
		if speed >= 6.7:
			sprint = {'index': index, 'second': second}
			all_sprints.append(sprint)

	return all_sprints

def split_array(array):
	trim_num = len(array) % 20
	array = array[:len(array)-trim_num]
	spl_array = np.split(array, len(array)/20)
	return spl_array

# @multimethod
def sprintmap(array):
	try:
		ndarray = _is_ndarray(array)
		if(ndarray):
			pass
		else:
			raise ValueError()
	except ValueError:
		print("Sprintmap takes ndarray")
		sys.exit()
	spl_array = split_array(array)

	all_sprints = analyze_seconds(spl_array)

	connected = connect_seconds(all_sprints)

	graph = graph_sprints(connected)

	return graph

# @multimethod
# def sprintmap(a,b):
# 	# print(a+b) testing...


# ----- Sprintmap (Finish) -----
