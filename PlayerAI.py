# #!/usr/bin/env python
# #coding:utf-8

from random import randint
from BaseAI import BaseAI

from Common import *

#from ComputerAI import ComputerAI

class PlayerAI(BaseAI):
	def getMove(self, grid, weight):
		# I'm too naive, please change me!
		
		depth = 0
		cells = grid.getAvailableCells()
		limit = 3
		bestmove = (None, 0)
		while depth < limit:
			#print "depth is "+str(depth)
			alpha = self.maxmove(depth,(None, -1), (None, sys.maxint), grid, weight)
			if alpha[0] == None:
				break;
			if bestmove[1] < alpha[1]:
				bestmove = alpha
			# if depth == 1 and grid.getMaxTile() < 128:
			# 	break;
			depth = depth + 1
		return bestmove[0]

		# moves = grid.getAvailableMoves()
		# return moves[randint(0, len(moves) - 1)] if moves else None
	def maxmove(self, depth, alpha, beta, grid, weight):
		#print "max move with alpha "+str(alpha)+" beta "+str(beta) +" depth "+str(depth)
		moves = grid.getAvailableMoves()
		bestmove = None
		for move in moves:
			if move!= None and grid.canMove([move]):
				grid_clone = grid.clone()
				grid_clone.move(move)
				if depth == 0:
					return (move,score(grid_clone))
				next = self.minmove(depth-1, alpha, beta, grid_clone, weight)
				if next[1] > alpha[1]:
					bestmove = move
					alpha = (bestmove, next[1])
				if alpha[1] >= beta[1]:
					return beta
		return (bestmove, alpha[1])
	def minmove(self, depth, alpha, beta, grid, weight):
		cells = grid.getAvailableCells()
		minimum = sys.maxint
		scores = []
		finalcells = []
		for cell in cells:
			grid.setCellValue(cell, 2)
			temp1 = score(grid)
			grid.setCellValue(cell, 0)
			scores.append((2, temp1, cell))
		#print "the branching factor in minmove is " + str(len(finalcells))
		for move in scores:
			grid_clone = grid.clone()
			grid_clone.setCellValue(move[2], move[0])
			next = self.maxmove(depth, alpha, beta, grid_clone, weight)
			if next[1] < beta[1]:
				beta = (alpha[0], next[1])
			if beta[1]<=alpha[1]:
				return alpha
		return beta

