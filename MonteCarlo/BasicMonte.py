import torch
import math
import numpy as np
# import Node as Node
import time
def ucb_score(parent, child):
    """
    The score for an action that would transition between the parent and child.
    """
    prior_score = child.prior * math.sqrt(parent.visit_count) / (child.visit_count + 1)
    if child.visit_count > 0:
        # The value of the child is from the perspective of the opposing player
        value_score = -child.value()
    else:
        value_score = 0

    return value_score + prior_score

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
        visit_counts = np.array([child.visit_count for child in self.children.values()])
        actions = [action for action in self.children.keys()]
        # print(actions)
        # print(visit_counts)
        if temperature == 0:
            action = actions[np.argmax(visit_counts)]
        elif temperature == float("inf"):
            action = np.random.choice(actions)
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
        best_score = -np.inf
        cords = game.findPerson(state)
        best_action = (0, 0)
        best_child = None
        for action, child in self.children.items():
            score = ucb_score(self, child)
            # print(score)
            # print(action)
            # print(cords)
            # time.sleep(1)
            if score > best_score and game.checkValid(action, state):
                best_score = score
                best_action = action
                best_child = child
        if not best_child:
            print('wee woo invalid')
            exit()
            # print()
            # print('not bsts child')
            for action, child in self.children.items():
                score = ucb_score(self, child)
                # print(action)
                if score > best_score:
                    best_score = score
                    best_action = action
                    best_child = child
        # print("best_action: ", best_action)
        # print("game location: ", game.findPerson())
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
                    # print('inside')
                    # print(i, j, prob)
                    # print(cords)
                    if prob != 0:
                        self.children[(i, j)] = Node(prior = prob)
                        probMissing -= prob
                    else:
                        # print(i, j)
                        missedValid.append((i, j))
        # for the cases where we missed some children cuz of 0 prob
        for c in missedValid:
            print("cords missing")
            print(probMissing)
            print(c)
            self.children[c] = Node(prior = probMissing/len(missedValid))
            exit()
                        
        # for a, prob in enumerate(action_probs):
        #     if prob != 0:
        #         self.children[a] = Node(prior=prob)

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
        print(np.shape(state))
        root = Node(0)

        # EXPAND root
        #state needs to be 1xnumofelements array
        action_probs, value = model.predict(state)
        # translate action_probs into a mxn array
        # ogAction_probs = action_probs
        action_probs = np.array(action_probs).reshape(self.row, self.col) # map these to a size var
        # print(ogAction_probs.shape)
        valid_moves = self.game.get_valid_moves(state) #we know the moves can be up, left, down right so mask based off of position
        action_probs = action_probs * valid_moves  # mask invalid moves
        action_probs /= np.sum(action_probs)
        root.expand(state, action_probs, self.game)

        for _ in range(self.args['num_simulations']):
            node = root
            search_path = [node]
            
            # SELECT
            while node and node.expanded():
                action, node = node.select_child(self.game, node.state)
                search_path.append(node)
                # print(node)
            parent = search_path[-2]
            state = parent.state
            # Now we're at a leaf node and we would like to expand
            # Players always play from their own perspective
            next_state = self.game.get_next_state(action, state)
            # The value of the new state from the perspective of the other player
            value = self.game.get_reward_for_player(state) # a function that determines if we finished or 
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
                # exit()

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