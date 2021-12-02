class play:
    def __init__(self, game, model, mcts, args) -> None:
        self.game = game
        self.model = model
        self.args = args
        self.mcts = mcts
    def playGame(self):
        play = []
        while not self.game.isWon:
            self.mcts.run(self.model, self.game)

        print(len(play), play)
        exit()
