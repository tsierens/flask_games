
import numpy as np
#import pandas as pd
from numpy import random
import time
import sys
import connect_four as cccc
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
#app.debug = True
app.board = [0]*42
app.player = 1

def net_value(board):
    t0=time.clock()
    (m1,m2,m3,m4) = np.load('TD_cccc_100_1_6million(1).npz')['arr_0']
    board = np.copy(board).reshape((1,42))
    m5 = np.dot(board, m1) + m2
    answer = np.tanh(np.dot(np.tanh(m5), m3) + m4) + random.random()*0.1 - 0.05
    print "node evaluation took {:.5}s".format(time.clock()-t0)
    return answer
#    return np.tanh(np.dot(np.vectorize(np.tanh)(m5), m3) + m4) + random.random()*0.1 - 0.05

def game_over(board):
    board = np.array(board).reshape((6,7))
    return cccc.winner(board) or cccc.is_full(board)

inf = float("inf")

def update_move(board, move, turn):
    board[np.where(board[:,move]==0)[0][-1], move] = turn
    return None
    
def unupdate_move(board, move):
    if 0 in board[:,move]:
        board[np.where(board[:,move]==0)[0][-1]+1, move] = 0
    else:
        board[0,move]=0
    return None

def alpha_beta_move(board, turn, depth = 0, alpha = -inf, beta = inf, evaluation = lambda x: 0):
    dummy_board = np.copy(board) # we don't want to change the board state

    swap_player = {1:-1,-1:1} # So we can change whose turn
    options = cccc.available_moves(board) # get legal moves
    random.shuffle(options) # should inherit move order instead of randomizing


#     if len(options) == 1:
#         update_move(board,options[0])
#         if cccc.winner(dummy_board):
#             return (inf,options[0])
#         else:
#             return (0,options[0])   
    
    best_value = -inf
    
    if not options:
        print board, cccc.game_over(board)
        print 'oops, no available moves'
    cand_move = options[0]
    if depth == 0: 
        for x in options:
            update_move(dummy_board,x,turn)
            op_value = evaluation(dummy_board*swap_player[turn])

            if -op_value > best_value:
                cand_move = x
                best_value = -op_value
                alpha = max(alpha, best_value)
    #        print depth,-op_value, best_value, cand_move,alpha,beta
            if alpha >= beta:
    #                print 'pruned'
                break   #alpha-beta cutoff
            unupdate_move(dummy_board,x)
    else:
    
        for x in options:

    #        dummy_board = np.copy(board)
    #        height= np.where(board[:,x]==0)[0][-1] #connect four only
    #        dummy_board[height, x] = turn
            update_move(dummy_board,x,turn)
        
            if cccc.winner(dummy_board): #should check over and tied too
                return(inf, x)
            
            if cccc.is_full(dummy_board): #This assumes you can't lose on your turn
                return(0 , x)
            
            op_value,_ = alpha_beta_move( dummy_board,
                                            swap_player[turn],
                                            depth-1,
                                            alpha = - beta,
                                            beta = - alpha,
                                            evaluation = evaluation)

            if -op_value > best_value:
                cand_move = x
                best_value = -op_value
                alpha = max(alpha, best_value)
    #        print depth,-op_value, best_value, cand_move,alpha,beta
            if alpha >= beta:
    #                print 'pruned'
                break   #alpha-beta cutoff
            unupdate_move(dummy_board,x)
    #        dummy_board[height, x] = 0
    return (best_value, cand_move)

def play(p1='human',p2='remote',depth=0,heir="random"):
    heir  = str(heir)
    board = np.zeros(42)
    player = 1
    player_type = {1:'human',-1:'human'}
    print 'playing tic tac toe'
    if p1 == "human":
        player_type[1] = 'human'
    else:
        player_type[1] = 'remote'
    if p2 == "human":
        player_type[-1] =  'human'
    else:
        player_type[-1] = 'remote'
    print 'starting a game of connect Four'
    print [player_type[1], player_type[-1]], heir, type(heir)
    return render_template('connect_four.html',board = list(board),heir = [heir],
                                   player =player, types = [player_type[1],player_type[-1]], depth = depth,finished = -2)
    