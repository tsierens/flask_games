import numpy as np
#import pandas as pd
import random
import time
import sys
import tic_tac_toe as ttt
import connect_four as cccc
import os
#import theano
#import theano.tensor as T
#import lasagne
from flask import Flask, render_template, request, redirect
#import json
import flask_connect_four as fc4
import flask_tic_tac_toe as ft3
app = Flask(__name__)
#app.debug = True
app.GAMES = [r"Tic_Tac_Toe", r"Connect_Four"]
app.OPTIONS = [r"Human", r"Computer"]
app.EVALUATION = ["Random", "Neural Network"]
app.DEPTH = 0
app.PLAYERS = ['1','2']
               
@app.route('/')
def main():
    return redirect('/index')
    

@app.route('/clear', methods = ['GET'])
def clear():
    return redirect('/index')
    #return render_template('index.html',op = app.OPTIONS, names = app.NAMES)

        
@app.route('/index', methods = ['GET','POST'])
def go():
    print 'HELLO!'
    if request.method == 'GET':
        print 'rendering menu'
        return render_template('menu.html')
    if request.method == 'POST':
        print 'receieved submission'
        game = request.form.get("game")
        p1 = request.form.get("p1")
        p2 = request.form.get("p2")
        depth = int(request.form.get("depth"))
        evaluation = request.form.get("eval")
        print game, game == 'ttt'
        if game == 'ttt':
            print 'calling tic tac toe initialization'
            return ft3.play(p1=p1,p2=p2,depth=depth,heir=evaluation)
        if game == 'c4':
            print 'calling connect four initialization'
            return fc4.play(p1=p1,p2=p2,depth=depth,heir=evaluation)
    return None
               
               
@app.route('/ttt',methods = ['POST'])
def play_ttt():
    player_index_dict = {-1:1,1:0}
    player = int(request.form.get("player"))
    depth = int(request.form.get("depth"))
    board = request.form.get("board")
    board = board.split(",")
    print board
    board = [int(x) for x in board]
    board = np.array(board)
    types = str(request.form.get("types"))
    types = types.split(",")

    print type(types)
    print types, board, player, ttt.game_over(np.copy(board))
    if  types[player_index_dict[player]] == 'remote' and not ttt.game_over(np.copy(board)):
        move = ft3.alpha_beta_move(board, -1, depth = depth)[1]
        print board,move
        print ''
        print ''
        board[move-1] = player
        print board
        player *= -1
    print player
    if ttt.game_over(np.copy(board)):
        if ttt.winner(board)==1:
            return render_template('tic_tac_toe.html', board = list(board), player = player, types = types,depth = depth, finished = 1)
        if ttt.winner(board) ==0:
            return render_template('tic_tac_toe.html', board = list(board), player = player, types = types,depth = depth, finished = 0)
        if ttt.winner(board) == -1:
            return render_template('tic_tac_toe.html', board = list(board), player = player, types = types,depth = depth, finished = -1)
    else:
        print 'render next move'
        return render_template('tic_tac_toe.html',board = list(board), player = player, types = types,depth = depth, finished = -2)
    
@app.route('/cccc',methods = ['POST'])
def play_cccc():
    player_index_dict = {-1:1,1:0}
    player = int(request.form.get("player"))
    depth = int(request.form.get("depth"))
    board = request.form.get("board")
    board = board.split(",")
    print board
    board = [int(x) for x in board]
    board = np.array(board).reshape((6,7))
    types = str(request.form.get("types"))
    types = types.split(",")
    heir = str(request.form.get("heir"))
    print heir
    if heir == 'nn':
        evaluation = fc4.net_value
    else:
        evaluation = lambda x: 0
    #evaluation
    print type(types)
    print types, player, fc4.game_over(np.copy(board)), heir, depth
    if  types[player_index_dict[player]] == 'remote' and not fc4.game_over(np.copy(board)):
        move = fc4.alpha_beta_move(board.reshape((6,7)), player, depth = depth, evaluation = evaluation)[1]
        print board,move
        print ''
        print ''
        fc4.update_move(board,move,player)
        print board
        player *= -1
    board = board.reshape(42)
    print player
    print fc4.game_over(np.copy(board).reshape((6,7)))
    if fc4.game_over(np.copy(board).reshape((6,7))):
        if cccc.winner(board.reshape((6,7)))==1:
            return render_template('connect_four.html', board = list(board), player = player, heir=[heir],types = types,depth = depth, finished = 1)
        if cccc.winner(board.reshape((6,7))) ==0:
            return render_template('connect_four.html', board = list(board), player = player, heir=[heir],types = types,depth = depth, finished = 0)
        if cccc.winner(board.reshape((6,7))) == -1:
            return render_template('connect_four.html', board = list(board), player = player, heir=[heir],types = types,depth = depth, finished = -1)
    else:
        print 'render next move'
        return render_template('connect_four.html',board = list(board), player = player,heir=[heir], types = types,depth = depth, finished = -2)
               
               
               
               
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)