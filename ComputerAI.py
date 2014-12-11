#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
from Common import *

class ComputerAI(BaseAI):
	
	def getMove(self, grid):
		# I'm too naive, please change me!
		depth = 0
		bestmove = (None, sys.maxint)
		while depth < 3:
			#print "depth is "+str(depth)
			beta = self.minmove(depth,(None, -1), (None, sys.maxint), grid)
			if beta[0] == None:
				break;
			if bestmove[1] > beta[1]:
				bestmove = beta
			depth = depth + 1
		return bestmove[0]
		# I’m too simple, please change me!
		# cells = grid.getAvailableCells()
		# return cells[randint(0, len(cells) - 1)] if cells else None
	def maxmove(self, depth, alpha, beta, grid):
		moves = grid.getAvailableMoves()
		for move in moves:
			if move!= None and grid.canMove([move]):
				grid_clone = grid.clone()
				grid_clone.move(move)
				next = self.minmove(depth, alpha, beta, grid_clone)
				if next[1] > alpha[1]:
					alpha = (beta[0], next[1])
				if alpha[1] >= beta[1]:
					return beta
		return alpha
	def minmove(self, depth, alpha, beta, grid):
		cells = grid.getAvailableCells()
		minimum = sys.maxint
		scores = []
		finalcells = []
		bestmove = None
		for move in cells:
			grid_clone = grid.clone()
			grid_clone.setCellValue(move, 2)
			if depth == 0:
				return (move, score(grid))
			next = self.maxmove(depth-1, alpha, beta, grid_clone)
			if next[1] < beta[1]:
				bestmove = move
				beta = (bestmove, next[1])
			if beta[1] <= alpha[1]:
				return alpha
		return (bestmove, beta[1])