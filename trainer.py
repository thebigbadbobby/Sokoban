# Note:
# Code based off: https://github.com/JoshVarty/AlphaZeroSimple/blob/master/trainer.py

import os
import numpy as np
from random import shuffle
import time
import torch
import torch.optim as optim

from MonteCarlo.BasicMonte import MCTS
from game import game as Game
import copy
verbose = False
class Trainer:

    def __init__(self, board, model, args, size, row, col, maxrow, maxcol, fname):
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
        self.fname = fname

    def execute_episode(self):

        train_examples = []
        copyBoard = copy.deepcopy(self.board)
        self.game = Game(copyBoard, self.row, self.col, self.maxrow, self.maxcol)
        exec_loop = 0
        state = self.game.getBoard()
        print('init board')
        print(self.game.toString(state))
        while True:
            print("exec_loop#: ", exec_loop)
            board = np.ndarray.flatten(state)
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
            state, _ = self.game.get_next_state(action, state, True)
            if verbose:
                print(action)
            print('state after move')
            print(self.game.toString(state))
            reward = self.game.get_reward_for_player(state)
            if exec_loop > self.args['loopStop'] and not reward:
                reward = 0
            if verbose:
                print('reward')
                print(reward)
            if reward is not None:
                ret = []
                for hist_state, hist_action_probs in train_examples:
                    ret.append((hist_state, hist_action_probs, reward))

                return ret
            exec_loop += 1

    def learn(self):
        for i in range(1, self.args['numIters'] + 1):

            print("{}/{}".format(i, self.args['numIters']))

            train_examples = []
            for eps in range(self.args['numEps']):
                print('eps #: ', eps)
                iteration_train_examples = self.execute_episode()
                train_examples.extend(iteration_train_examples)

            shuffle(train_examples)
            self.train(train_examples, i)
            filename = self.args['checkpoint_path']
            self.save_checkpoint(folder="./models/", filename=filename)

    def train(self, examples, iteration):
        optimizer = optim.SGD(self.model.parameters(), lr=5e-5)
        pi_losses = []
        v_losses = []
        for epoch in range(self.args['epochs']):
            self.model.train()

            batch_idx = 0
            while batch_idx < int(len(examples) / self.args['batch_size']):
                sample_ids = np.random.randint(len(examples), size=self.args['batch_size'])
                boards, pis, vs = list(zip(*[examples[i] for i in sample_ids]))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                boards = boards.contiguous().cuda()
                target_pis = target_pis.contiguous().cuda()
                target_vs = target_vs.contiguous().cuda()

                # compute output
                out_pi, out_v = self.model(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v

                pi_losses.append(float(l_pi))
                v_losses.append(float(l_v))

                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

                batch_idx += 1
            file1 = open(self.fname, "a")  # append mode
            file1.write(str(iteration) + ",")
            file1.write(str(epoch) + ",")
            file1.write(str(np.format_float_positional(np.mean(pi_losses)) + ","))
            file1.write(str(np.format_float_positional(np.mean(v_losses))) + "\n")
            file1.close()
            print()
            print("Policy Loss", np.mean(pi_losses))
            print("Value Loss", np.mean(v_losses))
            print("Examples:")
            print(out_pi[0].detach())
            print(target_pis[0])

    def loss_pi(self, targets, outputs):
        loss = -(targets * torch.log(outputs)).sum(dim=1)
        return loss.mean()

    def loss_v(self, targets, outputs):
        loss = torch.sum((targets-outputs.view(-1))**2)/targets.size()[0]
        return loss

    def save_checkpoint(self, folder, filename):
        if not os.path.exists(folder):
            os.mkdir(folder)

        filepath = os.path.join(folder, filename)
        torch.save(self.model.state_dict(), filepath)