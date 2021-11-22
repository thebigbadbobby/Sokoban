import torch
import math
import numpy as np
import node as Node


class MCTS:

    def __init__(self, game, model, args):
        self.game = game
        self.model = model
        self.args = args

    def run(self, model, state):

        root = Node(0)

        # EXPAND root
        #state needs to be 1xnumofelements array
        action_probs, value = model.predict(state)
        # translate action_probs into a mxn array
        action_probs = np.array(action_probs).reshape(28, 28)
        valid_moves = self.game.get_valid_moves() #we know the moves can be up, left, down right so mask based off of position
        action_probs = action_probs * valid_moves  # mask invalid moves
        action_probs /= np.sum(action_probs)
        root.expand(state, action_probs)

        for _ in range(self.args['num_simulations']):
            node = root
            search_path = [node]

            # SELECT
            while node.expanded():
                action, node = node.select_child()
                search_path.append(node)

            parent = search_path[-2]
            state = parent.state
            # Now we're at a leaf node and we would like to expand
            # Players always play from their own perspective

            #reroute to our function
            next_state, _ = self.game.get_next_state(state, action=action)
            # # Get the board from the perspective of the other player (WE DONT NEED THIS?)
            # next_state = self.game.get_canonical_board(next_state, player=-1)

            # The value of the new state from the perspective of the other player
            value = self.game.get_reward_for_player(next_state) # a function that determines if we finished or 
            if value is None:
                # If the game has not ended:
                # EXPAND
                action_probs, value = model.predict(next_state)
                valid_moves = self.game.get_valid_moves(next_state)
                action_probs = action_probs * valid_moves  # mask invalid moves
                action_probs /= np.sum(action_probs)
                node.expand(next_state, action_probs)

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