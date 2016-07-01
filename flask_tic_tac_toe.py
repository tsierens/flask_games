import numpy as np
#import pandas as pd
import random
import time
import sys
import tic_tac_toe as ttt
from flask import Flask, render_template, request, redirect
import json

def game_over(board):
    return ttt.is_full(board) or ttt.winner(board)
class alpha_beta:
    def __init__(self,depth):
        self.depth = depth
    def make_move(self,board,active_turn):
        #print (board,active_turn,self.depth)
        return alpha_beta_move(board,active_turn,self.depth)[1]
def alpha_beta_move(board, turn, depth = 0, alpha = (-inf,-inf), beta = (inf,inf), evaluation = lambda x: 0):
    dummy_board = np.copy(board).reshape(9) # we don't want to change the board state

    swap_player = {1:-1,-1:1} # So we can change whose turn
    options = cccc.available_moves(board) # get legal moves
    random.shuffle(options) # should inherit move order instead of randomizing

    best_value = (-inf,-inf)
    
    if not options:
        print board, cccc.game_over(board)
        print 'oops, no available moves'
    cand_move = options[0]
    if depth == 0: 
        for x in options:
            dummy_board[x] = turn
            op_value = (evaluation(dummy_board*swap_player[turn]) , depth)

            if tuple(-1 * el for el in op_value) > best_value:
                cand_move = x
                best_value = tuple(-1 * el for el in op_value)
                alpha = max(alpha, best_value)
            if alpha >= beta:
                break   #alpha-beta cutoff
            unupdate_move(dummy_board,x)
    else:
        for x in options:

            update_move(dummy_board,x,turn)
        
            if cccc.winner(dummy_board): #should check over and tied too
                return((inf,depth), x)
            
            if cccc.is_full(dummy_board): #This assumes you can't lose on your turn
                return((0,depth) , x)
            
            op_value,_ = alpha_beta_move( dummy_board,
                                            swap_player[turn],
                                            depth-1,
                                            alpha = tuple(-1 * el for el in beta),
                                            beta = tuple(-1 * el for el in alpha),
                                            evaluation = evaluation)

            if tuple(-1 * el for el in op_value) > best_value:
                cand_move = x
                best_value = tuple(-1 * el for el in op_value)
                alpha = max(alpha, best_value)
    #        print depth,-op_value, best_value, cand_move,alpha,beta
            if alpha >= beta:
    #                print 'pruned'
                break   #alpha-beta cutoff
            unupdate_move(dummy_board,x)
    #        dummy_board[height, x] = 0
    return (best_value, cand_move)

def play(p1='human',p2='remote',depth=0,heir=None):
    board = np.zeros(9)
    player = 1
    player_type = {1:'human',-1:'human'}
    print 'playing tic tac toe'
    if p1 == "human":
        player1 = ttt.player()
        player_type[1] = 'human'
    else:
        player1 = alpha_beta(depth)
        player_type[1] = 'remote'
    if p2 == "human":
        player2 = ttt.player()
        player_type[-1] =  'human'
    else:
        player2 = alpha_beta(depth)
        player_type[-1] = 'remote'
    print 'starting a game of tic tac toe'
    print [player_type[1], player_type[-1]]
    return render_template('tic_tac_toe.html',board = list(board),
                                   player =player, types = [player_type[1],player_type[-1]], depth = depth,finished = -2)
    
    
    