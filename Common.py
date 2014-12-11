#!/usr/bin/env python
#coding:utf-8
from math import sqrt
import sys, math
direction = [(-1, 0),  (0, 1), (0, -1), (1, 0)]
class weight:
	def __init__(self):
		self.weight_empty = 3
		self.weight_monotony = 0.8
		self.weight_max = 1.5
		self.weight_smoothy = 1.5
	def __str__(self):
		return "empty\t"+str(self.weight_empty) + " monotony\t"+str(self.weight_monotony) + " max\t"+str(self.weight_max)+ " smoothy\t"+str(self.weight_smoothy) + "\n"

def empty(grid):
	#print "enter empty"
	num = 0
	maxnum = 0
	sumnum = 0
	for x in xrange(grid.size):
		for y in xrange(grid.size):
			if grid.map[x][y] == 0:
				num = num+1
			else:# also consider the tiles that could be merged
				if grid.map[x][y] > maxnum:
					maxnum = grid.map[x][y]
				sumnum = sumnum + grid.map[x][y]
				for i in (0, 1):
					newx = x + direction[i][0]
					newy = y + direction[i][1]
					if not grid.crossBound((newx, newy)) and grid.map[newx][newy] == grid.map[x][y]:
						num = num + 1
	if sumnum > 1300:
		num = num * 1.5
	return num 

def smoothy(grid):
	size = grid.size
	measure = 0
	for x in xrange(size):
		for y in xrange(size):
			if grid.crossBound((x, y)) or grid.map[x][y] == 0:
				continue
			for i in (0, 1):
				newx = x + direction[i][0]
				newy = y + direction[i][1]
				if not grid.crossBound((newx, newy)) and grid.map[newx][newy] != 0:
					measure = measure - abs(grid.map[x][y] - grid.map[newx][newy])
	return -math.log(1-measure) / math.log(2)

def monotony(grid):
	scoreleft = 0
	scoreright = 0
	scoreup = 0
	scoredown = 0
	for x in xrange(grid.size):
		subscoreleft = 0# left less than right
		subscoreright = 0
		row = []
		for val in grid.map[x]:
			if val!=0:
				row.append(val)
		for i in xrange(len(row)):
			for j in xrange(i+1, len(row)):
				if row[i] <= row[j]:
					subscoreleft = subscoreleft + row[j] - row[i]
				else:
					subscoreright = subscoreright + row[i] - row[j]
		# if subscoreleft == 0 and len(row) > 1:
		# 	scoreright = scoreright / 2.0
		# if subscoreright == 0 and len(row) > 1:
		# 	scoreleft = scoreleft / 2.0
		scoreleft = scoreleft + subscoreleft
		scoreright = scoreright + subscoreright

	for y in xrange(grid.size):
		subscoreup = 0
		subscoredown = 0
		col = []
		for val in xrange(grid.size):
			if grid.map[val][y] != 0:
				col.append(grid.map[val][y])
		for i in xrange(len(col)):
			for j in xrange(i+1, len(col)):
				if col[i] <= col[j]:
					subscoreup = subscoreup + col[j] - col[i]
				else:
					subscoredown = subscoredown + col[i] - col[j]
		# if subscoredown == 0 and len(col) > 1:
		# 	subscoreup = subscoreup 
		# if subscoreup == 0 and len(col) > 1:
		# 	subscoredown = subscoredown 
		scoreup = scoreup + subscoreup
		scoredown = scoredown +subscoredown
	#print str(scoreup) +" "+ str(scoredown) +" "+ str(scoreleft)+ " "+ str(scoreright)
	return math.log(1+(max(scoreup, scoredown) + max(scoreleft, scoreright))) / math.log(2)

def visit(grid, visited, i, j):
	visited[i][j] = True
	#print "i, j is " + str(i) + str(j)
	for direct in direction:
		x = i + direct[0]
		y = j +direct[1]
		#print x, y
		if not grid.crossBound((x, y)) and grid.map[x][y] != 0 and not visited[x][y]:
			visit(grid, visited, x, y) 

def maxtile(grid):
	return math.log(grid.getMaxTile()) / math.log(2)

def score(grid_clone):
	w = weight()
	return empty(grid_clone)*w.weight_empty + \
		maxtile(grid_clone)*w.weight_max + \
		monotony(grid_clone)*w.weight_monotony + \
		smoothy(grid_clone)*w.weight_smoothy

def total(grid_clone):
	total = 0
	for x in range(4):
		for y in range(4):
			total = total + grid_clone.map[x][y]
	return total