import logging


from chess.controller import Controller
from chess.view import View
# import chess.controller

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        filename="logfile.log",
                        filemode="w",  # "a"
                        format='%(asctime)s - %(levelname)s : %(message)s')  # WARNING

    controller = Controller()
    vue = View()
    vue.MainMenu()
    pass
    controller.run()
# # #    logging.warning("whoaa!")
