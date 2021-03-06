from MonteCarlo.BasicMonte import MCTS
import numpy as np
import copy
from game import game as Game
import torch
import torch.optim as optim
import os
verbose = False
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
            state, move = self.game.get_next_state(action, state, True)
            if verbose:
                print(action)
            print('state after move')
            print(self.game.toString(state))
            play.append(move)
            reward = self.game.get_reward_for_player(state)
            if exec_loop > self.args['loopStop'] and not reward:
                reward = 0
            if reward is not None:
                ret = []
                for hist_state, hist_action_probs in train_examples:
                    ret.append((hist_state, hist_action_probs, reward))
                self.train(ret)
                filename = self.args['checkpoint_path']
                self.save_checkpoint(folder="./models/", filename=filename)
                if reward == 0: # reset
                    play = []
                    copyBoard = copy.deepcopy(self.game.getBoard())
                    state = copyBoard
            exec_loop += 1
            if reward == 0:
                exec_loop = 0
        result = ''
        for letter in play:
            result += letter + ' '
        print(len(play), result)
        exit()

    def train(self, examples):
        optimizer = optim.SGD(self.model.parameters(), lr=5e-5)
        pi_losses = []
        v_losses = []
        for _ in range(self.args['epochs']):
            self.model.train()
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