Name: Lixin Yao
UNI:ly2328
email: ly2328@columbia.edu

This is the readme file for AI 2048 project. The project try to use minimax algorithm with alpha beta pruning to solve the 2048 problem. 

How to run:
To see how the AI program solve the problem automaticly, run the following command:

	python GameManager.py

The game board will appear, every decision of PlayerAI and ComputerAI will be displayed alternatively. If the game end or time limit exceeds, the final score will be displayed.

How the algorithm works:

PlayerAI use iteratively deepening method to get the best move solution. The depth increases every time of up to 2. That is, the maxmove function in PlayerAI will execute 3 times, with last time returning the heuristic evaluation function. In every maxmove() function, another function named minmove() that simulating the computer action will be called. The alpha beta parameters are passed between these two functions to do the pruning. 

The alpha parameter is updated in maxmove() function, and if in next level the return value is greater than alpha, alpha is replaced by the greater value. If the value is less than the beta parameter, there is no need to continue the function, and we could just return. The same analysis applies to beta and minmove() function. Beta will be updated every time the value returned from next value is less than current beta. If the beta is even less than the alpha parameter in the current function, there is no need to search deeper and the function just returns.

How the module organized:

The module Common is used to store the common function that could be used by both computerAI and PlayerAI. That is mainly the calculation of heuristic functions.

The calculation of heuristic function is called score(). The score is combined by 4 parts:
Part 1:
Calculate the number of empty cells. Besides empty cells, we also consider adjacent cell with same value as empty because there will be one more empty cell if they merge later.

Also, to increase the weight of empty when the number is very small, I record the sum of every tiles and increase the weight of empty when the sum exceed a threshold. This works fine.

Part 2:
The second part calculates the measurement of monotony feature. It means that we want to see more conditions where tiles in a row increase in sequence or decrease in sequence. The same idea applies to column. We calculate the diff between tiles and use log2 function to normalize it. 

Part 3:
The third part is the current max tile value. Of course we want to see the max value to increase. We also use log2 function to normalize it, because otherwise the value will make other factors useless.

Part 4:
The fourth part is the measurement of smoothness. It check to see whether adjacent cells have the same value. Unlike what we do in empty function by just increase the empty by 1, we increase the measurement by the value of the cell (after log function). Smoothness could make the merge happen more frequently.

The ComputerAI and PlayerAI just follow the structure that are given. The main purpose is to get the next move for either Computer or player. Each module have its own maxmove and minmove functions to simulate the move and get the best move.


