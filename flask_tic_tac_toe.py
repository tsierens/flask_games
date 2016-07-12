import numpy as np
#import pandas as pd
import random
import time
import sys
import tic_tac_toe as ttt
from flask import Flask, render_template, request, redirect
import json
import pickle

with open('t3_net.pkl','rb') as f:
    value = pickle.load(f)
    


def net_value(board):
    t0=time.clock()

    h = board.reshape(9)
    activations = [np.vectorize(lambda x: max(0.,x))]*(len(value)-1) + [np.tanh]
    for i,layer in enumerate(value):
        h = activations[i](np.dot(h,layer[0])+layer[1])
    return float(h)

def sym_net_value(board):
    board = board.reshape((3,3))
    boards = [board,board.transpose()]
    for i in range(3):
        dummy_board = np.rot90(board)
        boards += [board,board.transpose()]
#    print boards
    return sum(net_value(b) for b in boards) / 8


def game_over(board):
    return ttt.is_full(board) or ttt.winner(board)
class alpha_beta:
    def __init__(self,depth):
        self.depth = depth
    def make_move(self,board,active_turn):
        #print (board,active_turn,self.depth)
        return alpha_beta_move(board,active_turn,self.depth)[1]
inf = float("inf")

def winning_squares(board):
    board = board.reshape((3,3))
    winners = set()
    for i in range(3):
        if abs(sum(board[i,:])) == 3:
            winners.update((i,j) for j in range(3))
        if abs(sum(board[:,i])) == 3:
            winners.update((j,i) for j in range(3))
    if abs(sum(np.diag(board))) == 3:
        winners.update((i,i) for i in range(3))
    if abs(sum(np.diag(np.fliplr(board)))) == 3:
        winners.update((i,2-i) for i in range(3))
    return winners
    

def update_move(board, move, turn):
    board[move] = turn
    return None

def unupdate_move(board, move):
    board[move] = 0
    return None
    
    
def alpha_beta_move(board, turn, depth = 0, alpha = (-inf,-inf), beta = (inf,inf), evaluation = lambda x: 0):
    dummy_board = np.copy(board).reshape(9) # we don't want to change the board state

    swap_player = {1:-1,-1:1} # So we can change whose turn
    options = ttt.available_moves(board) # get legal moves
    random.shuffle(options) # should inherit move order instead of randomizing

    best_value = (-inf,-inf)
    
    if not options:
        print board, cccc.game_over(board)
        print 'oops, no available moves'
    cand_move = options[0]
    if depth == 0: 
        for x in options:
            update_move(dummy_board,x,turn)
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
        
            if ttt.winner(dummy_board): #should check over and tied too
                return((inf,depth), x)
            
            if ttt.is_full(dummy_board): #This assumes you can't lose on your turn
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

def play(types=['human','human'],depths=(0,0),evals = ("random","random")):
    print 'starting a game of connect Four'
    return render_template('tic_tac_toe.html',
                           board = list(np.zeros(9)),
                           player = 1, 
                           finished = -2,
                           types = map(str,types),
                           depths = list(depths),
                           evals = map(str,evals))
                           
    