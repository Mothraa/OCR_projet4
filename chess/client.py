from chess.controller import MainController


class Client():
    app = None

    def __init__(self):
        self.app = MainController()

    def run(self):
        self.app.run()
