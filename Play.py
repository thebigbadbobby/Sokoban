from MonteCarlo.BasicMonte import MCTS
import numpy as np
import copy
from game import game as Game
class play:
    def __init__(self, board, model, args, size, row, col, maxrow, maxcol):
        self.board = board
        self.row = row 
        self.col = col 
        self.maxrow = maxrow
        self.maxcol = maxcol
        self.game = Game(self.board, row, col, maxrow, maxcol)
        self.model = model
        self.args = args
        self.action_size = size
        self.mcts = MCTS(self.game, self.model, self.args, maxrow, maxcol, row, col)
    def playGame(self):
        play = []
        state = self.game.getBoard()
        exec_loop = 0
        train_examples = []
        print('init board')
        print(self.game.toString(state))
        while not self.game.isWon(state):
            board = np.ndarray.flatten(state)
            print("exec_loop#: ", exec_loop)
            self.mcts = MCTS(self.game, self.model, self.args, self.maxrow, self.maxcol, self.row, self.col)
            root = self.mcts.run(self.model, board)
            action_probs = [0 for _ in range(self.action_size)]
            i = 0
            for k in root.children.keys():
                action_probs[i] = root.children[k].visit_count
                i+=1

            action_probs = action_probs / np.sum(action_probs)
            train_examples.append((board, action_probs))

            action = root.select_action(temperature=0)
            print(action)
            print('GETTING DA MOVE')
            state, move = self.game.get_next_state(action, state, True)
            play.append(move)
            print('state after move')
            print(self.game.toString(state))
            reward = self.game.get_reward_for_player(state)
            if exec_loop > self.args['loopStop'] and not reward:
                reward = 0
            if reward is not None:
                ret = []
                for hist_state, hist_action_probs in train_examples:
                    # [Board, currentPlayer, actionProbabilities, Reward]
                    ret.append((hist_state, hist_action_probs, reward))
                if reward == 0: # reset
                    play = []
                    copyBoard = copy.deepcopy(self.game.getBoard())
                    state = copyBoard
            exec_loop += 1
        
        print(len(play), play)
        exit()
