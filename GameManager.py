#!/usr/bin/env python
#coding:utf-8

from Grid import Grid
from ComputerAI import ComputerAI
from PlayerAI import PlayerAI
from Displayer import Displayer
from random import randint
import time
from Common import *

defaultInitialTiles = 2
defaultPossibility = 0.9
(PLAYER_TURN, COMPUTER_TURN) = (0, 1)
actionDic = {0:"UP", 1:'DOWN', 2:'LEFT', 3:'RIGHT'}
# time limit for guess time of each step
timeLimit = 1

class GameManager:
	def __init__(self, size = 4):
		# init some variables
		self.grid = Grid(size)
		self.possibleNewTileValue = [2, 4]
		self.possibility = defaultPossibility
		self.initTiles = defaultInitialTiles
		self.computerAI = None
		self.playerAI = None
		self.displayer = None
		self.over = False

	def setComputerAI(self, compAI):
		self.computerAI = compAI

	def setPlayerAI(self, playerAI):
		self.playerAI = playerAI

	def setDisplayer(self, displayer):
		self.displayer = displayer

	def updateAlarm(self, curTime):
		# 0.1 sec for the running time outside the AI module
		if curTime - self.lastTime > timeLimit + 0.1:
			self.over = True
		else:
			self.lastTime = curTime

	def start(self, weight):
        #insert 2 random tiles
		for i in xrange(self.initTiles):
			self.insertRandonTile()

		# show the initial grid state
		# self.displayer.display(self.grid)

		#player plays first
		turn = PLAYER_TURN
		maxTile = 0

		# set init alarm
		self.lastTime = time.clock()

		# check game over conditions
		while not self.isGameOver() and not self.over:
            # make a copy make sure AI cannot change the real grid and cheat
			gridCopy = self.grid.clone()
			move = None

			if turn == PLAYER_TURN:
				# print "Player's Turn"
				move = self.playerAI.getMove(gridCopy, weight)
				# print actionDic[move]

				#validate move
				if move != None and move >= 0 and move < 4:
					if self.grid.canMove([move]):
						self.grid.move(move)
						#update maxTile
						maxTile = self.grid.getMaxTile()
					else:
						print "Invalid PlayerAI Move"
						self.over = True
				else:
					print "Invalid PlayerAI Move - 1"
					self.over = True
			else:
				# print "Computer's turn"
				move = self.computerAI.getMove(gridCopy)
				#validate move
				if move and self.grid.canInsert(move):
					self.grid.setCellValue(move, self.getNewTileValue())
				else:
					print "Invalid Computer AI Move"
					self.over = True

			if not self.over:
				self.displayer.display(self.grid)
				
			# once you exceeds the time limit, previous action will be your last action
			self.updateAlarm(time.clock())
			#print "total is "+str(total(self.grid))
			turn = 1-turn
		# print maxTile
		return maxTile, total(self.grid)


	def isGameOver(self):
		return not self.grid.canMove()

	def getNewTileValue(self):
		if randint(0,99) < 100 * self.possibility: 
			return self.possibleNewTileValue[0] 
		else: 
			return self.possibleNewTileValue[1];

	def insertRandonTile(self):
		tileValue = self.getNewTileValue()
		cells = self.grid.getAvailableCells()
		cell = cells[randint(0, len(cells) - 1)]
		self.grid.setCellValue(cell, tileValue)


def main():
	w = weight()
	playerAI  	= PlayerAI()
	computerAI  = ComputerAI()
	displayer 	= Displayer()	
	monotony = [0.7,0.8, 0.85, 0.9] 
	smoothy = [ [ 1.4, 1.425, 1.45], [ 1.5, 1.525, 1.55 ], [1.7, 1.725, 1.75], [1.65, 1.675, 1.7] ]
	# monotony = [0.8]
	# smoothy = [[ 1.5]]
	
	for i in range(len(monotony)):
		w.weight_monotony = monotony[i]
		for j in range(len(smoothy[i])):
			for roundnum in range(4):
				gameManager = GameManager()
				gameManager.setDisplayer(displayer)
				gameManager.setPlayerAI(playerAI)
				gameManager.setComputerAI(computerAI)						
				w.weight_smoothy = smoothy[i][j]
				result = gameManager.start(w)
				print " \nround " + str(roundnum) +" \nweight is " + str(w) + " score is " + str(result[0])+ " total is " + str(result[1])


if __name__ == '__main__':
	main()