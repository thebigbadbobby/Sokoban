# Note:
# Adopted code from source: https://github.com/JoshVarty/AlphaZeroSimple/blob/master/monte_carlo_tree_search.py

import math
import numpy as np

import random
verbose = False

def ucb_score(parent, child):
    """
    The score for an action that would transition between the parent and child.
    """
    prior_score = child.prior * math.sqrt(parent.visit_count) / (child.visit_count + 1)
    return prior_score

class Node:
    def __init__(self, prior):
        self.visit_count = 0
        self.prior = prior
        self.value_sum = 0
        self.children = {}
        self.state = None

    def expanded(self):
        return len(self.children) > 0

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def select_action(self, temperature):
        """
        Select action according to the visit count distribution and the temperature.
        """
        visit_actionPairs = []
        visit_counts = np.array([child.visit_count for child in self.children.values()])
        actions = [action for action in self.children.keys()]
        for i in range(0, len(actions)):
            visit_actionPairs.append((visit_counts[i], actions[i]))
        
        if temperature == 0:
            best = []
            for pair in visit_actionPairs:
                if not best:
                    best.append(pair)
                    continue
                if best and pair[0] > best[0][0]:
                    best = [pair]
                    continue
                if best and pair[0] == best[0][0]:
                    best.append(pair)
            random.shuffle(best)
            if verbose:
                print('best in move')
                print(best)
            action = best[0][1]
        elif temperature == float("inf"):
            try:
                action = actions[np.random.randint(0,np.argmax(actions)-1)]
            except:
                action=actions[0]
        else:
            # See paper appendix Data Generation
            visit_count_distribution = visit_counts ** (1 / temperature)
            visit_count_distribution = visit_count_distribution / sum(visit_count_distribution)
            action = np.random.choice(actions, p=visit_count_distribution)

        return action

    # make action put out something that indicates right, left, etc. 
    def select_child(self, game, state):
        """
        Select the child with the highest UCB score.
        """
        best = []
        cords = game.findPerson(state)
        for action, child in self.children.items():
            score = ucb_score(self, child)
            if not best:
                best.append((score, action, child))
                continue
            if best and score > best[0][0] and game.checkValid(action, state):
                best = [(score, action, child)]
                continue
            if best and score == best[0][0] and game.checkValid(action, state):
                best.append((score, action, child))
        if not best:
            print('wee woo invalid')
            exit()
        random.shuffle(best)
        best_action = best[0][1]
        best_child = best[0][2]
        return best_action, best_child

    def expand(self, state, action_probs, game):
        """
        We expand a node and keep track of the prior policy probability given by neural network
        """
        self.state = state
        cords = game.findPerson(state)
        missedValid = []
        probMissing = 1
        for i in range(0, len(action_probs)):
            for j in range(0, len(action_probs[i])):
                prob = action_probs[i][j]
                if game.checkValid((i, j), state):
                    if prob != 0:
                        self.children[(i, j)] = Node(prior = prob)
                        probMissing -= prob
                    else:
                        missedValid.append((i, j))
        # for the cases where we missed some children cuz of 0 prob
        for c in missedValid:
            if verbose:
                print("cords missing")
                print(probMissing)
                print(c)
            self.children[c] = Node(prior = probMissing/len(missedValid))

    def __repr__(self):
        """
        Debugger pretty print node info
        """
        prior = "{0:.2f}".format(self.prior)
        return "{} Prior: {} Count: {} Value: {}".format(self.state.__str__(), prior, self.visit_count, self.value())

class MCTS:

    def __init__(self, game, model, args, row, col, actualRow, actualCol):
        self.game = game
        self.model = model
        self.args = args
        self.row = row
        self.col = col
        self.actualRow = actualRow
        self.actualCol = actualCol

    def run(self, model, state):

        root = Node(0)

        #state needs to be 1xnumofelements array
        action_probs, value = model.predict(state)
        # translate action_probs into a mxn array
        action_probs = np.array(action_probs).reshape(self.row, self.col) # map these to a size var
        valid_moves = self.game.get_valid_moves(state) #we know the moves can be up, left, down right so mask based off of position
        action_probs = action_probs * valid_moves  # mask invalid moves
        action_probs /= np.sum(action_probs)
        root.expand(state, action_probs, self.game)
        for _ in range(self.args['num_simulations']):
            node = root
            search_path = [node]
            
            # Select which node to play and maybe expand
            while node and node.expanded():
                action, node = node.select_child(self.game, node.state)
                search_path.append(node)
            parent = search_path[-2]
            state = parent.state
            # Now we're at a leaf node and we would like to expand
            # Players always play from their own perspective
            next_state, _ = self.game.get_next_state(action, state)

            # The value of the new state from the perspective of the other player
            value = self.game.get_reward_for_player(next_state) # a function that determines if we finished or 
            if value is None:
                # If the game has not ended:
                # EXPAND
                action_probs, value = model.predict(next_state)
                valid_moves = self.game.get_valid_moves(next_state)
                # ogAction_probs = action_probs
                action_probs = np.array(action_probs).reshape(self.row, self.col) # map these to a size var
                action_probs = action_probs * valid_moves  # mask invalid moves
                action_probs /= np.sum(action_probs)
                node.expand(next_state, action_probs, self.game)

            self.backpropagate(search_path, value)

        return root

    def backpropagate(self, search_path, value):
        """
        At the end of a simulation, we propagate the evaluation all the way up the tree
        to the root.
        """
        for node in reversed(search_path):
            node.value_sum += value
            node.visit_count += 1